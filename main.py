"""
Simple ETL Pipeline from extract data from PDF using Document AI
"""
import json
import asyncio
import warnings
warnings.filterwarnings('ignore')


import pandas as pd
from datetime import datetime
from prefect import task, Flow, flow

from google.cloud import documentai

from settings import (
    PROJECT_ID,
    LOCATION,
    MIME_TYPE,
    PROCESSOR_ID_OCR,
    PROCESSOR_ID_OCR_VERSION,
    MIME_TYPE,
)
from settings import (
    PROCESSOR_CLASSIFICATION_ID,
    PROCESSOR_CLASSIFICATION_VERSION_ID
)

from modules.doc_prep.identify_quality_pdf import get_quality, get_quality_after_rotate
from modules.doc_prep.extract import extract
from modules.doc_prep.extract_ocr import extract_ocr

from modules.doc_prep.orientation_change import rotate_pdf
from modules.doc_prep.orientation_change import get_orientation

from modules.classification.classification_file import classify_file

from modules.entity_extraction.extract_orc_blocks import extract_ocr_blocks
from modules.entity_extraction.extract_ocr_lines import read_ocr_by_line

#FILE_PATH = "MBRs_PISA_23-27_01_2023/ultimos/PDFs_MBRs_PISA_MBR Electrolit Tlajomulco_M23F321_m23f321_20230223093340_1-5.pdf"

FILE_PATH = "MBRs_PISA_23-27_01_2023/Electrolit_coco_1000mL_H22T031/DOC033.pdf"
#FILE_PATH = "MBRs_PISA_23-27_01_2023/Electrolit_coco_1000mL_H22T031/DOC037.pdf"


FILE_PATH_ROTATE = "log/rotated_file.pdf"

ROTATION = True


@task
async def transform(data: dict) -> pd.DataFrame:
    pass


@task
async def load(data: pd.DataFrame, path: str) -> None:
    pass



@flow(log_prints=True)
async def prefect_flow():
    """  Doc Prep """
    document = extract(
        project_id=PROJECT_ID,
        location=LOCATION,
        processor_id=PROCESSOR_ID_OCR,
        processor_version=PROCESSOR_ID_OCR_VERSION,
        file_path=FILE_PATH,
        mime_type=MIME_TYPE,
    )
    quality_stats_list = get_quality(document=document, path=FILE_PATH)

    # TODO: determine if the flow can be broken after a certain quality score

    # extract_ocr(document=document, path=FILE_PATH)

    if ROTATION:
        # get_orientation(file_path=FILE_PATH)

        rotate_pdf(file_path=FILE_PATH, output_path=FILE_PATH)

        # processing after rotate
        document_after_rotate = extract(
            project_id=PROJECT_ID,
            location=LOCATION,
            processor_id=PROCESSOR_ID_OCR,
            processor_version=PROCESSOR_ID_OCR_VERSION,
            file_path=FILE_PATH_ROTATE,
            mime_type=MIME_TYPE,
        )
        get_quality_after_rotate(document=document_after_rotate, path=FILE_PATH_ROTATE)

    # classification document type
    tipo_documento = classify_file(
        project_id=PROJECT_ID,
        location=LOCATION,
        processor_id=PROCESSOR_CLASSIFICATION_ID,
        processor_version=PROCESSOR_CLASSIFICATION_VERSION_ID,
        file_path=FILE_PATH,
        mime_type=MIME_TYPE,
    )

    """
    Entity Extraction
    """
    # extract ocr
    extract_ocr_blocks(document=document, path=FILE_PATH)
    read_ocr_by_line(document=document, path=FILE_PATH)

    # extract form parser

    # extract custom
    """
    Entity relationships
    """

    """
    Uptraining
    """

    """
    Repository
    """


if __name__ == '__main__':
    asyncio.run(prefect_flow())