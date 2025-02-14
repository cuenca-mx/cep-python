class CepError(Exception):
    """
    Error interno del sitio web
    https://www.banxico.org.mx/cep/
    """


class NotFoundError(CepError):
    """
    No se encontró el CEP de una transferencia
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
