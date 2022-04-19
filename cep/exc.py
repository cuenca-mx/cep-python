class CepError(Exception):
    """
    Error interno del sitio web
    https://www.banxico.org.mx/cep/
    """


class MaxRequestError(CepError):
    """
    Máximo número de peticiones alcanzadas para
    obtener el CEP de una transferencia
    """
