#!/usr/bin/env python3
"""Generate a simple ГОСТ-style DOCX report without external dependencies."""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "report" / "MLSD_case2_face_access_control.docx"


def t(text: str) -> str:
    return escape(text, {'"': "&quot;"})


def run(text: str, bold: bool = False, size: int = 28) -> str:
    b = "<w:b/>" if bold else ""
    return (
        "<w:r><w:rPr>"
        f"{b}<w:rFonts w:ascii=\"Times New Roman\" w:hAnsi=\"Times New Roman\" w:cs=\"Times New Roman\"/>"
        f"<w:sz w:val=\"{size}\"/><w:szCs w:val=\"{size}\"/>"
        "</w:rPr>"
        f"<w:t xml:space=\"preserve\">{t(text)}</w:t></w:r>"
    )


def paragraph(text: str = "", *, style: str | None = None, align: str | None = None, bold: bool = False, size: int = 28, indent: bool = True) -> str:
    ppr_parts = []
    if style:
        ppr_parts.append(f"<w:pStyle w:val=\"{style}\"/>")
    if align:
        ppr_parts.append(f"<w:jc w:val=\"{align}\"/>")
    if indent and not style:
        ppr_parts.append("<w:ind w:firstLine=\"708\"/>")
    ppr_parts.append("<w:spacing w:line=\"360\" w:lineRule=\"auto\" w:after=\"120\"/>")
    ppr = f"<w:pPr>{''.join(ppr_parts)}</w:pPr>"
    return f"<w:p>{ppr}{run(text, bold=bold, size=size)}</w:p>"


def heading(text: str, level: int = 1) -> str:
    style = "Heading1" if level == 1 else "Heading2"
    size = 32 if level == 1 else 30
    return paragraph(text, style=style, bold=True, size=size, indent=False)


def bullet(text: str) -> str:
    return (
        "<w:p><w:pPr><w:ind w:left=\"720\" w:hanging=\"360\"/>"
        "<w:spacing w:line=\"360\" w:lineRule=\"auto\" w:after=\"80\"/></w:pPr>"
        f"{run('• ' + text)}</w:p>"
    )


def page_break() -> str:
    return "<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>"


def table(rows: list[list[str]]) -> str:
    xml = ["<w:tbl><w:tblPr><w:tblStyle w:val=\"TableGrid\"/><w:tblW w:w=\"0\" w:type=\"auto\"/></w:tblPr>"]
    for row_idx, row in enumerate(rows):
        xml.append("<w:tr>")
        for cell in row:
            xml.append("<w:tc><w:tcPr><w:tcW w:w=\"3000\" w:type=\"dxa\"/></w:tcPr>")
            xml.append(paragraph(cell, bold=row_idx == 0, indent=False))
            xml.append("</w:tc>")
        xml.append("</w:tr>")
    xml.append("</w:tbl>")
    return "".join(xml)


def sect_pr() -> str:
    return (
        "<w:sectPr>"
        "<w:pgSz w:w=\"11906\" w:h=\"16838\"/>"
        "<w:pgMar w:top=\"1134\" w:right=\"567\" w:bottom=\"1134\" w:left=\"1701\" w:header=\"708\" w:footer=\"708\" w:gutter=\"0\"/>"
        "</w:sectPr>"
    )


