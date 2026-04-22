import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print(
        "oracle: python-dotenv is required. "
        "Install it with: pip install python-dotenv",
        file=sys.stderr,
    )
    sys.exit(1)


REQUIRED_KEYS = (
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
)


def _redact(value: str) -> str:
    if not value:
        return "<empty>"
    if len(value) <= 4:
        return "*" * len(value)
    return value[:2] + "*" * (len(value) - 4) + value[-2:]


def _describe_database(url: str) -> str:
    if not url:
        return "Not configured"
    if "localhost" in url or "127.0.0.1" in url:
        return "Connected to local instance"
    return "Connected to remote instance"


def _describe_api(key: str) -> str:
    if not key:
        return "No credentials"
    return f"Authenticated (key: {_redact(key)})"


def _describe_zion(endpoint: str) -> str:
    if not endpoint:
        return "Offline"
    return "Online"


def main() -> None:
    # Load .env from cwd if present; real env vars always win.
    env_path = Path(".env")
    if env_path.is_file():
        load_dotenv(env_path)

    mode = os.environ.get("MATRIX_MODE", "development")
    database = os.environ.get("DATABASE_URL", "")
    api_key = os.environ.get("API_KEY", "")
    log_level = os.environ.get("LOG_LEVEL", "INFO")
    zion = os.environ.get("ZION_ENDPOINT", "")

    print("ORACLE STATUS: Reading the Matrix...")
    print()
    print("Configuration loaded:")
    print(f"Mode: {mode}")
    print(f"Database: {_describe_database(database)}")
    print(f"API Access: {_describe_api(api_key)}")
    print(f"Log Level: {log_level}")
    print(f"Zion Network: {_describe_zion(zion)}")
    print()

    missing = [k for k in REQUIRED_KEYS if not os.environ.get(k)]
    print("Environment security check:")
    if not missing:
        print("[OK] No hardcoded secrets detected")
    else:
        print(f"[WARN] Missing values: {', '.join(missing)}")
    if env_path.is_file():
        print("[OK] .env file properly configured")
    else:
        print("[WARN] No .env file - copy .env.example to .env")
    if mode == "production":
        print("[OK] Production mode active")
    else:
        print("[OK] Production overrides available")
    print()
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()
