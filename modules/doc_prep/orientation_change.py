import PyPDF2
from prefect import task


@task
def rotate_pdf(file_path: str, output_path: str) -> None:
    """Rotates a PDF file 90 degrees clockwise and saves it to a new file.

    Args:
        file_path (str): Path to the input PDF file.
        output_path (str): Path to the output PDF file.
    """

    with open(file_path, "rb") as archivo:
        lector = PyPDF2.PdfReader(archivo)
        escritor = PyPDF2.PdfWriter()

        # Recorremos todas las páginas del archivo
        for i in range(len(lector.pages)):
            pagina = lector.pages[i]

            # Rotamos la página 90 grados en sentido antihorario
            pagina.rotate(90)

            # Agregamos la página rotada al archivo de salida
            escritor.add_page(pagina)

        # Guardamos el archivo de salida con el nombre "archivo_rotado.pdf"
        with open(f"log/rotated_file.pdf", "wb") as archivo_salida:
            escritor.write(archivo_salida)


@task
def get_orientation(file_path: str) -> str:
    """Returns the orientation of the pdf.

    Args:
        file_path (str): Path to the input PDF file.

    Returns:
        str: Orientation of the pdf.
    """
    with open(file_path, "rb") as archivo:
        reader = PyPDF2.PdfReader(archivo)
        for i in range(len(reader.pages)):
            reader.pages[i]
            rotation = reader.pages[i].get("/Rotate", 0)

            print(f"rotation: {rotation}")
            if rotation == 0:
                print("La orientación del PDF es horizontal")
            elif rotation == 90:
                print(
                    "La orientación del PDF es vertical (rotado 90 grados en sentido contrario a las manecillas del reloj)"
                )
            elif rotation == 270:
                print(
                    "La orientación del PDF es vertical (rotado 90 grados en sentido de las manecillas del reloj)"
                )
            else:
                print("La orientación del PDF es diagonal o desconocida")

    # with open(file_path, "rb") as archivo:
    #     lector = PyPDF2.PdfReader(archivo)
    #
    #     # Recorremos todas las páginas del archivo
    #     for i in range(len(lector.pages)):
    #         pagina = lector.pages[i]
    #         orientation = lector.pages[i].get("/Rotate", 0)
    #         print(orientation)
    #         if orientation > 0:
    #             return "portrait"
    #         else:
    #             return "landscape"
