import datetime
from dataclasses import asdict, dataclass

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
    sello: str

    @classmethod
    def valida(
        cls,
        fecha: datetime.date,
        clave_rastreo: str,
        emisor: str,
        receptor: str,
        cuenta: str,
        monto: float,
    ):
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
        client.post('/valida.do', request_body)
        resp_content = client.get('/descarga.do?formato=XML')
        resp = etree.fromstring(resp_content)

        ordenante = Cuenta.from_etree(resp.find('Ordenante'))
        beneficiario = Cuenta.from_etree(resp.find('Beneficiario'))
        concepto = resp.find('Beneficiario').get('Concepto')
        fecha_operacion = iso8601.parse_date(
            resp.get('FechaOperacion') + ' ' + resp.get('Hora'), None)

        transferencia = cls(
            fecha_operacion=fecha_operacion,
            ordenante=ordenante,
            beneficiario=beneficiario,
            monto=monto,
            concepto=concepto,
            sello=resp.get('sello'),
        )
        transferencia.__client = client
        return transferencia

    def descarga(self, formato: str = 'PDF') -> bytes:
        # formato puede ser PDF, XML o ZIP
        return self.__client.get(f'/descarga.do?formato={formato}')

    def to_dict(self):
        return asdict(self)
