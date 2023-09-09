from typing import Optional

from pydantic import BaseModel, Field


class CargoItem(BaseModel):
    length: int
    width: int
    height: int
    quantity: int
    weight: int
    delta: Optional[int]


class CalculateRequest(BaseModel):
    floor_length: int = Field(default=13400)
    tare_weight: int = Field(default=21)
    floor_height_from_level_rail_heads: int = Field(default=1310)
    height_center_gravity_from_level_rail_heads: int = Field(default=800)
    platform_base: int = Field(default=9720)
    cargo: list[CargoItem]


class CalculateResponse(BaseModel):
    result: dict[str, float | list]
    report: Optional[str]
