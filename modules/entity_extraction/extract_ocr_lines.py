import json
from typing import List

from prefect import task
from google.cloud import documentai

from shared.shared import layout_to_text


@task
def read_ocr_by_line(document: documentai.Document, path: str) -> List[str]:
    """Reads the text from the document and returns a list of blocks"""
    text = document.text
    lines_list = []
    for page in document.pages:
        list_line = {
            "page_number": page.page_number,
            "total_lines": len(page.lines),
            "confidence_line_average": "",
            "list_lines": [],
        }
        for line in page.lines:
            composition = {
                "confidence": round(line.layout.confidence, 2),
                "text": layout_to_text(line.layout, text),
            }
            list_line["list_lines"].append(composition)
        lines_list.append(list_line)

    # get average confidence
    for page in lines_list:
        confidence_lines = []
        for line in page["list_lines"]:
            confidence_lines.append(line["confidence"])
        page["confidence_line_average"] = round(
            sum(confidence_lines) / len(confidence_lines), 2
        )

    list_json = json.dumps(lines_list, ensure_ascii=False)
    with open("log/line_ocr_log.json", "w", encoding="utf-8") as f:
        f.write(list_json)

    return lines_list
