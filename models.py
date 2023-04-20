import datetime
from typing import Optional, List

from pydantic import BaseModel


class Outage(BaseModel):
    id: str
    begin: datetime.datetime
    end: datetime.datetime
    name: Optional[str]


class Device(BaseModel):
    id: str
    name: str


class Site(BaseModel):
    id: str
    name: str
    devices: List[Device]
