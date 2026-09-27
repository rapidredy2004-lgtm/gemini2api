"""Start the container with a private API key supplied at runtime."""

import json
import os
import sys
import tempfile
from pathlib import Path


def build_config():
    api_key = os.environ.get("GEMINI_WEB2API_API_KEY", "").strip()
    if not api_key:
        raise ValueError("Set GEMINI_WEB2API_API_KEY in Render Environment before deploying")

    try:
        port = int(os.environ.get("PORT", "8081"))
    except ValueError as exc:
        raise ValueError("PORT must be an integer") from exc
    if not 1 <= port <= 65535:
        raise ValueError("PORT must be between 1 and 65535")

    config = json.loads(Path(__file__).with_name("config.example.json").read_text(encoding="utf-8"))
    config.update({"host": "0.0.0.0", "port": port, "api_keys": [api_key]})

    cookie_file = os.environ.get("GEMINI_WEB2API_COOKIE_FILE", "").strip()
    if cookie_file:
        if not Path(cookie_file).is_file():
            raise ValueError(f"Cookie file does not exist: {cookie_file}")
        config["cookie_file"] = cookie_file

    return config


def main():
    try:
        config = build_config()
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    fd, config_path = tempfile.mkstemp(prefix="gemini-web2api-", suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as config_file:
        json.dump(config, config_file)

    os.execv(sys.executable, [sys.executable, "-m", "gemini_web2api", "--config", config_path])


if __name__ == "__main__":
    main()
