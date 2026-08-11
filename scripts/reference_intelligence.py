#!/usr/bin/env python3
"""Ingest GIF references into deterministic local state."""

import argparse
import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path

from PIL import Image, ImageChops, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CURATED = ROOT / "research" / "reference-studies" / "visual-library.json"
DEFAULT_STATE = ROOT / ".plugin-state" / "reference-studies"
SAMPLE_LABELS = ("first", "middle", "pre_seam", "final")


class ReferenceIngestionError(ValueError):
    """A source or curated record cannot produce a valid reference library."""


def _reference_number(reference_id: str) -> int:
    if not isinstance(reference_id, str) or not reference_id.startswith("REF-"):
        raise ReferenceIngestionError(f"invalid reference id: {reference_id!r}")
    try:
        return int(reference_id[4:])
    except ValueError as exc:
        raise ReferenceIngestionError(f"invalid reference id: {reference_id!r}") from exc


def load_reference_library(path: Path = DEFAULT_CURATED) -> dict:
    try:
        library = json.loads(path.read_text())
    except FileNotFoundError as exc:
        raise ReferenceIngestionError(f"missing reference library: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ReferenceIngestionError(f"invalid reference library JSON: {exc}") from exc
    if library.get("schema_version") != 1:
        raise ReferenceIngestionError("reference library schema_version must be 1")
    references = library.get("references")
    if not isinstance(references, list):
        raise ReferenceIngestionError("reference library requires references list")
    seen_ids = set()
    for row in references + library.get("aliases", []):
        if "id" in row:
            _reference_number(row["id"])
            if row["id"] in seen_ids:
                raise ReferenceIngestionError(f"duplicate reference id: {row['id']}")
            seen_ids.add(row["id"])
        if not isinstance(row.get("source_filename"), str) or not row["source_filename"]:
            raise ReferenceIngestionError("reference row missing source_filename")
    return library


def _curated_by_filename(curated: dict) -> dict[str, dict]:
    rows = curated.get("references", []) + curated.get("aliases", [])
    defaults = curated.get("defaults", {})
    return {row["source_filename"]: {**defaults, **row} for row in rows}


def _gif_paths(library: Path) -> list[Path]:
    if not library.is_dir():
        raise ReferenceIngestionError(f"reference library directory not found: {library}")
    paths = sorted(path for path in library.iterdir() if path.is_file() and path.suffix.lower() == ".gif")
    if not paths:
        raise ReferenceIngestionError(f"no GIF files found in {library}")
    return paths


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _scaled(frame: Image.Image) -> Image.Image:
    scaled = frame.convert("RGBA")
    scaled.thumbnail((160, 160), Image.Resampling.NEAREST)
    return scaled


def _changed_share(before: Image.Image, after: Image.Image) -> float:
    channels = ImageChops.difference(before, after).split()
    changed = ImageChops.lighter(ImageChops.lighter(channels[0], channels[1]), channels[2])
    changed = ImageChops.lighter(changed, channels[3])
    unchanged_pixels = changed.histogram()[0]
    return 1 - unchanged_pixels / (changed.width * changed.height)


def _visible_share(frame: Image.Image) -> float:
    alpha = frame.getchannel("A")
    return 1 - alpha.histogram()[0] / (alpha.width * alpha.height)


def _palette_shares(frame: Image.Image) -> list[dict]:
    colors = Counter(frame.get_flattened_data())
    total = frame.width * frame.height
    return [
        {"hex": "#%02X%02X%02X%02X" % color, "share": round(count / total, 6)}
        for color, count in colors.most_common(8)
    ]


def _sample_indices(frame_count: int) -> dict[str, int]:
    return {
        "first": 0,
        "middle": frame_count // 2,
        "pre_seam": max(0, frame_count - 2),
        "final": frame_count - 1,
    }


def _decode_metrics(source: Path) -> tuple[dict, dict[str, Image.Image]]:
    try:
        image = Image.open(source)
        if image.format != "GIF":
            raise ReferenceIngestionError(f"not a GIF: {source.name}")
        frame_count = image.n_frames
        samples = _sample_indices(frame_count)
        sampled_frames = {}
        durations = []
        changes = []
        visible_shares = []
        first_scaled = None
        previous_scaled = None
        final_scaled = None
        for index in range(frame_count):
            image.seek(index)
            rgba = image.convert("RGBA")
            durations.append(int(image.info.get("duration", 0) or 0))
            scaled = _scaled(rgba)
            visible_shares.append(_visible_share(scaled))
            if previous_scaled is not None:
                changes.append(_changed_share(previous_scaled, scaled))
            if index == 0:
                first_scaled = scaled.copy()
            if index in samples.values():
                for label, sample_index in samples.items():
                    if index == sample_index:
                        sampled_frames[label] = rgba.copy()
            previous_scaled = scaled
            final_scaled = scaled
        duration_ms = sum(durations)
        metrics = {
            "dimensions": [image.width, image.height],
            "bytes": source.stat().st_size,
            "frame_count": frame_count,
            "duration_ms": duration_ms,
            "fps": round(frame_count * 1000 / duration_ms, 6) if duration_ms else None,
            "loop": image.info.get("loop"),
            "palette_shares": _palette_shares(first_scaled),
            "frame_completeness": round(visible_shares[0] / max(visible_shares), 6) if max(visible_shares) else 1.0,
            "changed_pixel_mean": round(sum(changes) / len(changes), 6) if changes else 0.0,
            "seam_ratio": round(_changed_share(final_scaled, first_scaled), 6),
        }
        return metrics, sampled_frames
    except (UnidentifiedImageError, OSError, EOFError) as exc:
        raise ReferenceIngestionError(f"failed to decode {source.name}: {exc}") from exc
    finally:
        if "image" in locals():
            image.close()


def _cached_reference(state_dir: Path, cached: dict | None, reference_id: str, sha256: str) -> dict | None:
    if not cached or cached.get("id") != reference_id or cached.get("sha256") != sha256:
        return None
    relative_paths = [cached.get("asset_path", ""), *cached.get("frame_paths", {}).values()]
    if relative_paths and all((state_dir / relative).is_file() for relative in relative_paths):
        return cached
    return None


def _write_reference(source: Path, state_dir: Path, metadata: dict, sha256: str) -> dict:
    reference_id = metadata["id"]
    asset_path = Path("assets") / f"{reference_id}.gif"
    frame_dir = Path("frames") / reference_id
    metrics, frames = _decode_metrics(source)
    (state_dir / asset_path).parent.mkdir(parents=True, exist_ok=True)
    (state_dir / frame_dir).mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, state_dir / asset_path)
    frame_paths = {}
    for label in SAMPLE_LABELS:
        relative = frame_dir / f"{label}.png"
        frames[label].save(state_dir / relative, format="PNG")
        frame_paths[label] = relative.as_posix()
    return {
        **metadata,
        **metrics,
        "source_filename": source.name,
        "sha256": sha256,
        "asset_path": asset_path.as_posix(),
        "frame_paths": frame_paths,
    }


