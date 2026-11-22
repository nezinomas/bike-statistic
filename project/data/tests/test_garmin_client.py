import json
import logging
import os
import stat

import pytest
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
from garminconnect import Garmin, GarminConnectTooManyRequestsError
from mock import call, patch

from ...users.factories import UserFactory
from ..library import garmin_client
from ..library.garmin_client import (
    SHARED_TOKEN_MODE,
    GarminClient,
    keep_tokens_shared,
    token_file,
)

MODULE = "project.data.library.garmin_client"

# Windows has no group bits: os.chmod only sets or clears read-only there.
posix_modes = pytest.mark.skipif(os.name == "nt", reason="needs POSIX file modes")


def mode(path):
    return stat.S_IMODE(os.stat(path).st_mode)


@pytest.fixture
def tokenstore(tmp_path, monkeypatch):
    store = tmp_path / ".garminconnect"
    store.mkdir()
    monkeypatch.setitem(settings.ENV, "GARMIN_TOKEN_STORE", str(store))
    return store


def real_client():
    garmin = Garmin(email="user@example.com", password="secret")
    garmin.client.di_token = "token"
    garmin.client.di_refresh_token = "refresh"
    garmin.client.di_client_id = "client"
    return garmin.client


def test_token_file_for_directory(tokenstore):
    assert token_file(tokenstore) == tokenstore / "garmin_tokens.json"


def test_token_file_for_json_path(tmp_path):
    assert token_file(tmp_path / "x.json") == tmp_path / "x.json"


@posix_modes
def test_library_dump_alone_is_owner_only(tokenstore):
    # The reason for keep_tokens_shared: if garminconnect stops forcing 0600,
    # this fails and the wrapper can go.
    client = real_client()

    client.dump(str(tokenstore))

    assert mode(tokenstore / "garmin_tokens.json") == 0o600


@posix_modes
def test_dump_leaves_token_group_readable(tokenstore):
    client = real_client()
    keep_tokens_shared(client)

    client.dump(str(tokenstore))

    path = tokenstore / "garmin_tokens.json"
    assert mode(path) == 0o660
    assert json.loads(path.read_text())["di_refresh_token"] == "refresh"


@posix_modes
def test_token_refresh_leaves_token_group_readable(tokenstore):
    # A refresh during the run writes through client._persist_tokens().
    client = real_client()
    keep_tokens_shared(client)
    client._tokenstore_path = str(tokenstore)

    client._persist_tokens()

    assert mode(tokenstore / "garmin_tokens.json") == 0o660


def test_dump_chmods_token_file(tokenstore):
    # Same as the POSIX test above, but runs on Windows too.
    client = real_client()
    keep_tokens_shared(client)

    with patch(f"{MODULE}.os.chmod") as mck_chmod:
        client.dump(str(tokenstore))

    # os is shared, so the library's own chmods are in the list too; ours is last.
    assert mck_chmod.call_args == call(
        tokenstore / "garmin_tokens.json", SHARED_TOKEN_MODE
    )


def test_symlinked_token_file_is_not_chmodded(tmp_path, caplog):
    path = tmp_path / "garmin_tokens.json"

    with (
        patch.object(type(path), "is_symlink", return_value=True),
        patch(f"{MODULE}.os.chmod") as mck_chmod,
        caplog.at_level(logging.WARNING, logger=MODULE),
    ):
        garmin_client.share_token_file(path)

    mck_chmod.assert_not_called()
    assert "is a symlink" in caplog.text


def test_saved_token_is_loaded_back(tokenstore):
    writer = real_client()
    keep_tokens_shared(writer)
    writer.dump(str(tokenstore))

    reader = Garmin(email="user@example.com", password="secret").client
    reader.load(str(tokenstore))

    assert reader.di_token == "token"


@patch(f"{MODULE}.Garmin")
def test_client_resumes_from_token_store(mck_garmin, tokenstore):
    actual = GarminClient("user@example.com", "secret")

    mck_garmin.return_value.login.assert_called_once_with(str(tokenstore))
    assert actual.client is mck_garmin.return_value
    assert bool(actual)


@patch(f"{MODULE}.keep_tokens_shared")
@patch(f"{MODULE}.Garmin")
def test_client_shares_tokens_before_login(mck_garmin, mck_share, tokenstore):
    calls = []
    mck_share.side_effect = lambda client: calls.append("share")
    mck_garmin.return_value.login.side_effect = lambda path: calls.append("login")

    GarminClient("user@example.com", "secret")

    mck_share.assert_called_once_with(mck_garmin.return_value.client)
    assert calls == ["share", "login"]


@patch(f"{MODULE}.Garmin")
def test_client_rate_limited_is_logged(mck_garmin, tokenstore, caplog):
    mck_garmin.return_value.login.side_effect = GarminConnectTooManyRequestsError(
        "Too many login attempts"
    )

    with caplog.at_level(logging.WARNING, logger=MODULE):
        actual = GarminClient("user@example.com", "secret")

    assert not actual
    assert "Garmin login failed: Too many login attempts" in caplog.text


@patch(f"{MODULE}.Garmin")
def test_unreadable_token_is_logged(mck_garmin, tokenstore, caplog, monkeypatch):
    (tokenstore / "garmin_tokens.json").write_text("{}")
    monkeypatch.setattr(garmin_client.os, "access", lambda path, how: False)

    with caplog.at_level(logging.WARNING, logger=MODULE):
        GarminClient("user@example.com", "secret")

    assert "is not readable by this user" in caplog.text


@patch(f"{MODULE}.Garmin")
def test_readable_token_is_not_logged(mck_garmin, tokenstore, caplog):
    (tokenstore / "garmin_tokens.json").write_text("{}")

    with caplog.at_level(logging.WARNING, logger=MODULE):
        GarminClient("user@example.com", "secret")

    assert "not readable" not in caplog.text


@pytest.mark.django_db
@patch("project.data.management.commands.cron.sleep")
@patch(f"{MODULE}.Garmin")
def test_cron_command_fails_on_failed_login(mck_garmin, mck_sleep, tokenstore):
    UserFactory()
    mck_garmin.return_value.login.side_effect = GarminConnectTooManyRequestsError("429")

    with pytest.raises(CommandError, match="Garmin client is not initialized"):
        call_command("cron")


@pytest.mark.django_db
@patch("project.data.management.commands.cron.sleep")
def test_cron_command_success_writes_nothing_to_stderr(mck_sleep, capsys):
    with patch(
        "project.data.library.insert_garmin.SyncWithGarmin._inserter"
    ) as mck_inserter:
        call_command("cron")

    mck_inserter.assert_called_once()
    captured = capsys.readouterr()
    assert "successfully get Garmin activities" in captured.out
    assert captured.err == ""
