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
    doc.add_paragraph(f"Поперечное смещение в вагоне: b = {result['lateral_displacement_in_car']} мм")
    doc.add_paragraph(f"Поперечное смещение с вагоном: b = {result['lateral_displacement_with_car']} мм")
    doc.add_paragraph(f"Высота центра тяжести в вагоне: H(цт О) = {result['height_center_gravity_in_car']} мм")
    doc.add_paragraph(f"Общая высота ЦТ: H(цт) = {result['general_height_center_gravity']} мм")
    doc.add_paragraph(f"Расчет наветренной поверхности: S(bok) = {result['windward_surface']} м2")
    doc.add_paragraph(f"Удельная продольная инерционная сила на одну тонну веса груза: а(пр) = {result['specific_length_inertial_force_per_ton_cargo_weight']} тс/с")
    for i in range(len(result['longitudinal_inertial_force'])):
        doc.add_heading(f'Груз {i+1}', 3)
        doc.add_paragraph(f"Продольная инерционная сила: F(пр) = {result['longitudinal_inertial_force'][i]} тс", style='List Bullet 2')
        doc.add_paragraph(f"Ветровая нагрузка: W(е) = {result['wind_load'][i]} тс", style='List Bullet 2')
        doc.add_paragraph(f"Сила трения в продольном направлении: F(пр тр) = {result['friction_force_longitudinal_direction'][i]} тс", style='List Bullet 2')
    doc.save(docxfile.name)


async def get_report(result: dict) -> str:
    with tempfile.NamedTemporaryFile(mode="rb+", suffix=".docx") as docxfile:
        await create_document(result, docxfile)
        docxfile.seek(0)
        report = base64.b64encode(docxfile.read()).decode()
    return report
