"""
    Imprime en pantalla los datos de determinado tipo de bloque
"""

from typing import Sequence

from google.cloud import documentai


def print_paragraphs(
    paragraphs: Sequence[documentai.Document.Page.Paragraph], text: str
) -> None:
    print(f"    {len(paragraphs)} paragraphs detected:")
    first_paragraph_text = layout_to_text(paragraphs[0].layout, text)
    print(f"        First paragraph text: {repr(first_paragraph_text)}")
    last_paragraph_text = layout_to_text(paragraphs[-1].layout, text)
    print(f"        Last paragraph text: {repr(last_paragraph_text)}")


def print_all_blocks(
    blocks: Sequence[documentai.Document.Page.Block], text: str
) -> None:
    for block in blocks:
        print(
            f"Confianza del bloque"
            f" ================================= {block.layout.confidence:2f}"
        )
        block_text = layout_to_text(block.layout, text)
        print(block_text)


def print_image_quality_scores(
    image_quality_scores: documentai.Document.Page.ImageQualityScores,
) -> None:
    print(f"    Quality score: {image_quality_scores.quality_score:.1%}")
    print("    Detected defects:")

    for detected_defect in image_quality_scores.detected_defects:
        print(
            f"        {detected_defect.type_}: {detected_defect.confidence:.1%}"
        )


def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
    """
    Document AI identifies text in different parts of the document by their
    offsets in the entirety of the document's text. This function converts
    offsets to a string.
    """
    response = ""
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for segment in layout.text_anchor.text_segments:
        start_index = int(segment.start_index)
        end_index = int(segment.end_index)
        response += text[start_index:end_index]
    return response
