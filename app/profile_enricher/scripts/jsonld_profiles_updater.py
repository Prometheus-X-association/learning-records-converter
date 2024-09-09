from pathlib import Path

from dotenv import load_dotenv

from app.infrastructure.config.contract import ConfigContract
from app.infrastructure.config.envconfig import EnvConfig
from app.infrastructure.logging.contract import LoggerContract
from app.infrastructure.logging.jsonlogger import JsonLogger
from app.profile_enricher.exceptions import (BasePathException,
                                             ProfileNotFoundException,
                                             ProfileValidationError)
from app.profile_enricher.repositories.jsonld.profile_loader import ProfileLoader


class JsonLdProfilesUpdater:
    """
    A class to update JSON-LD profiles based on environment variables.
    """

    def __init__(
        self, destination_dir: str, logger: LoggerContract, config: ConfigContract
    ):
        """
        Initialize the JsonLdProfilesUpdater.

        :param destination_dir: The directory where profiles will be saved.
        :param logger: LoggerContract implementation for logging
        :param config: ConfigContract implementation for config
        """
        self.destination_path: Path = Path(destination_dir)
        self.logger = logger
        self.config = config
        self.profile_loader: ProfileLoader = ProfileLoader(logger=logger, config=config)

    def update_all_profiles(self) -> None:
        """
        Update all profiles based on environment variables starting with 'PROFILE'.
        """
        self.logger.debug("Create path if not exists", {"path": self.destination_path})
        self.destination_path.mkdir(parents=True, exist_ok=True)

        profiles = self.config.get_profiles_names()
        for profile_name in profiles:
            try:
                self.update_profile(profile_name=profile_name)
            except Exception as e:
                self.logger.exception(
                    "Failed to update profile file", e, {"profile": profile_name}
                )

    def update_profile(self, profile_name: str) -> None:
        """
        Update a single profile based on the given environment variable.

        :param profile_name: The profile name.
        """
        file_path = self.destination_path.joinpath(f"{profile_name.lower()}.jsonld")

        log_context = {"profile": profile_name, "file_path": file_path}
        self.logger.debug("Found variable", log_context)

        try:
            profile_json = self.profile_loader.download_profile(group_name=profile_name)
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


def main(destination_dir: str | None = None) -> None:
    """
    Main function to run the profile updater.

    :param destination_dir: Optional directory where profiles will be saved
                            If not provided, a default directory is used
    """
    load_dotenv(dotenv_path=".env", verbose=True)
    env_config = EnvConfig()

    json_logger = JsonLogger(name=__name__, level=env_config.get_log_level())
    json_logger.info("Script starting", {"destination_dir": destination_dir})

    if destination_dir is None:
        try:
            destination_dir: Path = Path(env_config.get_and_create_profiles_base_path())
        except BasePathException as e:
            json_logger.exception("Failed to create or access profiles directory", e)
            raise

    json_logger.info("Script starting", {"destination_dir": destination_dir})

    updater = JsonLdProfilesUpdater(
        destination_dir=destination_dir, logger=json_logger, config=env_config
    )
    updater.update_all_profiles()


if __name__ == "__main__":
    main()
