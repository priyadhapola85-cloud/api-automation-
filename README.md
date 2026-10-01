# API Automation Framework

Python + pytest + requests.

## Structure

```
config/
  environments/   dev.env, qa.env ... non-secret settings per environment
  settings.py     loads env file + .env (secrets) + OS env vars
core/
  api_client.py   shared HTTP client: base URL, API-key header, timeout, logging
services/         one class per API resource - tests call these, never raw URLs
schemas/          JSON schemas for response validation
test_data/        payload files for data-driven tests
tests/
  conftest.py     fixtures: settings, api_client
```

## Setup

```bash
python3.13 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env      # then put your real API key in .env
```

Set `BASE_URL` and `API_KEY_HEADER` in `config/environments/dev.env`.

## Running

```bash
pytest                      # all tests on dev
pytest --env qa             # against QA
pytest -m smoke             # only smoke tests
pytest --log-cli-level=DEBUG  # also print request/response bodies
```
