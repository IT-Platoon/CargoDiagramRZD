from typing import Annotated

from fastapi import APIRouter, Body, Request, status

from app.schemas import CalculateRequest, CalculateResponse
from app.utils.calculate import calculate_centers_of_mass, get_report


api_router = APIRouter(
    prefix="/calculate",
    tags=["Cargo Diagram Calculate"],
)


@api_router.post(
    "",
    response_model=CalculateResponse,
    status_code=status.HTTP_200_OK,
)
async def run_calculate(
    _: Request,
    body: Annotated[CalculateRequest, Body(...)]
):
    result = await calculate_centers_of_mass(body)
    report = await get_report(body, result)
    return CalculateResponse(result=result, report=report).json()
