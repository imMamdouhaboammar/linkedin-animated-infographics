#!/usr/bin/env python3
import argparse
import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "skills" / "info-stories" / "catalog.json"
DEFAULT_EXTENSIONS = ROOT / "skills" / "info-stories" / "extensions"
DEFAULT_REFERENCE_LIBRARY = ROOT / "research" / "reference-studies" / "visual-library.json"
AXIS_ALIASES = {
    "house": "houses",
    "style": "styles",
    "archetype": "archetypes",
    "motion": "motions",
    "mechanism": "mechanisms",
}
HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REFERENCE_ID_RE = re.compile(r"^REF-(?:00[1-9]|0[1-2][0-9]|03[0-5])$")
MECHANISM_CAP = 150
MECHANISM_FIELDS = {
    "slug", "name", "origin", "story_jobs", "content_shapes", "compatibility",
    "hook", "beats", "palette_roles", "layout", "hierarchy", "typography",
    "motion", "loop", "constraints", "anti_patterns", "implementation_hints",
    "reference_ids", "influence_axes", "originality",
}
MECHANISM_NESTED_FIELDS = {
    "layout": ("topology", "zones", "proportions", "negative_space"),
    "hierarchy": ("primary", "secondary", "reading_order"),
    "typography": ("classes", "roles", "language_policy"),
    "motion": ("job", "target", "sequence", "timing_family", "static_regions"),
    "loop": ("strategy", "hold", "reset"),
    "originality": ("adopt", "reject"),
}
RANK_WEIGHTS = {"story_jobs": 8, "content_shapes": 5, "reference_ids": 3}
REQUIRED_QUERY_FIELDS = ("story_jobs", "output_mode", "language", "density", "evidence_mode")
CAPSULE_FIELDS = {
    "concept": ("story_jobs", "hook", "originality"),
    "story": ("beats", "content_shapes", "compatibility", "originality"),
    "palette-type": ("palette_roles", "typography"),
    "layout": ("layout", "hierarchy", "constraints", "implementation_hints"),
    "motion": ("motion", "loop", "constraints", "implementation_hints"),
    "review": ("reference_ids", "originality", "anti_patterns"),
}


def load_catalog(path=DEFAULT_CATALOG, extensions_dir=None):
    path = Path(path)
    catalog = json.loads(path.read_text())
    is_default = path.resolve() == DEFAULT_CATALOG.resolve()
    if extensions_dir is None and is_default:
        extensions_dir = DEFAULT_EXTENSIONS
    if extensions_dir:
        extension_root = Path(extensions_dir)
        if extension_root.exists():
            for extension in sorted(extension_root.glob("*.json")):
                payload = json.loads(extension.read_text())
                for axis in ("houses", "styles", "archetypes", "motions", "mechanisms"):
                    catalog.setdefault(axis, []).extend(payload.get(axis, []))
    if len(catalog.get("mechanisms", [])) > MECHANISM_CAP:
        raise ValueError(f"mechanisms: maximum {MECHANISM_CAP} entries")
    if is_default and DEFAULT_REFERENCE_LIBRARY.exists():
        library = json.loads(DEFAULT_REFERENCE_LIBRARY.read_text())
        catalog["references"] = library.get("references", [])
    return catalog


def _non_empty_list(row, field):
    return isinstance(row.get(field), list) and bool(row[field])


