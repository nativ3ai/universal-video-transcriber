from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


def normalize_audio_to_wav16k(source_path: Path) -> Path:
    outdir = Path(tempfile.mkdtemp(prefix="uvt_audio_"))
    outpath = outdir / "audio_16k_mono.wav"

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(source_path),
        "-ac",
        "1",
        "-ar",
        "16000",
        "-f",
        "wav",
        str(outpath),
    ]
    subprocess.run(cmd, check=True)
    return outpath
