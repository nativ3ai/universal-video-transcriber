#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def _inject_repo_root() -> None:
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / "app" / "pipeline.py").exists():
            sys.path.insert(0, str(parent))
            return


_inject_repo_root()


def check_dependency(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def run_doctor() -> int:
    checks = [
        ("python3", check_dependency("python3")),
        ("ffmpeg", check_dependency("ffmpeg")),
        ("yt-dlp", check_dependency("yt-dlp")),
    ]
    if not checks[2][1]:
        try:
            import yt_dlp  # noqa: F401

            checks[2] = ("yt-dlp", True)
        except Exception:
            pass
    for name, ok in checks:
        print(f"{'OK ' if ok else 'MISS'} {name}")

    missing = [name for name, ok in checks if not ok]
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}", file=sys.stderr)
        return 1

    try:
        import faster_whisper  # noqa: F401
        print("OK  faster-whisper")
    except Exception as exc:
        print(f"MISS faster-whisper ({exc})", file=sys.stderr)
        return 1

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="URL -> transcript JSON")
    parser.add_argument("url", nargs="?", default="")
    parser.add_argument("--language", default=None)
    parser.add_argument("--model-size", default="small")
    parser.add_argument("--no-word-timestamps", action="store_true")
    parser.add_argument("--persist-media", action="store_true")
    parser.add_argument("--cookies-from-browser", default=None)
    parser.add_argument("--doctor", action="store_true")

    args = parser.parse_args()

    if args.doctor:
        return run_doctor()

    if not args.url:
        parser.error("url is required unless --doctor is used")

    try:
        from app.pipeline import transcribe_url

        result = transcribe_url(
            url=args.url,
            language=args.language,
            model_size=args.model_size,
            word_timestamps=not args.no_word_timestamps,
            persist_media=args.persist_media,
            cookies_from_browser=args.cookies_from_browser,
        )
        print(json.dumps(result.model_dump(), indent=2, ensure_ascii=True))
        return 0
    except subprocess.CalledProcessError as exc:
        print(f"ffmpeg/yt-dlp process failed: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"transcription failed: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
