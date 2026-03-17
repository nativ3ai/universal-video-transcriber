from __future__ import annotations

import shutil
from pathlib import Path

from app.asr import ASREngine
from app.fetcher import download_media, extract_media_info
from app.media import normalize_audio_to_wav16k
from app.models import Segment, TranscribeResponse, WordTimestamp


def _platform_from_extractor(extractor_key: str) -> str:
    key = (extractor_key or "unknown").lower()
    if "youtube" in key:
        return "youtube"
    if "twitter" in key or "x" == key:
        return "x"
    return key


def transcribe_url(
    url: str,
    language: str | None = None,
    model_size: str = "small",
    word_timestamps: bool = True,
    persist_media: bool = False,
    cookies_from_browser: str | None = None,
) -> TranscribeResponse:
    info = extract_media_info(url, cookies_from_browser=cookies_from_browser)
    media_path = download_media(url, cookies_from_browser=cookies_from_browser)

    audio_path = None
    try:
        audio_path = normalize_audio_to_wav16k(media_path)
        engine = ASREngine(model_size=model_size)
        asr_result = engine.transcribe(
            str(audio_path),
            language=language,
            word_timestamps=word_timestamps,
        )

        segments = []
        for seg in asr_result["segments"]:
            words = [WordTimestamp(**w) for w in seg.get("words", [])]
            segments.append(Segment(**{**seg, "words": words}))

        return TranscribeResponse(
            source_url=info.get("webpage_url") or url,
            platform=_platform_from_extractor(info.get("extractor_key") or "unknown"),
            title=info.get("title") or "untitled",
            duration_sec=info.get("duration"),
            language=asr_result.get("language"),
            transcript=asr_result.get("transcript", ""),
            segments=segments,
            metadata={
                "extractor_key": info.get("extractor_key"),
                "video_id": info.get("id"),
                "model_size": model_size,
            },
            status="completed",
        )
    finally:
        if not persist_media:
            if media_path.exists():
                shutil.rmtree(media_path.parent, ignore_errors=True)
            if audio_path and Path(audio_path).exists():
                shutil.rmtree(Path(audio_path).parent, ignore_errors=True)
