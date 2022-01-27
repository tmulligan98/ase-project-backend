from pydantic import BaseModel


class ErrorModel(BaseModel):  # Error Models
    message: str
    code: int
