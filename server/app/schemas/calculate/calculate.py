from pydantic import BaseModel


class CargoItem(BaseModel):
    length: int
    width: int
    height: int
    quantity: int
    weight: int

    delta_length: int
    delta_width: int


class CalculateRequest(BaseModel):
    floor_length: int
    floor_width: int
    tare_weight: int
    floor_height_from_level_rail_heads: int
    height_center_gravity_from_level_rail_heads: int
    platform_base: int
    cargo: list[CargoItem]


class CalculateResponse(BaseModel):
    result: dict
    report: str
