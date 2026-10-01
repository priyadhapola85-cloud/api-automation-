"""Single HTTP client shared by all services.

Handles base URL, API-key auth, default headers, timeouts and request/response logging,
so services and tests never deal with those details.
"""
import logging

import requests

log = logging.getLogger("api")


class APIClient:
    def __init__(self, base_url: str, api_key: str, api_key_header: str = "x-api-key", timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            api_key_header: api_key,
        })

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}/{path.lstrip('/')}"
        kwargs.setdefault("timeout", self.timeout)
        response = self.session.request(method, url, **kwargs)
        self._log(response)
        return response

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs) -> requests.Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self.request("DELETE", path, **kwargs)

    def close(self):
        self.session.close()

    @staticmethod
    def _log(response: requests.Response):
        # Headers are not logged, so the API key never ends up in logs or reports
        req = response.request
        elapsed_ms = response.elapsed.total_seconds() * 1000
        log.info("%s %s -> %s (%.0f ms)", req.method, req.url, response.status_code, elapsed_ms)
        if req.body:
            log.debug("Request body: %s", req.body)
        log.debug("Response body: %s", response.text[:2000])
