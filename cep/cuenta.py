from dataclasses import dataclass

from lxml import etree


@dataclass
class Cuenta:
    nombre: str
    tipo_cuenta: str
    banco: str
    numero: str
    rfc: str

    @classmethod
    def from_etree(cls, element: etree._Element):
        banco = (
            element.attrib['BancoEmisor']
            if 'BancoEmisor' in element.attrib
            else element.attrib['BancoReceptor']
        )

        return cls(
            nombre=element.attrib['Nombre'],
            tipo_cuenta=element.attrib['TipoCuenta'],
            banco=banco,
            numero=element.attrib['Cuenta'],
            rfc=element.attrib['RFC'],
        )
