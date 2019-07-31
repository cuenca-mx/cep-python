import requests

USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
)


class Client:
    base_url = 'http://www.banxico.org.mx/cep'

    def __init__(self):
        self.session = requests.Session()
        self.session.headers['User-Agent'] = USER_AGENT
        self.base_data = dict(
            tipoCriterio='T',
            receptorParticipante=0,
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
        url = self.base_url + endpoint
        response = self.session.request(method, url, data=data, **kwargs)
        if not response.ok:
            response.raise_for_status()
        return response.content
