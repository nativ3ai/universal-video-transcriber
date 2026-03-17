from __future__ import annotations

from typing import Any

from faster_whisper import WhisperModel


class ASREngine:
    def __init__(self, model_size: str = "small", compute_type: str = "int8") -> None:
        self.model = WhisperModel(model_size, compute_type=compute_type)

    def transcribe(
        self,
        audio_path: str,
        language: str | None = None,
        word_timestamps: bool = True,
    ) -> dict[str, Any]:
        segments, info = self.model.transcribe(
            audio_path,
            language=language,
            vad_filter=True,
            word_timestamps=word_timestamps,
            beam_size=5,
        )

        normalized_segments: list[dict[str, Any]] = []
        full_text_parts: list[str] = []

        for idx, seg in enumerate(segments):
            words = []
            if word_timestamps and seg.words:
                for w in seg.words:
                    words.append(
                        {
                            "word": w.word,
                            "start": float(w.start) if w.start is not None else None,
                            "end": float(w.end) if w.end is not None else None,
                        }
                    )
            text = seg.text.strip()
            if text:
                full_text_parts.append(text)

            normalized_segments.append(
                {
                    "id": idx,
                    "start": float(seg.start),
                    "end": float(seg.end),
                    "text": text,
                    "speaker": None,
                    "words": words,
                }
            )

        return {
            "language": getattr(info, "language", None),
            "segments": normalized_segments,
            "transcript": " ".join(full_text_parts).strip(),
        }
