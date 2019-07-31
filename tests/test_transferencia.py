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


@pytest.mark.vcr
def test_descarga_pdf(transferencia):
    pdf = transferencia.descargar()
    file_dir = os.path.dirname(__file__)
    file_path = os.path.join(file_dir, 'CEP-20190412-CUENCA1555093850.pdf')
    with open(file_path, 'rb') as f:
        assert pdf == f.read()
