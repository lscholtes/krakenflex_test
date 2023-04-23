import configparser
import json
from typing import List

from requests import request

from src.models import Outage, Site

config = configparser.ConfigParser()
config.read("config.ini")

API_KEY = config["DEFAULT"]["API_KEY"]
BASE_URL = config["DEFAULT"]["BASE_URL"]


class ResponseException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Status code {self.status_code}: {self.message}")


def get_outages() -> List[Outage]:
    r = request(
        method="GET",
        url=f"{BASE_URL}/outages",
        headers={"x-api-key": API_KEY},
    )
    all_outages = json.loads(r.text)
    if r.status_code == 200:
        return [Outage(**outage) for outage in all_outages]
    raise ResponseException(status_code=r.status_code, message=r.text)


def get_site_info(site_id: str) -> Site:
    r = request(
        method="GET",
        url=f"{BASE_URL}/site-info/{site_id}",
        headers={"x-api-key": API_KEY},
    )
    site_info = json.loads(r.text)
    if r.status_code == 200:
        return Site(**site_info)
    raise ResponseException(status_code=r.status_code, message=r.text)


def _create_json_outages_payload(outages: List[Outage]) -> str:
    return json.dumps([outage.to_POST_dict() for outage in outages])


def post_outages(outages: List[Outage], site: Site) -> bool:
    json_payload = _create_json_outages_payload(outages)
    r = request(
        method="POST",
        url=f"{BASE_URL}/site-outages/{site.id}",
        data=json_payload,
        headers={"x-api-key": API_KEY},
    )
    if r.status_code == 200:
        return True
    raise ResponseException(status_code=r.status_code, message=r.text)
