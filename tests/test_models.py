from app.models import TranscribeRequest


def test_request_defaults():
    req = TranscribeRequest(url="https://example.com/video")
    assert req.model_size == "small"
    assert req.word_timestamps is True
