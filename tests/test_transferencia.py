import datetime as dt
import os

import pytest
from requests.exceptions import HTTPError

from cep import Transferencia
from cep.exc import (
    CepError,
    CepNotAvailableError,
    MaxRequestError,
    TransferNotFoundError,
)


@pytest.mark.vcr
def test_fail_validar_transferencia_pago():
    with pytest.raises(TransferNotFoundError):
        Transferencia.validar(
            fecha=dt.date(2019, 1, 1),
            clave_rastreo='invalid-clave',
            emisor='37166',
            receptor='90723',
            cuenta='012180004643051249',
            monto=111111100,
        )


@pytest.mark.vcr
def test_fail_validar_transferencia_operacion():
    with pytest.raises(TransferNotFoundError):
        Transferencia.validar(
            fecha=dt.date(2024, 11, 8),
            clave_rastreo='BiB202411081016248XXX',
            emisor='37166',
            receptor='90723',
            cuenta='723969000011000077',
            monto=341495,
        )


@pytest.mark.vcr
def test_descarga_pdf(transferencia_tipo_1):
    pdf = transferencia_tipo_1.descargar()
    file_dir = os.path.dirname(__file__)
    file_path = os.path.join(
        file_dir, 'CEP-20241108-BiB202411081016248360.pdf'
    )
    with open(file_path, 'rb') as f:
        assert pdf == f.read()


@pytest.mark.vcr
def test_lanza_cep_error_para_errores_500():
    try:
        for i in range(10):
            Transferencia.validar(
                fecha=dt.date(2024, 11, 8),
                clave_rastreo='BiB2024110810162420780',
                emisor='37166',
                receptor='90723',
                cuenta='723969000011000077',
                monto=2520826,
            )
    except CepError as exc:
        assert type(exc.__cause__) is HTTPError
        assert '500 Server Error: Internal Server Error' in str(exc.__cause__)


@pytest.mark.vcr
def test_maximo_numero_de_requests():
    with pytest.raises(MaxRequestError):
        Transferencia.validar(
            fecha=dt.date(2024, 11, 8),
            clave_rastreo='MIFELSPEI20241108102122835',
            emisor='40042',
            receptor='90723',
            cuenta='723969000011000077',
            monto=2091298,
        )


@pytest.mark.vcr
def test_validar_transferencia_encontrada_sin_cep():
    with pytest.raises(CepNotAvailableError):
        Transferencia.validar(
            fecha=dt.date(2024, 11, 6),
            clave_rastreo='COMPROPAG2024110610833063',
            emisor='90728',
            receptor='90723',
            cuenta='723969000011000077',
            monto=1758428,
        )


@pytest.mark.vcr
def test_validar_transferencia_tipo_1(transferencia_tipo_1):
    tr = Transferencia.validar(
        fecha=dt.date(2024, 11, 8),
        clave_rastreo='BiB202411081016248360',
        emisor='37166',
        receptor='90723',
        cuenta='723969000011000077',
        monto=341495,  # In cents
    )
    assert tr is not None
    assert tr.tipo_pago == 1
    assert tr == transferencia_tipo_1
    assert type(tr.to_dict()) is dict


@pytest.mark.vcr
def test_validar_transferencia_tipo_3():
    tr = Transferencia.validar(
        fecha=dt.date(2024, 11, 8),
        clave_rastreo='BiB2024110810162418193',
        emisor='37166',
        receptor='90723',
        cuenta='566180000553286528',
        monto=1080262,
    )
    assert tr is not None
    assert tr.beneficiario.rfc == 'NA'
    assert tr.tipo_pago == 3


@pytest.mark.vcr
def test_validar_transferencia_tipo_4():
    tr = Transferencia.validar(
        fecha=dt.date(2024, 11, 8),
        clave_rastreo='RASPEIOAT202411081015742432',
        emisor='40021',
        receptor='90723',
        cuenta='021180043534353354',
        monto=1718723,
        pago_a_banco=True,
    )
    assert tr is not None
    assert tr.beneficiario.nombre == 'NA'
    assert tr.beneficiario.rfc == 'NA'
    assert tr.beneficiario.numero == 'NA'
    assert tr.tipo_pago == 4


@pytest.mark.vcr
def test_validar_transferencia_tipo_5():
    tr = Transferencia.validar(
        fecha=dt.date(2024, 11, 8),
        clave_rastreo='RASPEIOAT202411081015794072',
        emisor='40021',
        receptor='90723',
        cuenta='723969000011000077',
        monto=2752989,
    )
    assert tr is not None
    assert tr.ordenante.nombre == 'NA'
    assert tr.ordenante.rfc == 'NA'
    assert tr.ordenante.numero == 'NA'
    assert tr.tipo_pago == 5


