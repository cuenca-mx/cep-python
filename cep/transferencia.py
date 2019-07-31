import datetime
from dataclasses import asdict, dataclass
from typing import Optional

import clabe
import iso8601
from lxml import etree

from .client import Client
from .cuenta import Cuenta


@dataclass
class Transferencia:
    fecha_operacion: datetime.datetime
    ordenante: Cuenta
    beneficiario: Cuenta
    monto: float
    concepto: str
    clave_rastreo: str
    emisor: str
    receptor: str
    sello: str

    @classmethod
    def validar(
        cls,
        fecha: datetime.date,
        clave_rastreo: str,
        emisor: str,
        receptor: str,
        cuenta: str,
        monto: float,
    ):
        client = cls._validar(
            fecha, clave_rastreo, emisor, receptor, cuenta, monto)
        if not client:
            return None
        xml = cls._descargar(client, 'XML')
        resp = etree.fromstring(xml)

        ordenante = Cuenta.from_etree(resp.find('Ordenante'))
        beneficiario = Cuenta.from_etree(resp.find('Beneficiario'))
        concepto = resp.find('Beneficiario').get('Concepto')
        fecha_operacion = iso8601.parse_date(
            resp.get('FechaOperacion') + ' ' + resp.get('Hora'), None
        )

        transferencia = cls(
            fecha_operacion=fecha_operacion,
            ordenante=ordenante,
            beneficiario=beneficiario,
            monto=monto,
            concepto=concepto,
            clave_rastreo=clave_rastreo,
            emisor=emisor,
            receptor=receptor,
            sello=resp.get('sello'),
        )
        transferencia.__client = client
        return transferencia

    def descargar(self, formato: str = 'PDF') -> bytes:
        """formato puede ser PDF, XML o ZIP"""
        client = getattr(self, '__client', None)
        if not client:
            client = self._validar(
                self.fecha_operacion.date(),
                self.clave_rastreo,
                self.emisor,
                self.receptor,
                self.beneficiario.numero,
                self.monto
            )
        return self._descargar(client, formato)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def _validar(
        fecha: datetime.date,
        clave_rastreo: str,
        emisor: str,
        receptor: str,
        cuenta: str,
        monto: float,
    ) -> Optional[Client]:
        assert emisor in clabe.BANKS.values()
        assert receptor in clabe.BANKS.values()
        client = Client()  # Use new client to ensure thread-safeness
        request_body = dict(
            fecha=fecha.strftime('%d-%m-%Y'),
            criterio=clave_rastreo,
            emisor=emisor,
            receptor=receptor,
            cuenta=cuenta,
            monto=monto,
        )
        resp = client.post('/valida.do', request_body)
        if b'no encontrada' in resp:
            client = None  # No pudó validar
        return client

    @staticmethod
    def _descargar(client: Client, formato: str = 'PDF') -> bytes:
        """formato puede ser PDF, XML o ZIP"""
        return client.get(f'/descarga.do?formato={formato}')
