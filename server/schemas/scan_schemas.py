import datetime
from pydantic import BaseModel


class Scan(BaseModel):
    id: str
    created_at: datetime.datetime
