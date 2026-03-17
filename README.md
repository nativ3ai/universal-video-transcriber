# Universal Video Transcriber

Platform-agnostic URL -> transcript JSON pipeline:

`URL -> yt-dlp fetch -> ffmpeg normalize -> faster-whisper ASR -> timestamped JSON`

Supports any site resolvable by `yt-dlp`.

## Install

```bash
brew install ffmpeg yt-dlp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Quick use (CLI)

```bash
python3 skill/video-url-transcriber/scripts/transcribe_url.py --doctor
python3 skill/video-url-transcriber/scripts/transcribe_url.py "https://www.youtube.com/watch?v=..." --model-size small
```

## API use

```bash
python3 skill/video-url-transcriber/scripts/run_api.py
```

Example call:

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

## JSON response shape

```json
{
  "source_url": "https://x.com/.../video/1",
  "platform": "x",
  "title": "Example video",
  "duration_sec": 812.4,
  "language": "en",
  "transcript": "Full concatenated text...",
  "segments": [
    {
      "id": 0,
      "start": 0.0,
      "end": 4.7,
      "text": "Opening statement...",
      "speaker": null,
      "words": [
        {"word": "Opening", "start": 0.0, "end": 0.4}
      ]
    }
  ],
  "metadata": {
    "extractor_key": "Youtube",
    "video_id": "abc123",
    "model_size": "small"
  },
  "status": "completed"
}
```

## Notes

- Not truly universal forever; it works for platforms currently supported by `yt-dlp`.
- For auth-gated URLs, use `--cookies-from-browser chrome|firefox|safari`.
- For higher quality, switch model size to `medium` or `large-v3`.
