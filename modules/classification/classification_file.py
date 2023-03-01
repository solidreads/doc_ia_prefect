from google.cloud import documentai
from google.api_core.client_options import ClientOptions


# @task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def classify_file(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
):
    """ "
    function return the classification of the file
    according to the enums

    @TODO: validate if enums are the best options for classification
    """
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

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

    document = result.document

    entities = document.entities

    tipo_documento = [
        entity.mention_text
        for entity in entities
        if entity.type_ == "tipo-documento"
    ]

    print("tipo de documento: ", tipo_documento)
    return tipo_documento