def _canonical_source(group: list[tuple[Path, dict | None]], sha256: str) -> tuple[Path, dict]:
    curated_rows = [(path, row) for path, row in group if row and row.get("id")]
    if not curated_rows:
        names = ", ".join(path.name for path, _ in group)
        raise ReferenceIngestionError(f"missing curated metadata for unique GIF: {names} ({sha256[:12]})")
    return min(curated_rows, key=lambda pair: _reference_number(pair[1]["id"]))


def _alias_rows(group: list[tuple[Path, dict | None]], canonical: tuple[Path, dict], sha256: str) -> list[dict]:
    aliases = []
    for path, metadata in group:
        if path == canonical[0]:
            continue
        alias = {
            "source_filename": path.name,
            "sha256": sha256,
            "alias_of": canonical[1]["id"],
            "deprecated": bool(metadata and metadata.get("id")),
        }
        if metadata and metadata.get("id"):
            alias["id"] = metadata["id"]
        aliases.append(alias)
    return aliases


def ingest_library(library: Path, state_dir: Path, curated: dict) -> dict:
    curated_rows = _curated_by_filename(curated)
    groups: dict[str, list[tuple[Path, dict | None]]] = {}
    for source in _gif_paths(library):
        sha256 = _sha256(source)
        groups.setdefault(sha256, []).append((source, curated_rows.get(source.name)))
    cached_manifest = None
    manifest_path = state_dir / "manifest.json"
    if manifest_path.exists():
        try:
            cached_manifest = json.loads(manifest_path.read_text())
        except json.JSONDecodeError as exc:
            raise ReferenceIngestionError(f"invalid cached manifest: {exc}") from exc
    cached_by_sha = {row["sha256"]: row for row in (cached_manifest or {}).get("references", [])}
    references = []
    aliases = []
    for sha256, group in sorted(groups.items()):
        source, metadata = _canonical_source(group, sha256)
        cached = _cached_reference(state_dir, cached_by_sha.get(sha256), metadata["id"], sha256)
        references.append(cached or _write_reference(source, state_dir, metadata, sha256))
        aliases.extend(_alias_rows(group, (source, metadata), sha256))
    references.sort(key=lambda row: _reference_number(row["id"]))
    aliases.sort(key=lambda row: (_reference_number(row["id"]) if row.get("id") else 10**9, row["source_filename"]))
    manifest = {"schema_version": 1, "references": references, "aliases": aliases}
    state_dir.mkdir(parents=True, exist_ok=True)
    temporary = manifest_path.with_suffix(".tmp")
    temporary.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    temporary.replace(manifest_path)
    return manifest


