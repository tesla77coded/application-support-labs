import requests
import pytest
from unittest.mock import Mock, patch

from monitor import check_health


def test_check_health_success():
    mock_response = Mock()
    mock_response.status_code = 200

    with patch("monitor.requests.get", return_value=mock_response):
        result = check_health("https://example.com")

    assert result["status"] == "HEALTHY"
    assert result["http_status"] == 200


@pytest.mark.parametrize(
    "status_code",
    [400, 401, 403, 404, 500, 502, 503, 504],
)
def test_check_health_http_error(status_code):
    mock_response = Mock()
    mock_response.status_code = status_code

    with patch("monitor.requests.get", return_value=mock_response):
        result = check_health("https://example.com")

    assert result["status"] == "UNHEALTHY"
    assert result["http_status"] == status_code
    assert result["reason"] == f"HTTP {status_code}"


def test_check_health_timeout():
    with patch(
        "monitor.requests.get",
        side_effect=requests.Timeout,
    ):
        result = check_health("https://example.com")

    assert result["status"] == "UNHEALTHY"
    assert result["http_status"] is None
    assert result["latency"] is None
    assert result["reason"] == "Request timed out"


def test_check_health_connection_error():
    with patch(
        "monitor.requests.get",
        side_effect=requests.ConnectionError("Connection refused"),
    ):
        result = check_health("https://example.com")

    assert result["status"] == "UNHEALTHY"
    assert result["http_status"] is None
    assert result["latency"] is None
    assert "Connection refused" in result["reason"]


def test_check_health_slow_response():
    mock_response = Mock()
    mock_response.status_code = 200

    with (
        patch("monitor.requests.get", return_value=mock_response),
        patch(
            "monitor.time.perf_counter",
            side_effect=[100.0, 103.0],
        ),
    ):
        result = check_health("https://example.com")

    assert result["status"] == "UNHEALTHY"
    assert result["http_status"] == 200
    assert result["latency"] == 3.0
    assert result["reason"] == "Response too slow"
