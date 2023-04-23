import datetime
from typing import List, Optional

from pydantic import BaseModel


class Outage(BaseModel):
    id: str
    begin: datetime.datetime
    end: datetime.datetime
    name: Optional[str]

    @staticmethod
    def _dt2str(dt: datetime.datetime) -> str:
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    def to_POST_dict(self):
        return {
            "id": self.id,
            "begin": self._dt2str(self.begin),
            "end": self._dt2str(self.end),
            "name": self.name,
        }


class Device(BaseModel):
    id: str
    name: str


class Site(BaseModel):
    id: str
    name: str
    devices: List[Device]
