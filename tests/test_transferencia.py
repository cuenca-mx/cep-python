import datetime as dt
import os

import pytest

from cep import Transferencia


@pytest.mark.vcr
def test_validar_transferencia(transferencia):
    tr = Transferencia.validar(
        fecha=dt.date(2019, 4, 12),
        clave_rastreo='CUENCA1555093850',
        emisor='90646',  # STP
        receptor='40012',  # BBVA
        cuenta='012180004643051249',
        monto=8.17,
    )
    assert tr == transferencia
    assert type(tr.to_dict()) is dict


@pytest.mark.vcr
def test_fail_validar_transferencia():
    tr = Transferencia.validar(
        fecha=dt.date(2019, 1, 1),
        clave_rastreo='guey',
        emisor='90646',
        receptor='40012',
        cuenta='012180004643051249',
        monto=1111111.00,
    )
    assert tr is None


@pytest.mark.vcr
def test_descarga_pdf(transferencia):
    pdf = transferencia.descargar()
    file_dir = os.path.dirname(__file__)
    file_path = os.path.join(file_dir, 'CEP-20190412-CUENCA1555093850.pdf')
    with open(file_path, 'rb') as f:
        assert pdf == f.read()


@pytest.mark.vcr
def test_descagar_transferencia_con_fecha_distinta(transferencia):
    tr = Transferencia.validar(
        fecha=dt.date(2019, 8, 29),
        clave_rastreo='MBAN01001908300003463991',
        emisor='40012',  # BBVA
        receptor='90646',  # STP
        cuenta='646180157048010399',
        monto=300,
    )
    assert type(tr.to_dict()) is dict
    tr.descargar()
