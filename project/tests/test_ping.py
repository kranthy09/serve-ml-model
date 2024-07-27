"""
Tests for ping API endpoint
"""


def test_ping(test_app):
    """Test function for Ping API endpoint"""
    response = test_app.get("/ping")
    assert response.status_code == 200
    assert response.json() == {
        "ping": "pong!",
        "environment": "dev",
        "testing": True,
    }
