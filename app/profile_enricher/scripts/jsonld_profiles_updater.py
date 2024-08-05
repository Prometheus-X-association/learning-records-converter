import logging
import os
from pathlib import Path

from app.profile_enricher.exceptions import (ProfileNotFoundException,
                                             ProfileValidationError)
from app.profile_enricher.repositories.jsonld.profile_loader import ProfileLoader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JsonLdProfilesUpdater:
    """
    A class to update JSON-LD profiles based on environment variables.
    """

    def __init__(self, destination_dir: str):
        """
        Initialize the JsonLdProfilesUpdater.

        :param destination_dir: The directory where profiles will be saved.
        """
        self.destination_path: Path = Path(destination_dir)
        self.profile_loader: ProfileLoader = ProfileLoader(base_path=destination_dir)

    def update_all_profiles(self) -> None:
        """
        Update all profiles based on environment variables starting with 'PROFILE'.
        """
        self.destination_path.mkdir(parents=True, exist_ok=True)

        env_vars = self.get_env_vars_with_prefix("PROFILE")
        for env_var in env_vars:
            try:
                self.update_profile(env_var)
            except Exception as e:
                logger.error(f"Failed to update profile for {env_var}: {e}")

    def update_profile(self, env_var: str) -> None:
        """
        Update a single profile based on the given environment variable.

        :param env_var: The environment variable name for the profile.
        """
        profile = env_var.removeprefix("PROFILE_").split("_")[0]
        file_path = self.destination_path.joinpath(f"{profile.lower()}.jsonld")

        try:
            profile_json = self.profile_loader.download_profile(group_name=profile)
            self.profile_loader.build_profile_model(profile_json)
            self.profile_loader.save_profile_file(
                file_path=file_path, profile_json=profile_json
            )
            logger.info(f"Successfully updated profile: {profile}")
        except ProfileNotFoundException:
            logger.error(f"Profile not found: {profile}")
        except ProfileValidationError:
            logger.error(f"Profile validation failed: {profile}")
        except Exception as e:
            logger.error(f"Unexpected error updating profile {profile}: {e}")

    @staticmethod
    def get_env_vars_with_prefix(prefix: str) -> list[str]:
        """
        Get a list of environment variable names that start with the given prefix.

        :param prefix: The prefix to filter environment variables.
        :return: A list of matching environment variable names.
        """
        return [key for key, value in os.environ.items() if key.startswith(prefix)]


def main(destination_dir: str = None) -> None:
    """
    Main function to run the profile updater.

    :param destination_dir: Optional directory where profiles will be saved.
                            If not provided, a default directory is used.
    """
    if destination_dir is None:
        destination_dir = os.path.join("data", "dases_profiles")

    updater = JsonLdProfilesUpdater(destination_dir=destination_dir)
    updater.update_all_profiles()


if __name__ == "__main__":
    main()