def build_document() -> str:
    body: list[str] = []

    body.extend(
        [
            paragraph("[НАЗВАНИЕ ВУЗА]", align="center", bold=True, indent=False),
            paragraph("[ИНСТИТУТ / ФАКУЛЬТЕТ]", align="center", indent=False),
            paragraph("[КАФЕДРА]", align="center", indent=False),
            paragraph("", indent=False),
            paragraph("", indent=False),
            paragraph("ОТЧЕТ ПО ПРОЕКТУ", align="center", bold=True, size=32, indent=False),
            paragraph("по дисциплине «Проектирование информационных систем»", align="center", indent=False),
            paragraph("", indent=False),
            paragraph("Кейс №2. Система идентификации личности по фотографии для контроля доступа на промышленном предприятии", align="center", bold=True, indent=False),
            paragraph("", indent=False),
            paragraph("Выполнили: Егор, Артём, Максим", align="right", indent=False),
            paragraph("Группа: [указать группу]", align="right", indent=False),
            paragraph("Проверил: [ФИО преподавателя]", align="right", indent=False),
            paragraph("", indent=False),
            paragraph("", indent=False),
            paragraph("[Город] — 2026", align="center", indent=False),
            page_break(),
        ]
    )

    body.append(heading("Содержание", 1))
    for item in [
        "1. Название кейса и состав команды",
        "2. Цели и предпосылки",
        "3. Методология ML",
        "4. Подготовка пилота",
        "5. Production-архитектура",
        "6. Данные и диаграммы",
        "7. Риски",
        "8. Вывод",
    ]:
        body.append(paragraph(item, indent=False))
    body.append(page_break())

    body.append(heading("1. Название кейса и состав команды", 1))
    body.append(paragraph("Кейс №2: автоматизированная система идентификации личности по фотографии для контроля доступа на промышленном предприятии."))
    body.append(table([
        ["Участник", "Роль", "Ответственность"],
        ["Егор", "Product Owner / системный аналитик", "Бизнес-цели, требования, сценарии, критерии пилота"],
        ["Артём", "Data Scientist / ML-инженер", "ML-подход, метрики, эксперименты, модельные риски"],
        ["Максим", "Data Engineer / Data Architect", "Данные, архитектура хранения, интеграции, эксплуатация"],
    ]))

    body.append(heading("2. Цели и предпосылки", 1))
    body.append(paragraph("На предприятии около 5000 сотрудников и 10 проходных. Сейчас дежурный вручную сравнивает человека с фотографией в профиле после сканирования пластикового пропуска. Процесс зависит от внимательности оператора, плохо масштабируется в часы пик и не защищает от передачи пропуска другому человеку."))
    body.append(paragraph("Цель проекта — создать информационную систему с ML-модулем, которая автоматически проверяет соответствие лица сотрудника его пропуску, ускоряет проход через КПП, снижает субъективность проверки и сохраняет полный аудит решений."))
    for item in [
        "сокращение среднего времени проверки до 2 секунд;",
        "снижение риска прохода по чужому пропуску;",
        "автоматизация типовых проходов и ручная проверка только спорных случаев;",
        "полное журналирование решений системы и действий оператора;",
        "учет требований к персональным и биометрическим данным.",
    ]:
        body.append(bullet(item))

    body.append(heading("3. Методология ML", 1))
    body.append(paragraph("Основная ML-задача MVP — face verification: сотрудник предъявляет пропуск, а система сравнивает лицо перед камерой с эталонным биометрическим шаблоном владельца пропуска. Face identification по всей базе сотрудников рассматривается как развитие после успешного пилота."))
    body.append(paragraph("Пайплайн включает детекцию лица, оценку качества кадра, извлечение embedding-вектора, сравнение с эталоном, применение порога и запись результата."))
    body.append(table([
        ["Метрика", "Смысл", "Связь с бизнесом"],
        ["FAR", "Доля чужих лиц, ошибочно допущенных системой", "Главный риск безопасности"],
        ["FRR", "Доля своих сотрудников, не прошедших автоматически", "Очереди и нагрузка на КПП"],
        ["TAR при заданном FAR", "Корректные допуски при фиксированном уровне безопасности", "Выбор рабочего порога"],
        ["p95 latency", "Задержка 95% проверок", "Пропускная способность КПП"],
        ["Доля ручных проверок", "Сколько случаев ушло оператору", "Экономический эффект"],
    ]))

    body.append(heading("4. Подготовка пилота", 1))
    body.append(paragraph("Пилот проводится на 1-2 проходных и группе 300-500 сотрудников. Сначала система работает в теневом режиме, затем допускается автоматическое открытие турникета при высокой уверенности. Спорные случаи передаются оператору."))
    body.append(table([
        ["Критерий", "Целевое значение"],
        ["p95 времени проверки", "не более 2 секунд"],
        ["Автоматические штатные проходы", "не менее 90%"],
        ["Ложные допуски", "0 в пилоте или ниже согласованного порога"],
        ["Полнота журнала", "100% решений записаны"],
        ["Доступность пилотного контура", "не ниже 98.5%"],
    ]))

    body.append(heading("5. Production-архитектура", 1))
    body.append(paragraph("Архитектура гибридная: на каждой проходной есть камера, терминал и edge-узел, а центральные сервисы отвечают за Access Control API, ML Inference, Employee DB, Vector Storage, Audit Log и Monitoring. Распределенность нужна из-за 10 физических КПП и требования низкой задержки."))
    for item in [
        "Камера КПП получает изображение лица.",
        "Edge-узел выполняет предварительную обработку и буферизует события.",
        "Access Control API принимает решение о доступе.",
        "ML Inference Service извлекает embedding и сравнивает его с эталоном.",
        "Vector Storage хранит биометрические шаблоны.",
        "Audit Log хранит неизменяемую историю решений.",
    ]:
        body.append(bullet(item))

    body.append(heading("6. Данные и диаграммы", 1))
    body.append(paragraph("В репозитории подготовлены диаграммы бизнес-процессов AS-IS и TO-BE, ER-диаграмма данных, диаграмма архитектуры, UML-диаграмма компонентов и UML-диаграмма последовательности."))
    body.append(table([
        ["Диаграмма", "Файл"],
        ["Бизнес-процесс AS-IS", "diagrams/business-process-as-is.mmd"],
        ["Бизнес-процесс TO-BE", "diagrams/business-process-to-be.mmd"],
        ["ER-диаграмма данных", "diagrams/data-er-diagram.mmd"],
        ["Архитектура системы", "diagrams/system-architecture.mmd"],
        ["UML-компоненты", "diagrams/uml-components.mmd"],
        ["UML-последовательность", "diagrams/uml-sequence-access.mmd"],
    ]))

    body.append(heading("7. Риски", 1))
    body.append(table([
        ["Риск", "Влияние", "Мера снижения"],
        ["Ложный допуск", "Критический риск безопасности", "Строгий порог и ручная проверка спорных случаев"],
        ["Ложный отказ", "Очереди и недовольство сотрудников", "Настройка порогов и улучшение эталонных фото"],
        ["Утечка биометрии", "Юридический и репутационный риск", "Шифрование, RBAC, аудит, минимизация хранения фото"],
        ["Сбой сети или ML-сервиса", "Остановка автоматической проверки", "Edge-буфер и ручной режим"],
        ["Недоверие операторов", "Обход системы", "Обучение и понятное объяснение решений"],
    ]))

    body.append(heading("8. Вывод", 1))
    body.append(paragraph("Проект описывает не только ML-модель, но и полноценную информационную систему: бизнес-процессы, данные, архитектуру, требования, пилот, эксплуатацию и риски. Для MVP выбран сценарий «пропуск + лицо», потому что он дает быстрый эффект, снижает риск ложной идентификации и хорошо подходит для защищенного промышленного объекта. После успешного пилота систему можно масштабировать на все 10 проходных и развивать в сторону идентификации без пропуска."))

    body.append(sect_pr())
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{''.join(body)}</w:body></w:document>"
    )


CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
"""

RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>
"""

STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="180" w:after="100"/><w:outlineLvl w:val="1"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="30"/></w:rPr>
  </w:style>
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
    <w:tblPr><w:tblBorders>
      <w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      <w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      <w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      <w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      <w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      <w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>
    </w:tblBorders></w:tblPr>
  </w:style>
</w:styles>
"""

CORE = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>MLSD Case 2 Face Access Control</dc:title>
  <dc:creator>Егор, Артём, Максим</dc:creator>
</cp:coreProperties>
"""

APP = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
  <Application>Microsoft Office Word</Application>
</Properties>
"""


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUT, "w", ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/document.xml", build_document())
        z.writestr("word/styles.xml", STYLES)
        z.writestr("docProps/core.xml", CORE)
        z.writestr("docProps/app.xml", APP)
    print(OUT)


if __name__ == "__main__":
    main()
