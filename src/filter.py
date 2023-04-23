import datetime
from typing import List

from src.models import Device, Outage


def keep_outages_after_datetime(
    outages: List[Outage], cutoff_datetime: datetime.datetime
) -> List[Outage]:
    return list(filter(lambda outage: outage.begin >= cutoff_datetime, outages))


def keep_outages_from_devices(
    outages: List[Outage], devices: List[Device]
) -> List[Outage]:
    return list(
        filter(
            lambda outage: outage.id in set(device.id for device in devices), outages
        )
    )


def annotate_outages_with_device_names(
    outages: List[Outage], devices: List[Device]
) -> List[Outage]:
    for outage in outages:
        outage_device = match_outage_to_device(outage, devices)
        outage.name = outage_device.name
    return outages


def match_outage_to_device(outage: List[Outage], devices: List[Device]) -> Device:
    matching_devices = list(filter(lambda device: device.id == outage.id, devices))
    if len(matching_devices) > 0:
        assert (
            len(set(device.id for device in matching_devices)) == 1
        ), f"Multiple matches found for {outage=}, {devices=}"
    matching_device = matching_devices[0]
    return matching_device
