from pydantic import BaseModel


class CargoItem(BaseModel):
    length: int
    width: int
    height: int
    quantity: int
    weight: int
    coordinate_center_gravity_load_relative_end_board: int

    center_gravity: int
    coordinate_center_gravity_load_relative_end_board: int


class CalculateRequest(BaseModel):
    floor_length: int
    tare_weight: int
    floor_height_from_level_rail_heads: int
    height_center_gravity_from_level_rail_heads: int
    platform_base: int
    cargo: list[CargoItem]


class CalculateResponse(BaseModel):
    result: dict
    report: str
