import base64
import tempfile

from docx import Document


async def create_document(
    result: dict,
    docxfile: tempfile.NamedTemporaryFile,
) -> None:
    doc = Document()
    doc.add_paragraph(f"Продольное смещение грузов в вагоне: l(c) = {result['longitudinal_displacement_in_car']} мм")
    doc.add_paragraph(f"Продольное смещение грузов с вагоном: l(c) = {result['longitudinal_displacement_with_car']} мм")
    doc.add_paragraph(f"Общая высота ЦТ: H(цт) = {result['general_height_center_gravity']} мм")
    doc.save(docxfile.name)


async def get_report(result: dict) -> str:
    with tempfile.NamedTemporaryFile(mode="rb+", suffix=".docx") as docxfile:
        await create_document(result, docxfile)
        docxfile.seek(0)
        report = base64.b64encode(docxfile.read()).decode()
    return report
