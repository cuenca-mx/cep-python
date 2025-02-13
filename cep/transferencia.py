import datetime
from dataclasses import asdict, dataclass
from decimal import Decimal
from typing import cast

import clabe
from lxml import etree
from requests import HTTPError

from .client import Client
from .cuenta import Cuenta
from .exc import CepError, MaxRequestError, NotFoundError

MAX_REQUEST_ERROR_MESSAGE = (
    b'Lo sentimos, pero ha excedido el n&uacute;mero m&aacute;ximo '
    b'de consultas en este portal'
)

NOT_FOUND_ERROR_MESSAGE = (
    'No se encontró ningún pago con la información proporcionada'
)


@dataclass
class Transferencia:
    fecha_operacion: datetime.date
    fecha_abono: datetime.datetime
    ordenante: Cuenta
    beneficiario: Cuenta
    monto: Decimal
    iva: Decimal
    concepto: str
    clave_rastreo: str
    emisor: str
    receptor: str
    sello: str
    tipo_pago: int
    pago_a_banco: bool = False

    @classmethod
    def validar(
        cls,
        fecha: datetime.date,
        clave_rastreo: str,
        emisor: str,
        receptor: str,
        cuenta: str,
        monto: Decimal,
        pago_a_banco: bool = False,
    ):
        client = cls._validar(
            fecha, clave_rastreo, emisor, receptor, cuenta, monto, pago_a_banco
        )

        try:
            xml = cls._descargar(client, 'XML')
        except HTTPError as exc:
            raise CepError from exc

        if MAX_REQUEST_ERROR_MESSAGE in xml:
            raise MaxRequestError

        resp = etree.fromstring(xml)

        ordenante_element = cast(etree._Element, resp.find('Ordenante'))
        beneficiario_element = cast(etree._Element, resp.find('Beneficiario'))

        ordenante = Cuenta.from_etree(ordenante_element)
        beneficiario = Cuenta.from_etree(beneficiario_element)

        cadena_cda = resp.attrib['cadenaCDA'].split("|")

        # FechaAbono is not explicitly provided in response.
        # It can be extracted from the CDA string.
        fecha_abono_str = (
            f"{cadena_cda[4][4:]}-{cadena_cda[4][2:4]}-{cadena_cda[4][:2]}"
        )

        tipo_pago = cadena_cda[2]

        fecha_operacion = datetime.date.fromisoformat(
            resp.attrib['FechaOperacion']
        )

        hora_abono = resp.attrib['Hora']
        fecha_abono = datetime.datetime.fromisoformat(
            f'{fecha_abono_str} {hora_abono}'
        )

        iva = beneficiario_element.attrib['IVA']
        concepto = beneficiario_element.attrib['Concepto']
        sello = resp.attrib['sello']

        transferencia = cls(
            fecha_operacion=fecha_operacion,
            fecha_abono=fecha_abono,
            ordenante=ordenante,
            beneficiario=beneficiario,
            monto=monto,
            iva=Decimal(iva),
            concepto=concepto,
            clave_rastreo=clave_rastreo,
            emisor=emisor,
            receptor=receptor,
            sello=sello,
            tipo_pago=int(tipo_pago),
        )
        setattr(transferencia, '__client', client)
        return transferencia

    def descargar(self, formato: str = 'PDF') -> bytes:
        """formato puede ser PDF, XML o ZIP"""
        client = getattr(self, '__client', None)
        if not client:
            client = self._validar(
                self.fecha_abono.date(),
                self.clave_rastreo,
                self.emisor,
                self.receptor,
                self.beneficiario.numero,
                self.monto,
                self.pago_a_banco,
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
        monto: Decimal,
        pago_a_banco: bool = False,
    ) -> Client:
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
            receptorParticipante=1 if pago_a_banco else 0,
        )
        resp = client.post('/valida.do', request_body)
        if (
            NOT_FOUND_ERROR_MESSAGE in resp.decode('utf-8')
            or b'no encontrada' in resp
        ):
            raise NotFoundError
        return client

    @staticmethod
    def _descargar(client: Client, formato: str = 'PDF') -> bytes:
        """formato puede ser PDF, XML o ZIP"""
        return client.get(f'/descarga.do?formato={formato}')
