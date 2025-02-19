from typing import ClassVar

import requests

USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
)

BASE_URL = 'https://www.banxico.org.mx/cep'
BASE_URL_BETA = 'https://www.banxico.org.mx/cep-beta'


def configure(beta=False):
    Client.base_url = BASE_URL_BETA if beta else BASE_URL


class Client:
    base_url: ClassVar[str] = BASE_URL

    def __init__(self):
        self.session = requests.Session()
        self.session.headers['User-Agent'] = USER_AGENT
        self.base_data = dict(
            tipoCriterio='T',
            captcha='c',
            tipoConsulta=1,
        )

    def get(self, endpoint: str, **kwargs) -> bytes:
        return self.request('get', endpoint, {}, **kwargs)

    def post(self, endpoint: str, data: dict, **kwargs) -> bytes:
        data = {**self.base_data, **data}
        return self.request('post', endpoint, data, **kwargs)

    def request(
        self, method: str, endpoint: str, data: dict, **kwargs
    ) -> bytes:
        url = Client.base_url + endpoint
        response = self.session.request(method, url, data=data, **kwargs)
        if not response.ok:
            response.raise_for_status()
        return response.content