def _mechanism_fingerprint(row):
    layout = row.get("layout", {})
    hierarchy = row.get("hierarchy", {})
    typography = row.get("typography", {})
    motion = row.get("motion", {})
    loop = row.get("loop", {})
    return json.dumps(
        [
            layout.get("topology"), layout.get("zones"), layout.get("proportions"),
            hierarchy.get("primary"), hierarchy.get("reading_order"), typography.get("classes"),
            motion.get("job"), motion.get("target"), motion.get("sequence"), loop.get("strategy"),
        ],
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def validate_mechanisms(catalog):
    mechanisms = catalog.get("mechanisms")
    if not isinstance(mechanisms, list):
        return ["mechanisms: expected list"]
    errors = []
    if len(mechanisms) > MECHANISM_CAP:
        errors.append(f"mechanisms: maximum {MECHANISM_CAP} entries")
    known_references = {row.get("id") for row in catalog.get("references", []) if row.get("id")}
    slugs = set()
    fingerprints = {}
    for index, row in enumerate(mechanisms):
        if not isinstance(row, dict):
            errors.append(f"mechanisms[{index}]: expected object")
            continue
        slug = row.get("slug", f"mechanisms[{index}]")
        missing = sorted(field for field in MECHANISM_FIELDS if row.get(field) in (None, "", [], {}))
        if missing:
            errors.append(f"{slug}: missing {', '.join(missing)}")
        if not isinstance(row.get("slug"), str) or not SLUG_RE.match(row["slug"]):
            errors.append(f"mechanisms: invalid slug {row.get('slug')!r}")
        elif row["slug"] in slugs:
            errors.append(f"mechanisms: duplicate slug {row['slug']}")
        slugs.add(row.get("slug"))
        if row.get("origin") not in {"extracted", "new"}:
            errors.append(f"{slug}: origin must be extracted or new")
        for field in (
            "story_jobs", "content_shapes", "beats", "palette_roles", "constraints",
            "anti_patterns", "implementation_hints",
        ):
            if not _non_empty_list(row, field):
                errors.append(f"{slug}: {field} must be a non-empty list")
        compatibility = row.get("compatibility", {})
        for field in (
            "output_modes", "languages", "densities", "evidence_modes",
            "styles", "archetypes", "motions",
        ):
            if not _non_empty_list(compatibility, field):
                errors.append(f"{slug}: compatibility.{field} must be a non-empty list")
        for compatibility_field, catalog_axis in (
            ("styles", "styles"), ("archetypes", "archetypes"), ("motions", "motions"),
        ):
            known_slugs = {candidate.get("slug") for candidate in catalog.get(catalog_axis, [])}
            if known_slugs and isinstance(compatibility.get(compatibility_field), list):
                for unknown in sorted(set(compatibility[compatibility_field]) - known_slugs):
                    errors.append(f"{slug}: unknown compatible {catalog_axis[:-1]} {unknown}")
        for parent, fields in MECHANISM_NESTED_FIELDS.items():
            nested = row.get(parent, {})
            for field in fields:
                if not isinstance(nested, dict) or nested.get(field) in (None, "", [], {}):
                    errors.append(f"{slug}: {parent}.{field} must be non-empty")
        reference_ids = row.get("reference_ids", [])
        for reference_id in reference_ids if isinstance(reference_ids, list) else []:
            reference_known = (
                reference_id in known_references
                if known_references
                else isinstance(reference_id, str) and REFERENCE_ID_RE.fullmatch(reference_id)
            )
            if not reference_known:
                errors.append(f"{slug}: unknown reference {reference_id}")
        influence_axes = row.get("influence_axes", {})
        if isinstance(reference_ids, list) and set(influence_axes) != set(reference_ids):
            errors.append(f"{slug}: influence_axes must match reference_ids")
        for reference_id, axes in influence_axes.items() if isinstance(influence_axes, dict) else []:
            if not axes or not set(axes).issubset({"structure", "motion", "typography"}):
                errors.append(f"{slug}: invalid influence axes for {reference_id}")
        fingerprint = _mechanism_fingerprint(row)
        if fingerprint in fingerprints:
            errors.append(f"{slug}: duplicate fingerprint with {fingerprints[fingerprint]}")
        else:
            fingerprints[fingerprint] = slug
    return errors


def _query_values(query, field):
    values = query.get(field, [])
    if isinstance(values, str):
        return [values]
    if not isinstance(values, list):
        raise ValueError(f"{field} must be a string or list")
    return values


def _overlap(left, right):
    return sorted(set(left).intersection(right))


def _requested_content_shapes(query):
    if "content_shapes" in query:
        return _query_values(query, "content_shapes")
    return _query_values(query, "content_shape")


def _validate_retrieval_query(query):
    if not isinstance(query, dict):
        raise ValueError("query must be an object")
    missing = [field for field in REQUIRED_QUERY_FIELDS if query.get(field) in (None, "", [])]
    if "content_shape" not in query and "content_shapes" not in query:
        missing.append("content_shape")
    if missing:
        raise ValueError(f"query missing {', '.join(missing)}")


def _compatible(mechanism, query):
    compatibility = mechanism["compatibility"]
    hard_fields = {
        "output_mode": "output_modes",
        "language": "languages",
        "density": "densities",
        "evidence_mode": "evidence_modes",
    }
    for query_field, compatibility_field in hard_fields.items():
        requested = query.get(query_field)
        allowed = compatibility[compatibility_field]
        if requested and requested not in allowed and "*" not in allowed:
            return False
    requested_shapes = _requested_content_shapes(query)
    return not requested_shapes or bool(_overlap(requested_shapes, mechanism["content_shapes"]))


def rank_mechanisms(catalog, query):
    _validate_retrieval_query(query)
    top_k = query.get("top_k", 5)
    if not isinstance(top_k, int) or not 1 <= top_k <= MECHANISM_CAP:
        raise ValueError(f"top_k must be an integer from 1 to {MECHANISM_CAP}")
    ranked = []
    query_axes = {
        "story_jobs": _query_values(query, "story_jobs"),
        "content_shapes": _requested_content_shapes(query),
        "reference_ids": _query_values(query, "reference_ids"),
    }
    for mechanism in catalog.get("mechanisms", []):
        if not _compatible(mechanism, query):
            continue
        reasons = []
        score = 0
        for axis, requested in query_axes.items():
            matches = _overlap(requested, mechanism[axis])
            if matches:
                points = len(matches) * RANK_WEIGHTS[axis]
                reasons.append({
                    "axis": axis,
                    "matches": matches,
                    "weight": RANK_WEIGHTS[axis],
                    "points": points,
                })
                score += points
        ranked.append({"slug": mechanism["slug"], "score": score, "score_reasons": reasons})
    return sorted(ranked, key=lambda row: (-row["score"], row["slug"]))[:top_k]


def _selected_references(mechanisms):
    selected = []
    used = set()
    for axis in ("structure", "motion", "typography"):
        for mechanism in mechanisms:
            reference_id = next(
                (
                    candidate for candidate in mechanism["reference_ids"]
                    if candidate not in used and axis in mechanism["influence_axes"].get(candidate, [])
                ),
                None,
            )
            if reference_id:
                selected.append({
                    "id": reference_id,
                    "role": "primary" if axis == "structure" else "secondary",
                    "influence_axis": axis,
                })
                used.add(reference_id)
                break
    return selected


def _capsule_bytes(capsule):
    return len(
        json.dumps(capsule, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )


def _project_mechanism(mechanism, ranked_row, stage):
    projection = {
        "slug": mechanism["slug"],
        "name": mechanism["name"],
        "score": ranked_row["score"],
        "score_reasons": ranked_row["score_reasons"],
    }
    projection.update({field: mechanism[field] for field in CAPSULE_FIELDS[stage]})
    return projection


def build_context_capsule(catalog, ranked, stage, byte_budget):
    if stage not in CAPSULE_FIELDS:
        raise ValueError(f"stage must be one of {', '.join(CAPSULE_FIELDS)}")
    if not isinstance(byte_budget, int) or byte_budget < 1:
        raise ValueError("byte_budget must be a positive integer")
    mechanisms_by_slug = {row["slug"]: row for row in catalog.get("mechanisms", [])}
    included_rows = []
    included_mechanisms = []
    capsule = {"schema_version": 1, "stage": stage, "mechanisms": [], "references": [], "omitted_mechanisms": len(ranked)}
    for ranked_row in ranked:
        mechanism = mechanisms_by_slug[ranked_row["slug"]]
        candidate_rows = included_rows + [_project_mechanism(mechanism, ranked_row, stage)]
        candidate_mechanisms = included_mechanisms + [mechanism]
        candidate = {
            "schema_version": 1,
            "stage": stage,
            "mechanisms": candidate_rows,
            "references": _selected_references(candidate_mechanisms),
            "omitted_mechanisms": len(ranked) - len(candidate_rows),
        }
        if _capsule_bytes(candidate) > byte_budget:
            break
        capsule = candidate
        included_rows = candidate_rows
        included_mechanisms = candidate_mechanisms
    if ranked and not included_rows:
        raise ValueError(f"byte_budget {byte_budget} is too small for one {stage} mechanism")
    if _capsule_bytes(capsule) > byte_budget:
        raise ValueError(f"byte_budget {byte_budget} is too small for an empty {stage} capsule")
    return capsule


def _linear(channel):
    channel /= 255.0
    return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4


def _luminance(hex_color):
    if not HEX_RE.match(hex_color):
        raise ValueError(f"Expected #RRGGBB, got {hex_color!r}")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * _linear(r) + 0.7152 * _linear(g) + 0.0722 * _linear(b)


def contrast_ratio(foreground, background):
    a, b = _luminance(foreground), _luminance(background)
    lighter, darker = max(a, b), min(a, b)
    return (lighter + 0.05) / (darker + 0.05)


def validate_catalog(catalog):
    errors = []
    for axis in ("houses", "styles", "archetypes", "motions"):
        items = catalog.get(axis)
        if not isinstance(items, list):
            errors.append(f"{axis}: expected list")
            continue
        slugs, names = set(), set()
        for item in items:
            slug, name = item.get("slug"), item.get("name")
            if not slug or not SLUG_RE.match(slug):
                errors.append(f"{axis}: invalid slug {slug!r}")
            if slug in slugs:
                errors.append(f"{axis}: duplicate slug {slug}")
            if name in names:
                errors.append(f"{axis}: duplicate name {name}")
            slugs.add(slug)
            names.add(name)
    required_dials = {"design_variance", "motion_intensity", "visual_density"}
    for style in catalog.get("styles", []):
        dials = style.get("dials", {})
        if set(dials) != required_dials:
            errors.append(f"{style.get('slug')}: expected design dials {sorted(required_dials)}")
        else:
            for name, value in dials.items():
                if not isinstance(value, int) or not 1 <= value <= 10:
                    errors.append(f"{style.get('slug')}: {name} must be integer 1-10")
    required = {"bg", "surface", "ink", "ink_2", "muted", "line", "accent", "accent_deep"}
    for house in catalog.get("houses", []):
        tokens = house.get("tokens", {})
        missing = sorted(required - set(tokens))
        if missing:
            errors.append(f"{house.get('slug')}: missing tokens {', '.join(missing)}")
            continue
        for fg, bg in house.get("text_pairs", []):
            try:
                ratio = contrast_ratio(tokens[fg], tokens[bg])
            except (KeyError, ValueError) as exc:
                errors.append(f"{house['slug']}: invalid text pair {fg}/{bg}: {exc}")
                continue
            if ratio < 4.5:
                errors.append(f"{house['slug']}: text {fg}/{bg} contrast {ratio:.2f} < 4.5")
        for fg, bg in house.get("state_pairs", []):
            try:
                ratio = contrast_ratio(tokens[fg], tokens[bg])
            except (KeyError, ValueError) as exc:
                errors.append(f"{house['slug']}: invalid state pair {fg}/{bg}: {exc}")
                continue
            if ratio < 3.0:
                errors.append(f"{house['slug']}: state {fg}/{bg} contrast {ratio:.2f} < 3.0")
    if "mechanisms" in catalog:
        errors.extend(validate_mechanisms(catalog))
    return errors


def _items_for(catalog, singular):
    axis = AXIS_ALIASES.get(singular, singular)
    if axis not in catalog:
        raise KeyError(singular)
    return catalog[axis]


def _find(catalog, singular, slug):
    items = _items_for(catalog, singular)
    for item in items:
        if item["slug"] == slug:
            return item
    slugs = [item["slug"] for item in items]
    choices = ", ".join(slugs)
    match = difflib.get_close_matches(slug, slugs, n=1, cutoff=0.6)
    hint = f" Did you mean {match[0]!r}?" if match else ""
    raise ValueError(f"Unknown {singular} {slug!r}.{hint} Valid choices: {choices}")


COPY_SLOP_PATTERNS = [
    ("throat-clearing", re.compile(r"\b(here(?:'|’)s the thing|let(?:'|’)s be clear|the truth is|it(?:'|’)s important to note)\b", re.I)),
    ("binary-contrast", re.compile(r"\bnot\s+(?:just\s+|only\s+)?[^.!?]{1,120}?,\s*(?:but\s+)?it(?:'|’)s\b", re.I)),
    ("faux-insight", re.compile(r"\b(what most people get wrong|the real lesson|the deeper truth|here(?:'|’)s what nobody tells you)\b", re.I)),
    ("importance-puffery", re.compile(r"\b(revolution(?:ary)?|game[- ]changing|groundbreaking|changes everything|transformative)\b", re.I)),
    ("recap-ending", re.compile(r"\b(in conclusion|to sum up|in summary)\b", re.I)),
    ("rhetorical-setup", re.compile(r"(?:^|[.!?]\s+)(?:so,?\s+)?(?:what if|why does this matter|ready to|the question is)\b", re.I)),
    ("dash-crutch", re.compile(r"[—–]")),
]

FINGERPRINT_AXES = (
    "zone_topology",
    "card_grammar",
    "divider",
    "visual_anchor",
    "density",
    "motion_grammar",
)


def detect_copy_slop(text):
    findings = []
    for name, pattern in COPY_SLOP_PATTERNS:
        match = pattern.search(text)
        if match:
            findings.append({"pattern": name, "evidence": match.group(0)})
    return findings


def validate_fingerprint(current, previous=None, min_changes=2):
    missing = [axis for axis in FINGERPRINT_AXES if not current.get(axis)]
    if missing:
        return [f"Structural fingerprint is missing: {', '.join(missing)}"]
    if not previous:
        return []
    changed = sum(current.get(axis) != previous.get(axis) for axis in FINGERPRINT_AXES)
    if changed < min_changes:
        return [
            f"Structural fingerprint changes only {changed}/{len(FINGERPRINT_AXES)} axes; "
            f"change at least {min_changes}. A palette-only reskin is not a new visual style."
        ]
    return []


STUDY_REQUIRED_FIELDS = (
    "source", "source_kind", "provenance", "surface", "type_roles", "structure",
    "rhythm", "motion", "visual_anchor", "recommendations", "copy_boundaries",
)
QUALITY_AXES = ("Purpose", "Hierarchy", "Execution", "Specificity", "Restraint", "Variety")
FONT_POLICIES = {"exact-required", "fallback-accepted"}


def validate_study_report(report):
    errors = []
    for field in STUDY_REQUIRED_FIELDS:
        if field not in report or report[field] in (None, "", [], {}):
            errors.append(f"Study report missing {field}")
    if report.get("source_kind") not in {"image", "gif", "url", "user-work", None}:
        errors.append("Study report source_kind must be image, gif, url, or user-work")
    recs = report.get("recommendations", {})
    for axis in ("house", "style", "archetype", "motion"):
        if isinstance(recs, dict) and axis not in recs:
            errors.append(f"Study recommendations missing {axis}")
    errors.extend(validate_study_evidence(report))
    return errors


def validate_study_evidence(report):
    errors = []
    status = report.get("reference_status")
    if status is None:
        return errors
    if status not in {"READY", "HOLD", "SKIP"}:
        return [f"Unknown reference_status: {status!r}"]
    if status in {"HOLD", "SKIP"}:
        if not report.get("status_reason"):
            errors.append(f"{status} requires status_reason")
        return errors
    evidence = report.get("ranked_evidence")
    if not isinstance(evidence, list) or not evidence:
        return ["READY study requires ranked_evidence"]
    try:
        reference_library = json.loads(DEFAULT_REFERENCE_LIBRARY.read_text())
        valid_reference_ids = {
            row["id"] for field in ("references", "aliases")
            for row in reference_library.get(field, []) if row.get("id")
        }
    except (OSError, json.JSONDecodeError, TypeError):
        valid_reference_ids = set()
        errors.append("Canonical reference library is unavailable or invalid")
    seen_ranks = set()
    for index, row in enumerate(evidence):
        if not isinstance(row, dict):
            errors.append(f"ranked_evidence[{index}] must be an object")
            continue
        label = row.get("reference_id") or index
        if not isinstance(row.get("reference_id"), str) or not re.fullmatch(r"REF-\d{3}", row["reference_id"]):
            errors.append(f"Evidence {label}: invalid reference_id")
        elif row["reference_id"] not in valid_reference_ids:
            errors.append(f"Evidence {label}: unknown reference_id")
        rank = row.get("rank")
        if not isinstance(rank, int) or rank < 1 or rank in seen_ranks:
            errors.append(f"Evidence {label}: rank must be a unique positive integer")
        seen_ranks.add(rank)
        if row.get("confidence") not in {"high", "medium", "low"}:
            errors.append(f"Evidence {label}: invalid confidence")
        for field in ("provenance_state", "rights_state"):
            if not row.get(field):
                errors.append(f"Evidence {label}: missing {field}")
        contexts = row.get("focused_contexts")
        if not isinstance(contexts, dict) or not contexts or any(not value for value in contexts.values()):
            errors.append(f"Evidence {label}: focused_contexts must be a non-empty object")
    return errors


def validate_typography_spec(spec):
    roles = spec.get("roles") if isinstance(spec, dict) else None
    if not isinstance(roles, list):
        return ["Typography roles must be a list"]
    errors = []
    seen = set()
    for index, row in enumerate(roles):
        if not isinstance(row, dict):
            errors.append(f"Typography role {index} must be an object")
            continue
        role = row.get("role")
        if role not in {"display", "body", "label", "mono"} or role in seen:
            errors.append(f"Typography role {role!r} is invalid or duplicated")
        seen.add(role)
        for field in ("stack_id", "families"):
            if not row.get(field):
                errors.append(f"Typography role {role or index} missing {field}")
        if not isinstance(row.get("scripts"), list) or not row["scripts"]:
            errors.append(f"Typography role {role or index} requires scripts")
        weights = row.get("weights")
        if not isinstance(weights, list) or not weights or any(not isinstance(weight, int) for weight in weights):
            errors.append(f"Typography role {role or index} requires numeric weights")
        if row.get("font_policy") not in FONT_POLICIES:
            errors.append(f"Typography role {role or index} has invalid font_policy")
    for required in ("display", "body", "label"):
        if required not in seen:
            errors.append(f"Typography missing {required} role")
    return errors


def validate_motion_direction(report):
    if not isinstance(report, dict):
        return ["Motion direction must be an object"]
    output_mode = report.get("output_mode")
    motions = report.get("motions")
    if output_mode not in {"gif", "static"}:
        return ["Motion output_mode must be gif or static"]
    if not isinstance(motions, list):
        return ["Motion motions must be a list"]
    if output_mode == "static" and motions:
        return ["static output must not declare motions"]
    if len(motions) > 2:
        return ["Motion direction allows at most two motions"]
    errors = []
    required = ("communication_job", "target", "sequence", "duration_ms", "easing_family", "hold_ms", "reset", "static_regions")
    for index, row in enumerate(motions):
        if not isinstance(row, dict):
            errors.append(f"Motion {index} must be an object")
            continue
        for field in required:
            if field not in row or row[field] in (None, "", []):
                errors.append(f"Motion {index} missing {field}")
        if not isinstance(row.get("sequence"), list) or not row.get("sequence"):
            errors.append(f"Motion {index} requires sequence")
        if not isinstance(row.get("static_regions"), list) or not row.get("static_regions"):
            errors.append(f"Motion {index} requires static_regions")
        if not isinstance(row.get("duration_ms"), int) or row.get("duration_ms", 0) <= 0:
            errors.append(f"Motion {index} duration_ms must be positive")
        if not isinstance(row.get("hold_ms"), int) or row.get("hold_ms", -1) < 0:
            errors.append(f"Motion {index} hold_ms must be non-negative")
    return errors


def validate_visual_quality_report(report):
    if not isinstance(report, dict):
        return ["Visual quality report must be an object"]
    errors = []
    render = report.get("render_evidence")
    if not isinstance(render, dict) or not render.get("artifact") or not re.fullmatch(r"[0-9a-f]{64}", str(render.get("sha256", ""))):
        errors.append("Visual quality report requires render evidence artifact and SHA-256")
    rows = report.get("axes")
    if not isinstance(rows, list):
        return errors + ["Visual quality axes must be a list"]
    by_axis = {}
    blocking = False
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"Quality axis {index} must be an object")
            continue
        axis = row.get("axis")
        if axis not in QUALITY_AXES:
            errors.append(f"Unknown quality axis {axis!r}")
        if axis in by_axis:
            errors.append(f"Duplicate quality axis {axis}")
        by_axis[axis] = row
        if row.get("applicable") is False:
            if not row.get("reason"):
                errors.append(f"Quality axis {axis or index} requires non-applicable reason")
            continue
        score = row.get("score")
        if not isinstance(score, int) or not 1 <= score <= 5:
            errors.append(f"Quality axis {axis or index} score must be integer 1-5")
        elif score < 3:
            blocking = True
        for field in ("evidence", "finding"):
            if not row.get(field):
                errors.append(f"Quality axis {axis or index} missing {field}")
    for axis in QUALITY_AXES:
        if axis not in by_axis:
            errors.append(f"Missing quality axis {axis}")
    expected = "HOLD" if blocking else "PASS"
    if report.get("verdict") != expected:
        errors.append(f"Visual quality verdict must be {expected}")
    return errors


VERIFIER_VERDICTS = {"PASS", "FAIL:fixable", "FAIL:escalate"}
VERIFIER_STATUSES = {"PASS", "FAIL", "NA"}


def validate_verification_report(report):
    errors = []
    verdict = report.get("verdict")
    if verdict not in VERIFIER_VERDICTS:
        errors.append(f"Unknown verifier verdict: {verdict!r}")
    attempt = report.get("attempt")
    if not isinstance(attempt, int) or attempt < 0:
        errors.append("Verifier attempt must be a non-negative integer")
    elif attempt > 2:
        errors.append("Verification allows at most two targeted fix attempts")
    criteria = report.get("criteria")
    if not isinstance(criteria, list):
        errors.append("Verifier criteria must be a list")
        return errors
    if verdict == "PASS" and not criteria:
        errors.append("PASS requires at least one acceptance criterion with evidence")
    seen = set()
    for index, row in enumerate(criteria):
        if not isinstance(row, dict):
            errors.append(f"Criterion {index} must be an object")
            continue
        criterion_id = row.get("id")
        if not criterion_id:
            errors.append(f"Criterion {index} missing id")
        elif criterion_id in seen:
            errors.append(f"Duplicate criterion id {criterion_id}")
        seen.add(criterion_id)
        if row.get("status") not in VERIFIER_STATUSES:
            errors.append(f"Criterion {criterion_id or index} has invalid status")
        for field in ("artifact", "observation", "evidence"):
            if not row.get(field):
                errors.append(f"Criterion {criterion_id or index} missing {field}")
    return errors


def check_composition(catalog, style, archetype, motions):
    style_item = _find(catalog, "style", style)
    _find(catalog, "archetype", archetype)
    errors = []
    if archetype not in style_item.get("archetypes", []):
        errors.append(f"{style} is not compatible with {archetype}")
    if len(motions) > 2:
        errors.append("Use at most two motion patterns")
    structures = set(style_item.get("structures", []))
    primary_count = 0
    for motion_slug in motions:
        motion = _find(catalog, "motion", motion_slug)
        if not structures.intersection(motion.get("structures", [])):
            errors.append(f"{motion_slug} is not compatible with {style}")
        roles = motion.get("roles", [])
        if roles == ["primary"]:
            primary_count += 1
    if primary_count > 1:
        errors.append("Use at most one primary-only motion pattern")
    return errors


def build_brief(catalog, *, topic, takeaway, cta, house, style, archetype, motions, language="en", output_mode="gif"):
    house_item = _find(catalog, "house", house)
    style_item = _find(catalog, "style", style)
    archetype_item = _find(catalog, "archetype", archetype)
    for motion_slug in motions:
        _find(catalog, "motion", motion_slug)
    if output_mode not in {"gif", "static"}:
        raise ValueError("output_mode must be 'gif' or 'static'")
    if output_mode == "static" and motions:
        raise ValueError("static output must not declare motion patterns")
    errors = check_composition(catalog, style, archetype, motions)
    if errors:
        raise ValueError("; ".join(errors))
    return {
        "schema_version": 1,
        "topic": topic,
        "takeaway": takeaway,
        "cta": cta,
        "language": language,
        "output_mode": output_mode,
        "selection": {
            "house": house,
            "style": style,
            "archetype": archetype,
            "motions": list(motions),
        },
        "content_contract": {
            "required_beats": list(archetype_item["required_beats"]),
            "density_range": list(archetype_item["density_range"]),
        },
        "execution": {
            "artboard_archetype": style_item["preferred_artboard"],
            "structures": list(style_item["structures"]),
            "design_dials": dict(style_item["dials"]),
            "house_tokens": dict(house_item["tokens"]),
            "motion_limit": 2,
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inspect and validate Info-stories registries")
    sub = parser.add_subparsers(dest="command", required=True)
    lp = sub.add_parser("list")
    lp.add_argument("axis", choices=tuple(AXIS_ALIASES))
    sp = sub.add_parser("show")
    sp.add_argument("axis", choices=tuple(AXIS_ALIASES))
    sp.add_argument("slug")
    sub.add_parser("check")
    cp = sub.add_parser("compose")
    cp.add_argument("--style", required=True)
    cp.add_argument("--archetype", required=True)
    cp.add_argument("--motion", action="append", default=[])
    bp = sub.add_parser("scaffold")
    bp.add_argument("--topic", required=True)
    bp.add_argument("--takeaway", required=True)
    bp.add_argument("--cta", required=True)
    bp.add_argument("--house", required=True)
    bp.add_argument("--style", required=True)
    bp.add_argument("--archetype", required=True)
    bp.add_argument("--motion", action="append", default=[])
    bp.add_argument("--language", default="en")
    bp.add_argument("--output-mode", choices=("gif", "static"), default="gif")
    args = parser.parse_args(argv)
    catalog = load_catalog()
    try:
        if args.command == "list":
            for item in _items_for(catalog, args.axis):
                print(f"{item['slug']}\t{item['name']}")
            return 0
        if args.command == "show":
            print(json.dumps(_find(catalog, args.axis, args.slug), indent=2, sort_keys=True))
            return 0
        if args.command == "compose":
            errors = check_composition(catalog, args.style, args.archetype, args.motion)
            if errors:
                for error in errors:
                    print(error, file=sys.stderr)
                return 1
            print("Composition: OK")
            return 0
        if args.command == "scaffold":
            brief = build_brief(
                catalog, topic=args.topic, takeaway=args.takeaway, cta=args.cta,
                house=args.house, style=args.style, archetype=args.archetype,
                motions=args.motion, language=args.language, output_mode=args.output_mode,
            )
            print(json.dumps(brief, indent=2, sort_keys=True))
            return 0
        errors = validate_catalog(catalog)
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 1
        print("Info-stories catalog: OK")
        return 0
    except (KeyError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
