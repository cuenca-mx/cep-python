from dataclasses import dataclass
from typing import Optional

from lxml import etree


@dataclass
class Cuenta:
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    banco: Optional[str] = None
    numero: Optional[str] = None
    rfc: Optional[str] = None

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
