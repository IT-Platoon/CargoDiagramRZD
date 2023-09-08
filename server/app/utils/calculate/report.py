import tempfile

from fastapi import Response

from app.schemas import CalculateRequest


async def get_report(body: CalculateRequest, result: dict) -> Response:
    with tempfile.TemporaryFile(mode="w+", suffix=".docx") as docxfile:
        # создание файла
        response = Response(
            docxfile.read(),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    return response
