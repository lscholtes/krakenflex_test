from src.api_requests import _create_json_outages_payload
from src.models import Outage

OUTAGES = [
    {
        "id": "002b28fc-283c-47ec-9af2-ea287336dc1b",
        "begin": "2021-07-26T17:09:31.036Z",
        "end": "2021-08-29T00:37:42.253Z",
        "name": "foo",
    },
    {
        "id": "002b28fc-283c-47ec-9af2-ea287336dc1b",
        "begin": "2022-05-23T12:21:27.377Z",
        "end": "2022-11-13T02:16:38.905Z",
        "name": "bar",
    },
]


def test_create_json_outages_payload():
    outages = [Outage(**outage_kwargs) for outage_kwargs in OUTAGES]
    json_outages_payload = _create_json_outages_payload(outages)
    expected_payload = '[{"id": "002b28fc-283c-47ec-9af2-ea287336dc1b", "begin": "2021-07-26T17:09:31.036Z", "end": "2021-08-29T00:37:42.253Z", "name": "foo"}, {"id": "002b28fc-283c-47ec-9af2-ea287336dc1b", "begin": "2022-05-23T12:21:27.377Z", "end": "2022-11-13T02:16:38.905Z", "name": "bar"}]'
    assert json_outages_payload == expected_payload
