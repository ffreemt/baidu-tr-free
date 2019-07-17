r'''
baidu translate using token/gtk from https://fanyi.baidu.com

TOKEN 和 BAIDUID 从chrome devtools 里拿（Network， 定位 v2transapi，从 headers 拷出 TOKEN 和 BAIDUID）， 实测可行……

或用 selenium （chromedriver）拿TOKEN 和 BAIDUID

但用python requests程序里拿到的token和baiduid则无效，不知道什么原因
'''
# pylint: disable=line-too-long
# , unused-import

from sys import maxsize
import logging
from time import sleep
from random import random, randint
from pathlib import Path

import requests_cache
import js2py
from jsonpath_rw import parse

TOKEN = '564da85ec9a69e4f469df84fee8027a7'
BAIDUID = '2462075953DF51DB4F847392B678BBCA:FG=1'

# works
TOKEN = '13508e550366f3004701d561721e12bd'
BAIDUID = 'AFB6E3FB47D3EEA8C525D02E728E0991:FG=1'

# works
TOKEN = '6482f137ca44f07742b2677f5ffd39e1'
BAIDUID = '19288887A223954909730262637D1DEB:FG=1'

# copy from devtools
TOKEN = 'e9ff6a550307ca17c1bc461c07edeaaf'
BAIDUID = '4EAE417BC9660D50D9A867BC9D7BC0F1:FG=1'

# does not work
# TOKEN = '9b8bb341109338ba7e875bd9a9dd88ba'
# from browser_cookie3
# BAIDUID = '4EAE417BC9660D50D9A867BC9D7BC0F1:FG=1'

BAIDUID = '2462075953DF51DB4F847392B678BBCA:FG=1'
TOKEN = '564da85ec9a69e4f469df84fee8027a7'


BAIDUID = '731394280F578EDE85317AD6C0E13474:FG=1'
TOKEN = '0c323e96c5788185c6433a66daaae1ec'

TOKEN, BAIDUID = ('9b8bb341109338ba7e875bd9a9dd88ba', '85885D7321AF93211B8F0214B9B1F91E:FG=1')

# TOKEN, BAIDUID = ('b88bd1203769d778996525664a93af85', 'E56024F05E3017023A50047936591306:FG=1')
# TOKEN, BAIDUID = ('e66e5676d52ce2caa402c996ebd4bcb6', 'A6347D4D2C9E32E287A9D456B36B714C:FG=1')
TOKEN, BAIDUID = ('dd7f161198b5c8da969d4175f025d3fa', '7568DBBE0B2C2AFAA4E35DB432B424B0:FG=1')  # OK

TOKEN, BAIDUID = ('df9b627b81f5d6c41f10be655bdf3887', '85885D7321AF93211B8F0214B9B1F91E:FG=1')  # OK

# ###########################
GTK = '320305.131321201'

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'  # NOQA

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())
CACHE_NAME = (Path().home() / (Path(vars().get('__file__') or 'test')).stem).as_posix()  # NOQA
EXPIRE_AFTER = 3600

# requests_cache.configure(cache_name=CACHE_NAME, expire_after=36000)  # 10 hours
# requests_cache.install_cache()


JS = \
    '''function a(r, o) {
    for (var t = 0; t < o.length - 2; t += 3) {
        var a = o.charAt(t + 2);
        a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a), a = "+" === o.charAt(t + 1) ? r >>> a : r << a, r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
    }
    return r
}
var C = null;
var hash = function (r, _gtk) {
    var o = r.length;
    o > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(o / 2) - 5, 10) + r.substr(-10, 10));
    var t = void 0,
        t = null !== C ? C : (C = _gtk || "") || "";
    for (var e = t.split("."), h = Number(e[0]) || 0, i = Number(e[1]) || 0, d = [], f = 0, g = 0; g < r.length; g++) {
        var m = r.charCodeAt(g);
        128 > m ? d[f++] = m : (2048 > m ? d[f++] = m >> 6 | 192 : (55296 === (64512 & m) && g + 1 < r.length && 56320 === (64512 & r.charCodeAt(g + 1)) ? (m = 65536 + ((1023 & m) << 10) + (1023 & r.charCodeAt(++g)), d[f++] = m >> 18 | 240, d[f++] = m >> 12 & 63 | 128) : d[f++] = m >> 12 | 224, d[f++] = m >> 6 & 63 | 128), d[f++] = 63 & m | 128)
    }
    for (var S = h, u = "+-a^+6", l = "+-3^+b+-f", s = 0; s < d.length; s++) S += d[s], S = a(S, u);
    return S = a(S, l), S ^= i, 0 > S && (S = (2147483647 & S) + 2147483648), S %= 1e6, S.toString() + "." + (S ^ h)
}'''

HEADERS = {
    'Cookie': f'BAIDUID={BAIDUID}',
    'Host': 'fanyi.baidu.com',
    'Origin': 'https://fanyi.baidu.com',
    'Referer': 'https://fanyi.baidu.com/',
    'User-Agent': UA,
    'X-Requested-With': 'XMLHttpRequest'
}

# GTK = '320305.131321201'
# sign = execjs.compile(JS).call('hash', source, gtk)

# JSC = execjs.compile(JS).call

URL = "https://fanyi.baidu.com/translate"
# SESS = requests.Session()
SESS = requests_cache.CachedSession(
    cache_name=CACHE_NAME,
    expire_after=EXPIRE_AFTER,
    allowable_methods=('GET', 'POST'),
)
SESS.get(URL, headers=HEADERS)

# for js_sign below
exec(js2py.translate_js(JS))  # pylint: disable=exec-used


def js_sign(text, gtk='320305.131321201'):
    '''gtk, does not play  role

    >>> assert js_sign('test') == '431039.159886'
    '''
    return PyJs_anonymous_1_(text, gtk).to_py()  # pylint: disable=undefined-variable


