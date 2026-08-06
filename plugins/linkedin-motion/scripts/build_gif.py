#!/usr/bin/env python3
"""
build_gif.py — assemble captured PNG frames into a LinkedIn-ready looping GIF.

Runs a two-pass ffmpeg palette (palettegen -> paletteuse), then walks a ladder of
quality reductions until the file fits the size budget. Every attempt is printed
so you can see exactly what was traded away.

Also reports the pixel delta between the first and last frame, which is the
fastest way to catch a loop that does not close.

Usage:
    python3 build_gif.py frames/ --out post.gif --fps 12.5 --max-mb 5
    python3 build_gif.py frames/ --out post.gif --fps 30 --max-mb 5 --colors 96
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def require(binary):
    if shutil.which(binary) is None:
        sys.exit(f"{binary} not found on PATH. Run: bash scripts/setup.sh")


def loop_delta(frames_dir, sample=64):
    """Check whether the loop closes.

    Comparing frame 0 to the last frame on its own is misleading. The last frame
    sits one step *before* the loop point, so it is legitimately different from
    frame 0 by one step of motion. And on a stepped animation, "one step" can be
    a large visual change that happens at several points in the loop anyway.

    So the baseline is the LARGEST change between any two consecutive frames in
    the loop. If the seam (last -> first) is no bigger than that, the seam is
    indistinguishable from any other frame boundary, which is exactly what a
    clean loop means.

    Also returns the mean change per frame, which is the real motion budget metric.
    See references/animation-recipes.md, "Motion budget: measure changed pixels".

    Returns (max_step_pct, mean_step_pct, seam_pct, ratio) or None.
    """
    files = sorted(frames_dir.glob("f*.png"))
    if len(files) < 3:
        return None
    try:
        from PIL import Image, ImageChops
    except ImportError:
        return None

    # Downscale for speed; relative comparison is unaffected.
    def load(path):
        im = Image.open(path).convert("RGB")
        im.thumbnail((360, 450), Image.BILINEAR)
        return im

    ims = [load(f) for f in files]
    w, h = ims[0].size
    npx = w * h

    def pct(a, b):
        hist = ImageChops.difference(a, b).convert("L").histogram()
        return 100.0 * sum(hist[13:]) / npx

    steps = [pct(ims[i], ims[i + 1]) for i in range(len(ims) - 1)]
    max_step = max(steps)
    mean_step = sum(steps) / len(steps)
    seam = pct(ims[-1], ims[0])
    ratio = seam / max_step if max_step > 0.01 else (0.0 if seam < 0.01 else 999.0)
    return max_step, mean_step, seam, ratio


def encode(frames_dir, out, fps, colors, scale, dither):
    """Two-pass palette encode. Returns file size in bytes."""
    pattern = str(frames_dir / "f%04d.png")
    palette = frames_dir / "_palette.png"

    vf_scale = f"scale={scale}:-1:flags=lanczos," if scale else ""

    p1 = run([
        "ffmpeg", "-y", "-v", "error",
        "-framerate", str(fps), "-i", pattern,
        "-vf", f"{vf_scale}palettegen=max_colors={colors}:stats_mode=diff",
        str(palette),
    ])
    if p1.returncode != 0:
        sys.exit("palettegen failed:\n" + p1.stderr)

    p2 = run([
        "ffmpeg", "-y", "-v", "error",
        "-framerate", str(fps), "-i", pattern,
        "-i", str(palette),
        "-lavfi", f"{vf_scale}paletteuse=dither={dither}:diff_mode=rectangle",
        "-loop", "0",
        str(out),
    ])
    if p2.returncode != 0:
        sys.exit("paletteuse failed:\n" + p2.stderr)

    palette.unlink(missing_ok=True)
    return Path(out).stat().st_size


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("frames", help="directory of f0000.png frames")
    ap.add_argument("--out", default="post.gif")
    ap.add_argument("--fps", type=float, default=None,
                    help="defaults to the fps recorded in capture.json")
    ap.add_argument("--max-mb", type=float, default=5.0, help="size budget")
    ap.add_argument("--colors", type=int, default=128, help="starting palette size")
    ap.add_argument("--dither", default="bayer:bayer_scale=4",
                    help="bayer:bayer_scale=N (flat art) or sierra2_4a (photos)")
    ap.add_argument("--no-ladder", action="store_true",
                    help="do a single encode and stop, even if oversized")
    args = ap.parse_args()

    require("ffmpeg")

    frames_dir = Path(args.frames)
    if not frames_dir.is_dir():
        sys.exit(f"No such directory: {frames_dir}")

    fps = args.fps
    meta_path = frames_dir / "capture.json"
    if fps is None and meta_path.exists():
        fps = json.loads(meta_path.read_text())["fps"]
    if fps is None:
        sys.exit("--fps is required when capture.json is absent")

    n = len(list(frames_dir.glob("f*.png")))
    print(f"frames   : {n} @ {fps} fps ({n / fps:.2f}s)")

    d = loop_delta(frames_dir)
    if d is not None:
        max_step, mean_step, seam, ratio = d
        if mean_step < 0.5:
            m = "cheap, room to add motion"
        elif mean_step < 2.0:
            m = "healthy"
        elif mean_step < 5.0:
            m = "high — only viable on a dark flat ground"
        else:
            m = "TOO HIGH — something full-bleed is animating"
        print(f"motion   : {mean_step:.2f}% of pixels change per frame — {m}")
        if ratio <= 1.25:
            verdict = "closes cleanly"
        elif ratio <= 2.0:
            verdict = "CHECK — watch the seam"
        else:
            verdict = "DOES NOT CLOSE — see animation-recipes.md"
        print(f"loop     : biggest frame-to-frame change {max_step:.2f}%, "
              f"seam {seam:.2f}% (x{ratio:.2f}) — {verdict}")

    budget = args.max_mb * 1024 * 1024
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    # Reduction ladder. Palette first (invisible on flat art), then frame rate,
    # then resolution. Resolution last because it is the only visible loss.
    ladder = [
        (args.colors, None),
        (96, None),
        (64, None),
        (64, 1080),
        (48, 1080),
        (48, 864),
        (32, 864),
        (32, 720),
    ]
    if args.no_ladder:
        ladder = ladder[:1]

    for colors, scale in ladder:
        size = encode(frames_dir, out, fps, colors, scale, args.dither)
        mb = size / 1024 / 1024
        tag = f"{colors} colours" + (f", {scale}px wide" if scale else "")
        status = "FITS" if size <= budget else "over budget"
        print(f"encode   : {tag:<28} {mb:5.2f} MB   {status}")
        if size <= budget:
            print(f"\noutput   : {out}  ({mb:.2f} MB)")
            if scale:
                print("  Note: the image was downscaled to fit. Consider cutting the "
                      "moving area or the frame rate instead, and re-rendering.")
            return

    print("\nStill over budget after the full ladder. The moving area is too large.")
    print("Read references/animation-recipes.md, section 'Motion budget'.")
    sys.exit(1)


if __name__ == "__main__":
    main()
