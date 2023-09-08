import base64
import tempfile

from app.schemas import CalculateRequest


async def get_report(body: CalculateRequest, result: dict) -> bytes:
    with tempfile.TemporaryFile(mode="w+", suffix=".docx") as docxfile:
        # создание файла
        report = base64.b64encode(docxfile.read()).decode()
    return report
