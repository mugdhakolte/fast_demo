from pydantic import BaseModel


class SummeryPayloadSchema(BaseModel):
    url: str
