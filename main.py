import datetime
import logging

from api_requests import get_outages, get_site_info, post_outages
from filter import (annotate_outages_with_device_names,
                    keep_outages_after_datetime, keep_outages_from_devices)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def main(site_id: str, cutoff_datetime: datetime.datetime) -> None:
    outages = get_outages()
    logging.info(f"Retrieved {len(outages)} outages")
    site = get_site_info(site_id)

    filtered_outages = keep_outages_after_datetime(
        keep_outages_from_devices(outages, devices=site.devices),
        cutoff_datetime=cutoff_datetime,
    )
    logging.info(f"Filtered down to {len(filtered_outages)} outages")

    logging.info("Annotating outages...")
    annotated_outages = annotate_outages_with_device_names(
        filtered_outages, devices=site.devices
    )

    post_successful = post_outages(annotated_outages, site)
    if post_successful:
        logging.info(f"Outages successfully posted to {site.id}")


if __name__ == "__main__":
    main(
        site_id="norwich-pear-tree",
        cutoff_datetime=datetime.datetime(2022, 1, 1, tzinfo=datetime.timezone.utc),
    )
