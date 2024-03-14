from pydantic import BaseModel, field_validator
from typing_extensions import TypedDict
from app.enums.mod_enum import MeanOfDeath


class GameSchema(BaseModel):
    game_id: int
    total_kills: int
    world_kills: int
    players: list[str]
    kills: dict
