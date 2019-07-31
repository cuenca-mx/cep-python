from dataclasses import dataclass

from lxml import etree


@dataclass
class Cuenta:
    nombre: str
    tipo: str
    banco: str
    numero: str
    rfc: str

    @classmethod
    def from_etree(cls, element: etree._Element):
        cuenta = cls(
            nombre=element.get('Nombre'),
            tipo=element.get('TipoCuenta'),
            banco=element.get('BancoEmisor') or element.get('BancoReceptor'),
            numero=element.get('Cuenta'),
            rfc=element.get('RFC'),
        )
        return cuenta
