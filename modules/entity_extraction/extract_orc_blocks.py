import json
from typing import Sequence

from prefect import task
from google.cloud import documentai

from shared.shared import layout_to_text


@task
def extract_ocr_blocks(
    document: documentai.Document,
    path: str,
) -> Sequence[documentai.Document.Page.Block]:
    """
    Get blocks from document.
    :param document:
    :return  blocks:
    """
    text = document.text

    blocks_list = []
    #
    for page in document.pages:
        blocks_dict = {
            "page_number": page.page_number,
            "total_blocks": len(page.blocks),
            "confidence_blocks_average": "",
            "list_blocks": [],
        }
        for block in page.blocks:
            composition = {
                "confidence": round(block.layout.confidence, 2),
                "text": layout_to_text(block.layout, text),
            }
            blocks_dict["list_blocks"].append(composition)

        blocks_list.append(blocks_dict)

    # get average confidence
    for page in blocks_list:
        confidence_blocks = []
        for block in page["list_blocks"]:
            confidence_blocks.append(block["confidence"])
        page["confidence_blocks_average"] = round(
            sum(confidence_blocks) / len(confidence_blocks), 2
        )

    blocks_json = json.dumps(blocks_list, ensure_ascii=False)
    with open("log/blocks_dict_log.json", "w", encoding="utf-8") as f:
        f.write(blocks_json)
    return blocks_list
