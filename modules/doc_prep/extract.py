from datetime import timedelta

from prefect.tasks import task_input_hash
from prefect import task
from google.cloud import documentai
from google.api_core.client_options import ClientOptions


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(minutes=30))
def extract(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
) -> documentai.Document:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor version
    # e.g. projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}
    # You must create processors before running sample code.
    name = client.processor_version_path(
        project_id, location, processor_id, processor_version
    )

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load Binary Data into Document AI RawDocument Object
    raw_document = documentai.RawDocument(
        content=image_content, mime_type=mime_type
    )

    # Configure the process request
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)

    return result.document
