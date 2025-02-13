# CEP

[![test](https://github.com/cuenca-mx/cep-python/workflows/test/badge.svg)](https://github.com/cuenca-mx/cep-python/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/cuenca-mx/cep-python/branch/master/graph/badge.svg)](https://codecov.io/gh/cuenca-mx/cep-python)
[![PyPI](https://img.shields.io/pypi/v/cepmex.svg)](https://pypi.org/project/cepmex/)

Python client library for CEP (http://www.banxico.org.mx/cep/)


## Instalación

```bash
pip install cepmex
```

## Development & Testing

You can use a staging environment to test the library:

```python
from cep import Config

Config.BASE_URL = 'http://www.banxico.org.mx/cep-beta'
```

To run unit tests, use `pytest`.
```bash
pytest
```

### Usage

```python
from datetime import date
from cep import Transferencia
from cep.exc import NotFoundError

try:
    tr = Transferencia.validar(
        fecha=date(2019, 4, 12),
        clave_rastreo='CUENCA1555093850',
        emisor='90646',  # STP
        receptor='40012',  # BBVA
        cuenta='012180004643051249',
        monto=8.17,
    )
    pdf = tr.descargar()
    with open('CUENCA1555093850.pdf', 'wb') as f:
        f.write(pdf)
except NotFoundError as e:
    print('No se encontro la transferencia')
```

## Validate Transfer Parameters

Use the `validar` method to validate a transfer with the following parameters:

### Required Parameters:
- `fecha` (`datetime.date`): Transfer date.
- `clave_rastreo` (`str`): Transfer tracking key.
- `emisor` (`str`): Transfer sender bank code.
- `receptor` (`str`): Transfer receiver bank code.
- `cuenta` (`str`): Transfer account number.
- `monto` (`Decimal`): Transfer amount.

### Optional Parameters:
- `pago_a_banco` (`bool`, default=`False`): Set to `True` for transfer types 4 and 31.

## Download Transfer Data

Use the `descargar` method to download a transfer in one of the following formats:
- `PDF` (default)
- `XML`
- `ZIP`

```python
tr.descargar(formato='XML')
```
