from pydantic import BaseModel


class SampleInputBody(BaseModel):
    field_a: int
    field_b: str


class SampleOutputBody(BaseModel):
    message: str
