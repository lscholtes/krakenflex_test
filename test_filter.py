import datetime

from filter import (annotate_outages_with_device_names,
                    keep_outages_after_datetime, keep_outages_from_devices)
from models import Device, Outage

OUTAGES = [
    {
        "id": "002b28fc-283c-47ec-9af2-ea287336dc1b",
        "begin": "2021-07-26T17:09:31.036Z",
        "end": "2021-08-29T00:37:42.253Z",
    },  # Before cutoff, from kingfisher
    {
        "id": "002b28fc-283c-47ec-9af2-ea287336dc1b",
        "begin": "2022-05-23T12:21:27.377Z",
        "end": "2022-11-13T02:16:38.905Z",
    },  # After cutoff, from kingfisher
    {
        "id": "002b28fc-283c-47ec-9af2-ea287336dc1b",
        "begin": "2022-12-04T09:59:33.628Z",
        "end": "2022-12-12T22:35:13.815Z",
    },  # After cutoff, from kingfisher
    {
        "id": "04ccad00-eb8d-4045-8994-b569cb4b64c1",
        "begin": "2022-07-12T16:31:47.254Z",
        "end": "2022-10-13T04:05:10.044Z",
    },  # After cutoff, not from kingfisher
    {
        "id": "086b0d53-b311-4441-aaf3-935646f03d4d",
        "begin": "2022-07-12T16:31:47.254Z",
        "end": "2022-10-13T04:05:10.044Z",
    },  # After cutoff, from kingfisher
    {
        "id": "27820d4a-1bc4-4fc1-a5f0-bcb3627e94a1",
        "begin": "2021-07-12T16:31:47.254Z",
        "end": "2022-10-13T04:05:10.044Z",
    },  # Before cutoff, not from kingfisher
]

SITE = {
    "id": "kingfisher",
    "name": "KingFisher",
    "devices": [
        {"id": "002b28fc-283c-47ec-9af2-ea287336dc1b", "name": "Battery 1"},
        {"id": "086b0d53-b311-4441-aaf3-935646f03d4d", "name": "Battery 2"},
    ],
}


def test_keep_outages_after_datetime():
    outages = [Outage(**outage) for outage in OUTAGES]
    cutoff_datetime = datetime.datetime(2022, 2, 1, tzinfo=datetime.timezone.utc)

    filtered_outages = keep_outages_after_datetime(outages, cutoff_datetime)

    expected_outages = [Outage(**OUTAGES[i]) for i in [1, 2, 3, 4]]
    for outage in expected_outages:
        assert outage in filtered_outages
    assert len(filtered_outages) == len(expected_outages)


def keep_outages_from_devices():
    outages = [Outage(**outage) for outage in OUTAGES]
    devices = [Device(**device_kwargs) for device_kwargs in SITE["devices"]]

    filtered_outages = keep_outages_from_devices(outages, devices)

    expected_outages = [Outage(**OUTAGES[i]) for i in [0, 1, 2, 4]]
    for outage in expected_outages:
        assert outage in filtered_outages
    assert len(filtered_outages) == len(expected_outages)


def test_annotate_outages_with_device_names():
    outages = [
        Outage(**OUTAGES[i])
        for i in [0, 1, 2, 4]  # Only test outages in kingfisher site
    ]
    devices = [Device(**device_kwargs) for device_kwargs in SITE["devices"]]

    annotated_outages = annotate_outages_with_device_names(outages, devices)

    expected_device_names = ["Battery 1", "Battery 1", "Battery 1", "Battery 2"]
    assert len(annotated_outages) == len(expected_device_names)
    for i, device_name in enumerate(expected_device_names):
        assert annotated_outages[i].name == device_name
