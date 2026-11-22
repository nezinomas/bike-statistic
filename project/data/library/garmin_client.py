import logging
import os
from pathlib import Path

import requests
from django.conf import settings
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

from ...core.lib import utils
from . import garmin_exceptions

logger = logging.getLogger(__name__)

# The token store is shared with the maps site: one Garmin account, one folder
# (root:garmin 2770), both site users in the 'garmin' group. garminconnect
# writes its token file as 0600, which locks the other site out and sends it
# to a password login (and Garmin's 429s) on every run. Every write from here
# is made group-readable again.
TOKEN_FILE_NAME = "garmin_tokens.json"
SHARED_TOKEN_MODE = 0o660


def token_file(tokenstore: Path) -> Path:
    """The file garminconnect reads and writes for a token store path."""
    if tokenstore.is_dir() or tokenstore.suffix.lower() != ".json":
        return tokenstore / TOKEN_FILE_NAME
    return tokenstore


def share_token_file(path: Path) -> None:
    if path.is_symlink():
        logger.warning("Garmin token file %s is a symlink; mode left alone", path)
        return
    try:
        os.chmod(path, SHARED_TOKEN_MODE)
    except OSError as e:
        logger.warning("Cannot make Garmin token file %s group-readable: %s", path, e)


def keep_tokens_shared(client) -> None:
    """Wrap client.dump, so a login and a token refresh both leave the file shared."""
    library_dump = client.dump

    def dump(path: str) -> None:
        library_dump(path)
        share_token_file(token_file(Path(path).expanduser()))

    client.dump = dump


def warn_if_unreadable(path: Path) -> None:
    """Say why a saved token is not used, instead of a silent password login."""
    if not path.exists() or os.access(path, os.R_OK):
        return
    st = path.stat()
    logger.warning(
        "Garmin token file %s is not readable by this user (owner uid %s, "
        "mode %o): logging in with the password instead. The other site wrote "
        "it owner-only; it must be group-readable (%o).",
        path,
        st.st_uid,
        st.st_mode & 0o777,
        SHARED_TOKEN_MODE,
    )


class GarminClient:
    def __init__(self, username: str, password: str):
        self.client = self._client(username, password)

    def __bool__(self):
        return self.client is not None

    def _client(self, username, password):
        if not username or not password:
            raise garmin_exceptions.NoUsernameOrPasswordError

        tokenstore_path = Path(settings.ENV["GARMIN_TOKEN_STORE"]).expanduser()

        # Ensure directory exists
        if not tokenstore_path.parent.exists():
            tokenstore_path.parent.mkdir(parents=True, exist_ok=True)

        warn_if_unreadable(token_file(tokenstore_path))

        try:
            garmin = Garmin(
                email=username,
                password=utils.decrypt(password),
                is_cn=False,
                return_on_mfa=False,
            )
            keep_tokens_shared(garmin.client)
            # Resumes from the saved token; the password is used only when the
            # token is missing, unreadable or rejected.
            garmin.login(str(tokenstore_path))

            return garmin

        except (
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
            FileNotFoundError,
            GarminConnectConnectionError,
            requests.exceptions.HTTPError,
        ) as e:
            logger.warning("Garmin login failed: %s", e)
            return None

        except KeyboardInterrupt:
            return None

    def get_workouts(self, max_results=10):
        if not self.client:
            raise Exception("Garmin client is not initialized")

        try:
            workouts = self.client.get_activities(0, max_results)
        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
        ) as e:
            raise garmin_exceptions.GetActivitiesError(e) from e
        except Exception as e:
            raise garmin_exceptions.GetActivitiesUnknownError(e) from e

        return workouts
