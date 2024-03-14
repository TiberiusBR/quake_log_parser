from pydantic import BaseModel


class PlayerSchema(BaseModel):
    id: str
    name: str
    score: int
