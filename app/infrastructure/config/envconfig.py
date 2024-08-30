import os
from pathlib import Path
from typing import Any

from app.profile_enricher.exceptions import BasePathException

from .contract import ConfigContract


class EnvConfig(ConfigContract):
    """
    Implementation of ConfigContract that reads configuration from environment variables.
    """

    def __init__(self):
        self.env = os.environ

    def get_log_level(self) -> str:
        return self._get("LOG_LEVEL", "INFO").upper()

    def get_download_timeout(self) -> int:
        return int(self._get("DOWNLOAD_TIMEOUT", 10))

    def get_cors_allowed_origins(self) -> list[str]:
        origins = self._get("CORS_ALLOWED_ORIGINS", [])
        return [origin.strip() for origin in origins.split(",")]

    def get_profiles_base_path(self) -> str:
        return self._get("PROFILES_BASE_PATH", os.path.join("data", "dases_profiles"))

    def get_and_create_profiles_base_path(self) -> str:
        path = self.get_profiles_base_path()
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
        except PermissionError:
            raise BasePathException(
                f"Permission denied when creating directory: {path}"
            )
        except OSError as e:
            raise BasePathException(f"Failed to create directory {path}: {str(e)}")

        if not os.access(path, os.W_OK):
            raise BasePathException(f"Created directory {path} is not writable")

        return path

    def get_profile_url(self, profile_name: str) -> str:
        return self._get(f"PROFILE_{profile_name.upper()}_URL", "")

    def get_profiles_names(self) -> list[str]:
        names = self._get("PROFILES_NAMES", [])
        return [name.strip() for name in names.split(",")]

    @staticmethod
    def _get(key: str, default: Any = None) -> Any:
        """
        Get a value from environment variables with a default.

        :param key: The key of the environment variable.
        :param default: The default value if the key is not found.
        :return: The value from the environment variable or the default.
        """
        try:
            return os.getenv(key=key, default=default)
        except Exception:
            return default