def jp_match(path, obj):
    '''emulate jsonpath_rw_ext\'s jp.match'''
    return [elm.value for elm in parse(path).find(obj)]


def make_throttle_hook(timeout=1.0):
    """
    Returns a response hook function which sleeps for `timeout` seconds if
    response is not cached

    time.sleep(min(0, timeout - 0.5) + random())
        average delay: timeout

    s = requests_cache.CachedSession()
    s.hooks = {'response': make_throttle_hook(0.1)}
    s.get('http://httpbin.org/delay/get')
    s.get('http://httpbin.org/delay/get')
    """
    def hook(response, *args, **kwargs): # pylint: disable=unused-argument
        if not getattr(response, 'from_cache', False):
            timeout0 = min(0, timeout - 0.5) + random()
            LOGGER.debug('%s', f'sleeping {timeout0} s')
            sleep(timeout0)
        return response
    return hook


# av .6 s  for noncached requests
SESS.hooks = {'response': make_throttle_hook(0.6)}


def swap(token, bdid, func='bdtr'):
    '''
    swap token, id

    token, id pairs maybe saved to token-id.json
    in the format of {tokenid":[["tk1", "id1"], ["tk2", "id2"]]}
    token_id = ujson.load(Path('token-id.json').open())['token-id']

    to test:
    for idx, pair in enumerate(token_id):
        swap(*pair)
        res = bdtr('test ' + str(randint(0, maxsize)))
        if not res:
            print(idx, pair, 'likely invalid')
        else:
            print(idx, 'valid')
    '''
    bdtr_ = globals()[func]
    try:
        bdtr_.token, bdtr_.id = token, bdid
        bdtr_.headers['Cookie'] = f'BAIDUID={bdtr_.id}'
        bdtr_.sess.get(URL, headers=bdtr_.headers)
    except Exception as _:
        # print(_)
        # raise Exception('bdtr must be called at least once before using swap()')

        # call bdtr once to activate bdtr's props
        bdtr('test')
        bdtr_.token, bdtr_.id = token, bdid
        bdtr_.headers['Cookie'] = f'BAIDUID={bdtr_.id}'
        bdtr_.sess.get(URL, headers=bdtr_.headers)


def bdtr(text, from_lang='auto', to_lang='zh', cache=True): # pylint: disable=too-many-branches, too-many-statements
    ''' baidu translate based on html token and gtk

    from_lang='auto'; to_lang='zh'; cache=False
    '''

    # use TOKEN, BAIDUID if not defined (first time)
    try:
        bdtr.token
    except Exception as exc:
        _ = exc
        bdtr.token = TOKEN
    try:
        bdtr.id
    except Exception as exc:
        _ = exc
        bdtr.id = BAIDUID

    try:
        bdtr.headers
    except Exception as exc:
        _ = exc
        bdtr.headers = HEADERS

    try:
        bdtr.sess
    except Exception as exc:
        _ = exc
        bdtr.sess = SESS

    try:
        text = str(text).strip()
    except Exception as exc:
        text = ''
    if not text:
        return ''

    url = 'https://fanyi.baidu.com/v2transapi'

    from_lang = from_lang.lower()
    to_lang = to_lang.lower()

    if from_lang in ['zh-cn', 'chinese']:
        from_lang = 'zh'
    if to_lang in ['zh-cn', 'chinese']:
        to_lang = 'zh'

    if from_lang in ['english']:
        from_lang = 'en'
    if to_lang in ['english']:
        to_lang = 'en'

    data = {
        'from': from_lang,
        'to': to_lang,
        'query': text,
        'transtype': 'translang',
        'simple_means_flag': '3',
        'sign': js_sign(text, GTK),
        'token': bdtr.token,
    }

    def fetch():
        '''fetch for two cache cases'''
        try:
            resp = bdtr.sess.post(url, data=data, headers=bdtr.headers)  # OK
            resp.raise_for_status()
            bdtr.text = resp.text
        except Exception as exc:
            LOGGER.error('%s', exc)
            bdtr.text = str(exc)
            resp = bdtr.text
        return resp

    if cache:
        resp = fetch()
    else:
        with requests_cache.disabled():
            resp = fetch()

    try:
        jdata = resp.json()
    except Exception as exc:
        LOGGER.error('resp.json exc: %s', exc)
        jdata = {"error": str(exc)}

    bdtr.json = jdata

    resu = jp_match('$..dst', jdata)

    if resu:
        return resu[0]
    return ''


def test1():
    ''' test1 '''
    text = '为乐为魂之语与通〜'
    from_lang = 'wyw'
    to_lang = 'en'
    assert bdtr(text, from_lang, to_lang) == 'Language and Communication for Music Is the Soul'  # NOQA

def pressure_test():
    '''pressure_test'''
    from time import perf_counter
    from tqdm import trange
    for _ in trange(100):
        tick = perf_counter()
        res = bdtr('test ' + str(randint(1, maxsize)))
        print(res, f'time: {(perf_counter() - tick):.2f} s')
        assert res, 'probably need to increase the value in SESS.hooks = {\'response\': make_throttle_hook(0.6)}'


def main():
    """main"""

    text = 'When it comes to digital marketing and the ad tech industry, the bright promise of a decentralised future has led to a spate of blockchain initiatives.'  # NOQA
    from_lang = 'en'
    to_lang = 'zh'
    # resu = bdtr(text, from_lang, to_lang, cache=False)

    text = 'test ' + str(randint(0, maxsize))
    resu = bdtr(text, from_lang, to_lang)

    print(f'{text} trans: [{resu}]')
    # print(bdtr.json)


if __name__ == "__main__":
    main()
