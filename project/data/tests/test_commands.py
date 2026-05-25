import io
import pytest
from django.core.management import call_command
from django.core.management.base import CommandError


def test_get_temperature_command_success(mocker):
    mock_get_temp = mocker.patch(
        "project.data.management.commands.get_temperature.get_temperature",
        return_value=15.4,
    )

    out = io.StringIO()
    call_command("get_temperature", stdout=out)

    assert "successfully fetched temperature: 15.4" in out.getvalue()
    mock_get_temp.assert_called_once()


def test_get_temperature_command_failure(mocker):
    mocker.patch(
        "project.data.management.commands.get_temperature.get_temperature",
        side_effect=Exception("API offline"),
    )

    with pytest.raises(CommandError) as excinfo:
        call_command("get_temperature")

    assert "Can't fetch temperature - API offline" in str(excinfo.value)
