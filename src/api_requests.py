import configparser
import json
import logging
import time
from typing import List

from requests import request

from src.models import Outage, Site

config = configparser.ConfigParser()
config.read("config.ini")

API_KEY = config["DEFAULT"]["API_KEY"]
BASE_URL = config["DEFAULT"]["BASE_URL"]
MAX_RETRIES = config["DEFAULT"]["MAX_RETRIES"]

logger = logging.getLogger()


class ResponseException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Status code {self.status_code}: {self.message}")


def get_outages(retry: int = 0) -> List[Outage]:
    r = request(
        method="GET",
        url=f"{BASE_URL}/outages",
        headers={"x-api-key": API_KEY},
    )
    all_outages = json.loads(r.text)
    if r.status_code == 200:
        return [Outage(**outage) for outage in all_outages]
    elif r.status_code == 500 and retry < MAX_RETRIES:
        logger.warn(f"500 encountered in GET outages on {retry=}, retrying...")
        time.sleep(3)
        return get_outages(retry + 1)
    raise ResponseException(status_code=r.status_code, message=r.text)


def get_site_info(site_id: str, retry: int = 0) -> Site:
    r = request(
        method="GET",
        url=f"{BASE_URL}/site-info/{site_id}",
        headers={"x-api-key": API_KEY},
    )
    site_info = json.loads(r.text)
    if r.status_code == 200:
        return Site(**site_info)
    elif r.status_code == 500 and retry < MAX_RETRIES:
        logger.warn(f"500 encountered in GET site-info on {retry=}, retrying...")
        time.sleep(3)
        return get_site_info(site_id, retry + 1)
    raise ResponseException(status_code=r.status_code, message=r.text)


def _create_json_outages_payload(outages: List[Outage]) -> str:
    return json.dumps([outage.to_POST_dict() for outage in outages])


def post_outages(outages: List[Outage], site: Site, retry: int = 0) -> bool:
    json_payload = _create_json_outages_payload(outages)
    r = request(
        method="POST",
        url=f"{BASE_URL}/site-outages/{site.id}",
        data=json_payload,
        headers={"x-api-key": API_KEY},
    )
    if r.status_code == 200:
        return True
    elif r.status_code == 500 and retry < MAX_RETRIES:
        logger.warn(f"500 encountered in GET site-info on {retry=}, retrying...")
        time.sleep(3)
        return post_outages(outages, site, retry + 1)
    raise ResponseException(status_code=r.status_code, message=r.text)
