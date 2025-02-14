class CepError(Exception):
    """
    Error interno del sitio web
    https://www.banxico.org.mx/cep/
    """


class TransferNotFoundError(CepError):
    """
    No se encontró la transferencia con
    los datos proporcionados
    """


class MaxRequestError(CepError):
    """
    Máximo número de peticiones alcanzadas para
    obtener el CEP de una transferencia
    """


class CepNotAvailableError(CepError):
    """
    La transferencia fue encontrada, pero el CEP no
    está disponible.
    """
