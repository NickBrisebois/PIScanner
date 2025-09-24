from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class PiScannerServerSettings(BaseSettings):
    app_name: str = "PiScanner-Server"

    datastore_path: str = "~/.local/share/PiScanner/images"

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_prefix="PISCANNER_",
        env_file=".env",
    )

@lru_cache
def get_settings() -> PiScannerServerSettings:
    return PiScannerServerSettings()
