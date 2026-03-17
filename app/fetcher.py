from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

import yt_dlp


def extract_media_info(url: str, cookies_from_browser: str | None = None) -> dict[str, Any]:
    opts: dict[str, Any] = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "noplaylist": True,
    }
    if cookies_from_browser:
        opts["cookiesfrombrowser"] = (cookies_from_browser,)

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return {
        "id": info.get("id"),
        "title": info.get("title") or "untitled",
        "duration": info.get("duration"),
        "extractor_key": info.get("extractor_key") or info.get("extractor") or "unknown",
        "webpage_url": info.get("webpage_url") or url,
    }


def download_media(url: str, cookies_from_browser: str | None = None) -> Path:
    tmpdir = Path(tempfile.mkdtemp(prefix="uvt_media_"))
    outtmpl = str(tmpdir / "source.%(ext)s")

    opts: dict[str, Any] = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "restrictfilenames": True,
    }
    if cookies_from_browser:
        opts["cookiesfrombrowser"] = (cookies_from_browser,)

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return Path(filename)
