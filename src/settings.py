import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

def _to_bool(s: str | None, default=False) -> bool:
    if s is None:
        return default
    return s.strip().lower() in {"1","true","yes","y"}

@dataclass(frozen=True)
class Settings:
    supabase_url: str
    supabase_key: str
    zapi_base_url: str
    zapi_instance_id: str
    zapi_token: str
    zapi_client_token: str
    dry_run: bool
    log_level: str
    max_messages: int

def get_settings() -> Settings:
    supabase_url = os.getenv("SUPABASE_URL", "")
    supabase_key = os.getenv("SUPABASE_ANON_KEY", "")
    zapi_base_url = os.getenv("ZAPI_BASE_URL", "https://api.z-api.io").rstrip("/")
    zapi_instance_id = os.getenv("ZAPI_INSTANCE_ID", "")
    zapi_token = os.getenv("ZAPI_TOKEN", "")
    zapi_client_token = os.getenv("ZAPI_CLIENT_TOKEN", "")
    dry_run = _to_bool(os.getenv("DRY_RUN"), False)
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    max_messages = int(os.getenv("MAX_MESSAGES", "3"))

    for k, v in {
        "SUPABASE_URL": supabase_url,
        "SUPABASE_ANON_KEY": supabase_key,
        "ZAPI_INSTANCE_ID": zapi_instance_id,
        "ZAPI_TOKEN": zapi_token,
    }.items():
        if not v:
            raise RuntimeError(f"Missing required env var: {k}")

    return Settings(
        supabase_url, supabase_key, zapi_base_url, zapi_instance_id, zapi_token,
        zapi_client_token, dry_run, log_level, max_messages
    )
