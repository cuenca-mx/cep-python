import datetime

import pytest

from cep import Cuenta, Transferencia


@pytest.fixture
def transferencia():
    yield Transferencia(
        fecha_operacion=datetime.datetime(2019, 4, 12, 13, 31, 44),
        ordenante=Cuenta(
            nombre='Matin Tamizi',
            tipo='40',
            banco='STP',
            numero='646180157042875763',
            rfc='ND',
        ),
        beneficiario=Cuenta(
            nombre='MATIN TAMIZI',
            tipo='40',
            banco='BBVA BANCOMER',
            numero='012180004643051249',
            rfc='TAMA840916669',
        ),
        monto=8.17,
        clave_rastreo='CUENCA1555093850',
        concepto='Matin',
        emisor='90646',
        receptor='40012',
        sello=(
            'X8YFvAfKZhV72datpHzKes/AaOyLqgs0uDWlVqrDy8i0FV96ajZY17Hz9X35c7'
            'z/TrSSvw6BQiqVWbJGG5xriNn8PK4pFKF6nyCEr6uGQ6FuF7YqAD6tUK55BBKT'
            'dqF3j+qummKguTHJyttR4xMwmOpiuwkgXuUFaEEHiO+UjgIk7BVzkULkZdpciL'
            'rY4czMZhdqpQ7if0udu2BxWI99eU9ZqaAtILyt39MtCPObu61D4A6SFnw6JwsU'
            'Rm2wCZ4KSYzex18Re3Hrg+BLri5drlgcPSG5/OBeE2omlcuZTQqd5iUzRt/XVg'
            '33arK4M8h2hbcfU/xwtYEDBQ6Jewh+tg=='
        ),
    )
