import enum


class TiposDeArchivoEnum(enum.Enum):
    CONFIDENCIAL_REGISTRO_MAESTRO_DE_SURTIDO_DE_MATERIAS_PRIMAS = {
        "numero": 1,
        "coincidencias": [
            "CONFIDENCIAL REGISTRO MAESTRO DE SURTIDO DE MATERIAS PRIMAS",
        ],
    }
    CONFIDENCIAL_REGISTRO_MAESTRO_DE_RECEPCION_DE_MATERIALES = {
        "numero": 2,
        "coincidencias": [
            "CONFIDENCIAL REGISTRO MAESTRO DE RECEPCIÓN DE MATERIALES"
        ],
    }
    CONFIDENCIAL_REGISTRO_MAESTRO_DE_FABRICACION = {
        "numero": 3,
        "coincidencias": ["CONFIDENCIAL REGISTRO MAESTRO DE FABRICACION"],
    }
    CONFIDENCIAL_REGISTRO_MAESTRO_DE_ENVASE = {
        "numero": 4,
        "coincidencias": ["CONFIDENCIAL REGISTRO MAESTRO DE ENVASE"],
    }
    CONFIDENCIAL_REGISTRO_MAESTRO_DE_LLENADO_DE_CARROS = {
        "numero": 5,
        "coincidencias": [
            "CONFIDENCIAL REGISTRO MAESTRO DE LLENADO DE CARROS"
        ],
    }
    LISTA_DE_VERIFICACION_LIBERACION_DE_EXPEDIENTE_DE_FABRICACION_SUEROS_PLASTICOS = {
        "numero": 6,
        "coincidencias": [
            "LISTA DE VERIFICACIÓN: LIBERACIÓN DE EXPEDIENTE DE FABRICACIÓN SUEROS PLASTICOS"
        ],
    }
