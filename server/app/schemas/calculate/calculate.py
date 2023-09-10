from typing import Optional

from pydantic import BaseModel, Field


class CargoItem(BaseModel):
    length: float
    width: float
    height: float
    quantity: int
    weight: int
    delta_length: int
    delta_width: int


class CalculateRequest(BaseModel):
    floor_length: float = Field(default=13400)
    floor_width: float = Field(default=2870)
    tare_weight: float = Field(default=21)
    floor_height_from_level_rail_heads: float = Field(default=1310)
    height_center_gravity_from_level_rail_heads: float = Field(default=800)
    platform_base: float = Field(default=9720)
    cargo: list[CargoItem]


class CalculateResponse(BaseModel):
    result: dict[str, float | list | str]
    report: Optional[str]
