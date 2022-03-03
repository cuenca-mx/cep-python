import pytest
from requests.exceptions import HTTPError


@pytest.mark.vcr
def test_http_error(client):
    with pytest.raises(HTTPError):
        client.get('/no/existe')
