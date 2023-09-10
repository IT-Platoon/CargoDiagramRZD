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
    doc.add_paragraph(f"Поперечное смещение в вагоне: b = {1} мм")
    doc.add_paragraph(f"Поперечное смещение с вагоном: b = {2} мм")
    doc.add_paragraph(f"Высота центра тяжести в вагоне: H(цт О) = {1} мм")
    doc.add_paragraph(f"Общая высота ЦТ: H(цт) = {result['general_height_center_gravity']} мм")
    doc.add_paragraph(f"Удельная продольная инерционная сила на одну тонну веса груза: а(пр) = {1} тс/с")
    doc.add_paragraph(f"Продольная инерционная сила: F(пр) = {2} тс")
    doc.add_paragraph(f"Ветровая нагрузка: W(е) = {3} тс")
    doc.add_paragraph(f"Сила трения в продольном направлении: F(пр тр) = {4} тс")
    doc.save(docxfile.name)


async def get_report(result: dict) -> str:
    with tempfile.NamedTemporaryFile(mode="rb+", suffix=".docx") as docxfile:
        await create_document(result, docxfile)
        docxfile.seek(0)
        report = base64.b64encode(docxfile.read()).decode()
    return report
