import datetime
from dataclasses import asdict, dataclass
from typing import Optional

import clabe
import requests
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
    ) -> Optional["Transferencia"]:
        """
        validar CEP.

        Deprecated, use TransferenciaClient instead.
        """
        client = TransferenciaClient()
        tr = client.validar(
            fecha=fecha,
            clave_rastreo=clave_rastreo,
            emisor=emisor,
            receptor=receptor,
            cuenta=cuenta,
            monto=monto,
        )
        if tr is not None:
            setattr(tr, '__client', client)
        return tr

    def descargar(self, formato: str = "PDF") -> bytes:
        """
        formato puede ser PDF, XML o ZIP.

        Deprecated, use TransferenciaClient instead.
        """
        client: Optional[TransferenciaClient] = getattr(self, '__client', None)
        if client is None:
            client = TransferenciaClient()
            client._validar(
                fecha=self.fecha_operacion.date(),
                clave_rastreo=self.clave_rastreo,
                emisor=self.emisor,
                receptor=self.receptor,
                cuenta=self.beneficiario.numero,
                monto=self.monto,
            )
        return client.descargar(formato)

    def to_dict(self) -> dict:
        return asdict(self)


class TransferenciaClient:
    """
    Python client library for CEP (http://www.banxico.org.mx/cep/)
    """

    def __init__(self, session: requests.Session = None) -> None:
        self.__client = Client(session=session)

    def __enter__(self):
        self.__client.__enter__()
        return self

    def __exit__(self, *args, **kwargs):
        self.__client.__exit__(*args, **kwargs)

    def validar(
        self,
        fecha: datetime.date,
        clave_rastreo: str,
        emisor: str,
        receptor: str,
        cuenta: str,
        monto: float,
    ) -> Optional[Transferencia]:
        """validar CEP."""
        is_success = self._validar(
            fecha=fecha,
            clave_rastreo=clave_rastreo,
            emisor=emisor,
            receptor=receptor,
            cuenta=cuenta,
            monto=monto,
        )
        if not is_success:
            return None
        xml = self._descargar("XML")
        resp = etree.fromstring(xml)

        ordenante = Cuenta.from_etree(resp.find("Ordenante"))
        beneficiario = Cuenta.from_etree(resp.find("Beneficiario"))
        concepto = resp.find("Beneficiario").get("Concepto")
        fecha_operacion = datetime.datetime.fromisoformat(
            str(fecha) + " " + resp.get("Hora")
        )
        transferencia = Transferencia(
            fecha_operacion=fecha_operacion,
            ordenante=ordenante,
            beneficiario=beneficiario,
            monto=monto,
            concepto=concepto,
            clave_rastreo=clave_rastreo,
            emisor=emisor,
            receptor=receptor,
            sello=resp.get("sello"),
        )
        return transferencia

    def descargar(self, formato: str = "PDF") -> bytes:
        """formato puede ser PDF, XML o ZIP."""
        return self._descargar(formato)

    def _validar(
        self,
        fecha: datetime.date,
        clave_rastreo: str,
        emisor: str,
        receptor: str,
        cuenta: str,
        monto: float,
    ) -> bool:
        assert emisor in clabe.BANKS.values()
        assert receptor in clabe.BANKS.values()
        request_body = dict(
            fecha=fecha.strftime("%d-%m-%Y"),
            criterio=clave_rastreo,
            emisor=emisor,
            receptor=receptor,
            cuenta=cuenta,
            monto=monto,
        )
        resp = self.__client.post("/valida.do", request_body)
        # None si no pudó validar
        is_success = b"no encontrada" not in resp
        return is_success

    def _descargar(self, formato: str = "PDF") -> bytes:
        """formato puede ser PDF, XML o ZIP."""
        return self.__client.get(f"/descarga.do?formato={formato}")
