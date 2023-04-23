import datetime

import pydantic
import pytest

from src.models import Device, Outage, Site


def test_outage_model_parses():
    outage_kwargs = {
        "id": "123",
        "begin": "2022-01-01T01:02:03.456Z",
        "end": "2022-02-02T03:02:01.654Z",
    }
    outage = Outage(**outage_kwargs)
    assert outage.id == "123"
    assert outage.begin == datetime.datetime(
        year=2022,
        month=1,
        day=1,
        hour=1,
        minute=2,
        second=3,
        microsecond=456000,
        tzinfo=datetime.timezone.utc,
    )
    assert outage.end == datetime.datetime(
        year=2022,
        month=2,
        day=2,
        hour=3,
        minute=2,
        second=1,
        microsecond=654000,
        tzinfo=datetime.timezone.utc,
    )


def test_outage_model_parsing_fails():
    outage_kwargs = {
        "id": "123",
        "begin": "2022/01/01T01:02:03.456Z",  # Incorrect formatting
        "end": "2022/02/02T03:02:01.654Z",
    }
    with pytest.raises(pydantic.ValidationError):
        outage = Outage(**outage_kwargs)


def test_outage_model_POST_dict():
    outage_kwargs = {
        "id": "123",
        "begin": "2022-01-01T01:02:03.456Z",
        "end": "2022-02-02T03:02:01.654Z",
        "name": "foo",
    }
    outage = Outage(**outage_kwargs)
    outage_POST_dict = outage.to_POST_dict()
    assert outage_POST_dict == outage_kwargs


def test_site_model_parses():
    site_kwargs = {
        "id": "456",
        "name": "foo",
        "devices": [{"id": "789", "name": "bar"}, {"id": "123", "name": "baz"}],
    }
    site = Site(**site_kwargs)
    assert site.id == "456"
    assert site.name == "foo"
    device_ids = ["789", "123"]
    device_names = ["bar", "baz"]
    for i, device in enumerate(site.devices):
        assert type(device) is Device
        assert device.id == device_ids[i]
        assert device.name == device_names[i]


def test_site_model_parsing_fails():
    site_kwargs = {
        "id": "456",
        "name": "foo",
        "devices": [
            {
                "id": "789",
            },  # Missing name for a device
            {"id": "123", "name": "baz"},
        ],
    }
    with pytest.raises(pydantic.ValidationError):
        site = Site(**site_kwargs)
