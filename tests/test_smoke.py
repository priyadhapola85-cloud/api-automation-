import pytest


@pytest.mark.smoke
def test_api_is_reachable(api_client):
    response = api_client.get("/")
    assert response.status_code < 500, f"Server error: {response.status_code} {response.text[:200]}"
