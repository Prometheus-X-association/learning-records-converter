import os
from pathlib import Path

from app.profile_enricher.exceptions import BasePathError

from .contract import ConfigContract


class EnvConfig(ConfigContract):
    """Implementation of ConfigContract that reads configuration from environment variables."""

    def __init__(self) -> None:
        """Initialize the EnvConfig."""
        self.env = os.environ

    def get_log_level(self) -> str:
        """Inherited from ConfigContract.get_log_level."""
        return self._get("LOG_LEVEL", "INFO").upper()

    def get_download_timeout(self) -> int:
        """Inherited from ConfigContract.get_download_timeout."""
        return int(self._get("DOWNLOAD_TIMEOUT", "10"))

    def get_cors_allowed_origins(self) -> set[str]:
        """Inherited from ConfigContract.get_cors_allowed_origins."""
        origins = self._get("CORS_ALLOWED_ORIGINS", "*")
        return {origin.strip() for origin in origins.split(",")}

    def get_profiles_base_path(self) -> str:
        """Inherited from ConfigContract.get_profiles_base_path."""
        return self._get(
            "PROFILES_BASE_PATH",
            Path("data").joinpath("dases_profiles").as_posix(),
        )

    def get_and_create_profiles_base_path(self) -> str:
        """Inherited from ConfigContract.get_and_create_profiles_base_path."""
        path = self.get_profiles_base_path()
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            raise BasePathError(
                f"Permission denied when creating directory: {path}",
            ) from e
        except OSError as e:
            raise BasePathError(f"Failed to create directory {path}: {e}") from e

        if not os.access(path, os.W_OK):
            raise BasePathError(f"Created directory {path} is not writable")

        return path

    def get_profile_url(self, profile_name: str) -> str:
        """Inherited from ConfigContract.get_profile_url."""
        return self._get(f"PROFILE_{profile_name.upper()}_URL", "")

    def get_profiles_names(self) -> set[str]:
        """Inherited from ConfigContract.get_profiles_names."""
        names = self._get("PROFILES_NAMES")
        if not names:
            return set()
        return {name.strip() for name in names.split(",")}

    @staticmethod
    def _get(key: str, default: str | None) -> str:
        """
        Get a value from environment variables with a default.

        :param key: The key of the environment variable.
        :param default: The default value if the key is not found.
        :return: The value from the environment variable or the default.
        """
        return os.environ.get(key, default)
