# CEP

[![Build Status](https://travis-ci.com/cuenca-mx/cep-python.svg?branch=master)](https://travis-ci.com/cuenca-mx/cep-python)
[![Coverage Status](https://coveralls.io/repos/github/cuenca-mx/cep-python/badge.svg?branch=master)](https://coveralls.io/github/cuenca-mx/cep-python?branch=master)
[![PyPI](https://img.shields.io/pypi/v/cepmex.svg)](https://pypi.org/project/cepmex/)

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
