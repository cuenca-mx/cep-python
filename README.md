# CEP

[![test](https://github.com/cuenca-mx/cep-python/workflows/test/badge.svg)](https://github.com/cuenca-mx/cep-python/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/cuenca-mx/cep-python/branch/master/graph/badge.svg)](https://codecov.io/gh/cuenca-mx/cep-python)
[![PyPI](https://img.shields.io/pypi/v/cuenca.svg)](https://pypi.org/project/cuenca/)

Python client library for CEP (http://www.banxico.org.mx/cep/)


## Instalación

```bash
pip install cepmex
```

### Uso

```python
from datetime import date

from cep import Transferencia

tr = Transferencia.validar(
    fecha=date(2019, 4, 12),
    clave_rastreo='CUENCA1555093850',
    emisor='90646',  # STP
    receptor='40012',  # BBVA
    cuenta='012180004643051249',
    monto=8.17,
)
pdf = tr.descargar()
```