def check_library(state_dir: Path, curated: dict) -> list[str]:
    errors = []
    manifest_path = state_dir / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text())
    except FileNotFoundError:
        return [f"missing manifest: {manifest_path}"]
    except json.JSONDecodeError as exc:
        return [f"invalid manifest JSON: {exc}"]
    canonical_ids = {row["id"] for row in manifest.get("references", [])}
    curated_rows = curated.get("references", []) + curated.get("aliases", [])
    curated_ids = {row["id"] for row in curated_rows if row.get("id")}
    alias_ids = {row["id"] for row in manifest.get("aliases", []) if row.get("id")}
    missing_ids = sorted(curated_ids - canonical_ids - alias_ids)
    if missing_ids:
        errors.append(f"missing curated IDs: {', '.join(missing_ids)}")
    if not canonical_ids:
        errors.append("manifest has no canonical references")
    for reference in manifest.get("references", []):
        asset = state_dir / reference.get("asset_path", "")
        if not asset.is_file():
            errors.append(f"{reference['id']}: missing cached asset")
        elif _sha256(asset) != reference.get("sha256"):
            errors.append(f"{reference['id']}: cached asset SHA mismatch")
        for label in SAMPLE_LABELS:
            frame = state_dir / reference.get("frame_paths", {}).get(label, "")
            if not frame.is_file():
                errors.append(f"{reference['id']}: missing {label} frame")
    return errors


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    ingest = commands.add_parser("ingest", help="ingest GIF references")
    ingest.add_argument("--library", type=Path, required=True)
    ingest.add_argument("--state-dir", type=Path, default=DEFAULT_STATE)
    ingest.add_argument("--curated", type=Path, default=DEFAULT_CURATED)
    check = commands.add_parser("check", help="validate cached reference state")
    check.add_argument("--state-dir", type=Path, default=DEFAULT_STATE)
    check.add_argument("--curated", type=Path, default=DEFAULT_CURATED)
    return parser


def main(argv=None) -> int:
    args = _parser().parse_args(argv)
    curated = load_reference_library(args.curated)
    if args.command == "ingest":
        manifest = ingest_library(args.library, args.state_dir, curated)
        print(f"Reference ingest: {len(manifest['references'])} canonical, {len(manifest['aliases'])} aliases")
        return 0
    errors = check_library(args.state_dir, curated)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Reference library: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
