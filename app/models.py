from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class TranscribeRequest(BaseModel):
    url: HttpUrl
    language: str | None = None
    model_size: str = "small"
    diarize: bool = False
    word_timestamps: bool = True
    persist_media: bool = False


class WordTimestamp(BaseModel):
    word: str
    start: float | None = None
    end: float | None = None


class Segment(BaseModel):
    id: int
    start: float
    end: float
    text: str
    speaker: str | None = None
    words: list[WordTimestamp] = Field(default_factory=list)


class TranscribeResponse(BaseModel):
    source_url: str
    platform: str
    title: str
    duration_sec: float | None = None
    language: str | None = None
    transcript: str
    segments: list[Segment]
    metadata: dict[str, Any] = Field(default_factory=dict)
    status: str = "completed"
