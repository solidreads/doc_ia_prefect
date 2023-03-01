""""
    Function that identifies the quality of a pdf
"""
import json

from prefect import task, get_run_logger
from google.cloud import documentai


@task
def get_quality(document: documentai.Document, path: str) -> list:
    """
    This functions returns a list of dictionaries with the quality of the pdf
    :param document:
    :return: list [{'page_number': 1,
                 'quality_score': 0.7350051403045654,
                 'detected_defects': [
                 'quality/defect_document_cutoff: 100.0%',
                  'quality/defect_glare: 61.9%',
                  'quality/defect_text_cutoff: 50.0%']}
                ]
    """

    quality_stats_list: list = []
    quality_stats_list.append({"document": path})

    for page in document.pages:
        list_detected_defects: list = []
        for detected_defect in page.image_quality_scores.detected_defects:
            defect = (
                f"{detected_defect.type_}: {detected_defect.confidence:.1%}"
            )
            list_detected_defects.append(defect)

        quality_stats = {
            "page_number": page.page_number,
            "orientation": page.layout.orientation,
            "quality_score": page.image_quality_scores.quality_score,
            "detected_defects": list_detected_defects,
        }

        quality_stats_list.append(quality_stats)

    with open("log/get_quality_log.json", "w") as archivo:
        json.dump(quality_stats_list, archivo, indent=4)
    archivo.close()

    logger = get_run_logger()
    logger.info("Se genero el log de calidad en el pdf.")
    return quality_stats_list


@task
def get_quality_after_rotate(document: documentai.Document, path: str) -> list:
    """
    This functions returns a list of dictionaries with the quality of the pdf
    :param document:
    :return: list [{'page_number': 1,
                 'quality_score': 0.7350051403045654,
                 'detected_defects': [
                 'quality/defect_document_cutoff: 100.0%',
                  'quality/defect_glare: 61.9%',
                  'quality/defect_text_cutoff: 50.0%']}
                ]
    """

    quality_stats_list: list = []
    quality_stats_list.append({"document": path})

    for page in document.pages:
        list_detected_defects: list = []
        for detected_defect in page.image_quality_scores.detected_defects:
            defect = (
                f"{detected_defect.type_}: {detected_defect.confidence:.1%}"
            )
            list_detected_defects.append(defect)

        quality_stats = {
            "page_number": page.page_number,
            "orientation": page.layout.orientation,
            "quality_score": page.image_quality_scores.quality_score,
            "detected_defects": list_detected_defects,
        }

        quality_stats_list.append(quality_stats)

    with open("log/get_quality_after_roate_log.json", "w") as archivo:
        json.dump(quality_stats_list, archivo, indent=4)
    archivo.close()

    logger = get_run_logger()
    logger.info("Se genero el log de calidad en el pdf.")
    return quality_stats_list
