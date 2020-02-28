'''
test get_baiduid_token

pytest --log-cli-level=10 -k token_1
'''
import httpx
from bdtr import get_baiduid_token


def test_getbaiduid_token_1():
    ''' test 1'''

    baiduid, token = get_baiduid_token()
    print(baiduid, token)
    assert len(baiduid) if baiduid is not None else 0 == 37
    assert len(token) if token is not None else 0 == 32


def test_getbaiduid_token_monkeypatch(monkeypatch):
    ''' test_getbaiduid_token_monkeypatch '''
    def raise_():
        raise Exception()

    monkeypatch.setattr(httpx, 'get', raise_)

    baiduid, token = get_baiduid_token()
    print(baiduid, token)
    assert len(baiduid) if baiduid is not None else 0 == 37
    assert not token
