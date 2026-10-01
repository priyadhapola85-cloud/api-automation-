"""Loads settings for the selected environment.

Priority (highest wins): OS environment variables > .env (secrets) > config/environments/<env>.env
"""
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_DIR = ROOT_DIR / "config" / "environments"


@dataclass(frozen=True)
class Settings:
    env: str
    base_url: str
    api_key: str
    api_key_header: str
    timeout: int


def load_settings(env: str) -> Settings:
    env_file = ENV_DIR / f"{env}.env"
    if not env_file.exists():
        available = ", ".join(p.stem for p in ENV_DIR.glob("*.env"))
        raise FileNotFoundError(f"No config for env '{env}'. Available: {available}")

    values = {**dotenv_values(env_file), **dotenv_values(ROOT_DIR / ".env"), **os.environ}

    missing = [key for key in ("BASE_URL", "API_KEY") if not values.get(key)]
    if missing:
        raise ValueError(f"Missing required settings: {', '.join(missing)} (see .env.example)")

    return Settings(
        env=env,
        base_url=values["BASE_URL"],
        api_key=values["API_KEY"],
        api_key_header=values.get("API_KEY_HEADER") or "x-api-key",
        timeout=int(values.get("TIMEOUT") or 30),
    )