@pytest.mark.vcr
def test_validar_transferencia_tipo_6():
    tr = Transferencia.validar(
        fecha=dt.date(2024, 11, 8),
        clave_rastreo='RASPEIOAT202411081015791849',
        emisor='40021',
        receptor='90723',
        cuenta='723969000011000077',
        monto=2753217,
    )
    assert tr is not None
    assert tr.ordenante.nombre == 'NA'
    assert tr.ordenante.rfc == 'NA'
    assert tr.ordenante.numero == 'NA'
    assert tr.beneficiario.rfc == 'NA'
    assert tr.tipo_pago == 6


@pytest.mark.vcr
def test_validar_transferencia_tipo_8():
    tr = Transferencia.validar(
        fecha=dt.date(2024, 11, 8),
        clave_rastreo='MIFELSPEI20241108102121081',
        emisor='40042',
        receptor='90723',
        cuenta='723969000011000077',
        monto=2852396,
    )
    assert tr is not None
    assert tr.tipo_pago == 8


@pytest.mark.vcr
def test_validar_transferencia_tipo_9():
    tr = Transferencia.validar(
        fecha=dt.date(2024, 11, 8),
        clave_rastreo='RASPEIOAT202411081215739794',
        emisor='40021',
        receptor='90723',
        cuenta='723969000011000077',
        monto=2977866,
    )
    assert tr is not None
    assert tr.beneficiario.rfc == 'NA'
    assert tr.tipo_pago == 9


@pytest.mark.vcr
def test_validar_transferencia_tipo_10():
    tr = Transferencia.validar(
        fecha=dt.date(2024, 11, 8),
        clave_rastreo='MIFELSPEI20241108102122835',
        emisor='40042',
        receptor='90723',
        cuenta='723969000011000077',
        monto=2091298,
    )
    assert tr is not None
    assert tr.ordenante.rfc == 'NA'
    assert tr.ordenante.nombre == 'NA'
    assert tr.ordenante.numero == 'NA'
    assert tr.tipo_pago == 10


@pytest.mark.vcr
def test_validar_transferencia_tipo_11():
    tr = Transferencia.validar(
        fecha=dt.date(2024, 11, 8),
        clave_rastreo='MIFELSPEI20241108112123712',
        emisor='40042',
        receptor='90723',
        cuenta='723969000011000077',
        monto=985870,
    )
    assert tr is not None
    assert tr.ordenante.rfc == 'NA'
    assert tr.ordenante.nombre == 'NA'
    assert tr.ordenante.numero == 'NA'
    assert tr.tipo_pago == 11


@pytest.mark.vcr
def test_validar_transferencia_tipo_12():
    tr = Transferencia.validar(
        fecha=dt.date(2024, 11, 7),
        clave_rastreo='EPRU723PRENOM24110744VL0000001',
        emisor='2001',
        receptor='90723',
        cuenta='723969000011000077',
        monto=125,
    )
    assert tr is not None
    assert tr.tipo_pago == 12


@pytest.mark.vcr
def test_validar_transferencia_tipo_30():
    tr = Transferencia.validar(
        fecha=dt.date(2024, 11, 8),
        clave_rastreo='BiB2024110810162420780',
        emisor='37166',
        receptor='90723',
        cuenta='723969000011000077',
        monto=2520826,
    )
    assert tr is not None
    assert tr.tipo_pago == 30


@pytest.mark.vcr
def test_validar_transferencia_tipo_31():
    tr = Transferencia.validar(
        fecha=dt.date(2024, 11, 8),
        clave_rastreo='6022135',
        emisor='40059',
        receptor='90723',
        cuenta='059180019535000152',
        monto=659315,
        pago_a_banco=True,
    )
    assert tr is not None
    assert tr.beneficiario.rfc == 'NA'
    assert tr.beneficiario.nombre == 'NA'
    assert tr.beneficiario.numero == 'NA'
    assert tr.tipo_pago == 31


@pytest.mark.vcr
def test_validar_transferencia_tipo_35():
    tr = Transferencia.validar(
        fecha=dt.date(2024, 11, 8),
        clave_rastreo='2370050',
        emisor='40062',
        receptor='90723',
        cuenta='723969000011000077',
        monto=1388770,
    )
    assert tr is not None
    assert tr.tipo_pago == 35


@pytest.mark.vcr
def test_validar_transferencia_tipo_36():
    tr = Transferencia.validar(
        fecha=dt.date(2024, 11, 8),
        clave_rastreo='BXM492411081919171201',
        emisor='40113',
        receptor='90723',
        cuenta='723969000011000077',
        monto=2168376,
    )
    assert tr is not None
    assert tr.tipo_pago == 36
