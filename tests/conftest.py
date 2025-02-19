import datetime

import pytest

import cep
from cep import Client, Cuenta, Transferencia

# Use beta endpoint for testing
cep.configure(beta=True)


@pytest.fixture
def client():
    yield Client()


@pytest.fixture
def transferencia_tipo_1():
    yield Transferencia(
        fecha_operacion=datetime.date(2024, 11, 8),
        fecha_abono=datetime.datetime(2024, 11, 8, 10, 53, 36),
        ordenante=Cuenta(
            nombre='Pruebas Bienestar',
            tipo_cuenta='40',
            banco='BaBien',
            numero='166180026480316602',
            rfc='GAJH931011I41',
        ),
        beneficiario=Cuenta(
            nombre='Felipe Lopez Hernandez',
            tipo_cuenta='40',
            banco='Cuenca',
            numero='723969000011000077',
            rfc='LOHF890619HCSPRL05',
        ),
        monto=341495,  # In cents
        iva=0.00,
        concepto='CONCEPTO PAGO TIPO 1',
        clave_rastreo='BiB202411081016248360',
        emisor='37166',
        receptor='90723',
        sello=(
            'WtvkPvCMGKSaj+B/XPUnVnahJXwCfASJ1u3cUsU0+MYSaXV2K0a'
            'EC5otVJntu80bbsmdaVqI1P+V7BbXr3WJDKPtFJnVTXmuRalInP'
            'UZ6e0rs5GOO45ZktZ0CYnxoLqt1kgX5oIlRchh/xXVfHAPy964K'
            'sARiCTr8/BeaiBeImjhcXh6CKwmO23cGiydQ3OxGPagnijfZE/F'
            'PWPJ2z5NBOIH9Qo4wg/UuDZEVl5ekmUZlarFZ+sT8F+RkrRYr6I'
            'P0x+5Y7y53qMGqoBy0x6L3wI9rwhue4Nrcmk40pQGjsQR+FBKtS'
            'etSaWZhz/32cbulWzEk9wug8LfUij+KNtU3Q=='
        ),
        tipo_pago=1,
        pago_a_banco=False,
    )
