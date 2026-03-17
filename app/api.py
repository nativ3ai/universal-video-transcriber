from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse

from app.models import TranscribeRequest
from app.pipeline import transcribe_url

app = FastAPI(title="Universal Video Transcriber", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/transcribe", response_class=ORJSONResponse)
def transcribe(req: TranscribeRequest):
    try:
        result = transcribe_url(
            url=str(req.url),
            language=req.language,
            model_size=req.model_size,
            word_timestamps=req.word_timestamps,
            persist_media=req.persist_media,
        )
        return result.model_dump()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
