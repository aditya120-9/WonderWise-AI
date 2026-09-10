from app.security.rate_limit import allow_request


def test_rate_limiter_blocks_after_limit():
    key = "test-rate-limit"

    assert allow_request(key, 2)[0] is True
    assert allow_request(key, 2)[0] is True
    allowed, retry_after = allow_request(key, 2)

    assert allowed is False
    assert retry_after > 0