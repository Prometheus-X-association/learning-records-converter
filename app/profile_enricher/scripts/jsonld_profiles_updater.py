import os
from pathlib import Path

from app.infrastructure.logging.contract import LoggerContract
from app.infrastructure.logging.jsonlogger import JsonLogger
from app.profile_enricher.exceptions import (ProfileNotFoundException,
                                             ProfileValidationError)
from app.profile_enricher.repositories.jsonld.profile_loader import ProfileLoader


class JsonLdProfilesUpdater:
    """
    A class to update JSON-LD profiles based on environment variables.
    """

    def __init__(self, destination_dir: str, logger: LoggerContract):
        """
        Initialize the JsonLdProfilesUpdater.

        :param destination_dir: The directory where profiles will be saved.
        :param logger: LoggerContract implementation for logging
        """
        self.destination_path: Path = Path(destination_dir)
        self.logger = logger
        self.profile_loader: ProfileLoader = ProfileLoader(
            base_path=destination_dir, logger=logger
        )

    def update_all_profiles(self) -> None:
        """
        Update all profiles based on environment variables starting with 'PROFILE'.
        """
        self.logger.debug("Create path if not exists", {"path": self.destination_path})
        self.destination_path.mkdir(parents=True, exist_ok=True)

        env_vars = self.get_env_vars_with_prefix("PROFILE")
        for env_var in env_vars:
            try:
                self.update_profile(env_var)
            except Exception as e:
                self.logger.exception(
                    "Failed to update profile file", e, {"env_var": env_var}
                )

    def update_profile(self, env_var: str) -> None:
        """
        Update a single profile based on the given environment variable.

        :param env_var: The environment variable name for the profile.
        """
        profile = env_var.removeprefix("PROFILE_").split("_")[0]
        file_path = self.destination_path.joinpath(f"{profile.lower()}.jsonld")

        log_context = {"env_var": env_var, "profile": profile, "file_path": file_path}
        self.logger.debug("Found variable", log_context)

        try:
            profile_json = self.profile_loader.download_profile(group_name=profile)
            self.profile_loader.build_profile_model(profile_json)
            self.profile_loader.save_profile_file(
                file_path=file_path, profile_json=profile_json
            )
            self.logger.info("Successfully updated profile", log_context)
        except ProfileNotFoundException:
            self.logger.error("Profile not found", log_context)
        except ProfileValidationError:
            self.logger.error("Profile validation failed", log_context)
        except Exception as e:
            self.logger.exception("Unexpected error updating profile", e, log_context)

    @staticmethod
    def get_env_vars_with_prefix(prefix: str) -> list[str]:
        """
        Get a list of environment variable names that start with the given prefix.

        :param prefix: The prefix to filter environment variables.
        :return: A list of matching environment variable names.
        """
        return [key for key in os.environ.keys() if key.startswith(prefix)]


def main(destination_dir: str | None = None) -> None:
    """
    Main function to run the profile updater.

    :param destination_dir: Optional directory where profiles will be saved.
                            If not provided, a default directory is used.
    """
    if destination_dir is None:
        destination_dir = os.path.join("data", "dases_profiles")

    logger = JsonLogger(__name__)
    logger.info("Script starting", {"destination_dir": destination_dir})

    updater = JsonLdProfilesUpdater(destination_dir=destination_dir, logger=logger)
    updater.update_all_profiles()


if __name__ == "__main__":
    main()
