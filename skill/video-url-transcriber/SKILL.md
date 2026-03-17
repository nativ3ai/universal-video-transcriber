---
name: video-url-transcriber
description: Transcribe a video/audio URL into timestamped JSON using yt-dlp + ffmpeg + faster-whisper. Use when an agent needs platform-agnostic URL-to-transcript ingestion for downstream analysis.
---

# Video URL Transcriber Skill

Use this skill when a user asks for transcript extraction from a public media URL (YouTube, X, and any site supported by yt-dlp).

## Preconditions

Install system deps:

```bash
brew install ffmpeg yt-dlp
```

Install Python deps from repo root:

```bash
pip install -r requirements.txt
```

## Minimal workflow

1. Run dependency check:

```bash
python3 skill/video-url-transcriber/scripts/transcribe_url.py --doctor
```

2. Run one-shot URL transcription:

```bash
python3 skill/video-url-transcriber/scripts/transcribe_url.py "https://www.youtube.com/watch?v=..." --model-size small
```

3. Return JSON output with:
- `source_url`
- `platform`
- `title`
- `duration_sec`
- `language`
- `transcript`
- `segments[]` with timestamps and optional words

## API mode (agent workers)

Start API service:

```bash
python3 skill/video-url-transcriber/scripts/run_api.py
```

Transcribe request:

```bash
curl -s http://127.0.0.1:8099/transcribe \
  -H 'content-type: application/json' \
  -d '{
    "url": "https://www.youtube.com/watch?v=...",
    "language": null,
    "model_size": "small",
    "word_timestamps": true,
    "persist_media": false
  }'
```

## Optional auth-gated media

If URL requires a logged-in browser session, pass browser cookies:

```bash
python3 skill/video-url-transcriber/scripts/transcribe_url.py "<url>" --cookies-from-browser chrome
```

## Execution rules

- Always normalize audio to mono 16k WAV before ASR.
- Default `model_size` is `small`; raise to `medium`/`large-v3` only when user asks for higher quality.
- Prefer `persist_media=false` unless user explicitly wants artifacts retained.
- If transcription fails, return exact failing stage: `fetch`, `ffmpeg normalize`, or `asr`.
