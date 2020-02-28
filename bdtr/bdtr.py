r'''
browser-cookie3>=0.10.1: fetc BAIDUID from local browser cookies

2020 02 10: only works if len(text) < 31?

baidu translate using token/gtk from https://fanyi.baidu.com

TOKEN 和 BAIDUID 从chrome devtools 里拿（Network， 定位 v2transapi，从 headers 拷出 TOKEN 和 BAIDUID）， 实测可行……

或用 selenium （chromedriver）拿TOKEN 和 BAIDUID

'''
# pylint: disable=line-too-long
# , unused-import

import os
from sys import maxsize
import logging
from time import sleep
from random import random, randint
from pathlib import Path

import requests_cache

import js2py
# from jsonpath_rw import parse
import jmespath

# from loguru import logger
# from logzero import logger

# import pkg_resources
# if pkg_resources.get_distribution("browser-cookie3").version.split('.') < ['0', '10', '1']:

from .py_sign import py_sign
from .js2py_sign import js2py_sign
from .get_baiduid_token import get_baiduid_token

# devtools, copy curl(bash)-> requets https://curl.trillworks.com/  OK 2019.11.12
# pypi-ready\baidu_tr\bdtr\curl2req20191112.py
# BAIDUID = '4EAE417BC9660D50D9A867BC9D7BC0F1:FG=1'
# TOKEN = 'e9ff6a550307ca17c1bc461c07edeaaf'

# BAIDUID = '573D03E3F52E7A9006471EEE9059A242:FG=1'
# TOKEN = 'ce903b4ae5b301e9fbe10e5b8e902191'

# 'BF565E9628E0A53ED07B135111920C1B:FG=1'
# '37a9c9518da5c7feeb4b21d26e957a0a'

BAIDUID, TOKEN = get_baiduid_token()
# 'BF565E9628E0A53ED07B135111920C1B:FG=1'
# '9b8bb341109338ba7e875bd9a9dd88ba'  # x

# get_bd_token_baiduid()  # chromedriver based, valid
token0, baiduid0 = ('d4ff30487b004d0a7197216bd18c6a84', '5929C2F4F3D0DB4F822C3167E1AE8C0B:FG=1')

# logger.info('BAIDUID: %s TOKEN: %s', BAIDUID, TOKEN)

# BDTR_DEBUG off
# set/export BDTR_DEBUG=1 to skip check
if not os.getenv('BDTR_DEBUG'):
    assert TOKEN, '本程序需要百度的cookies，用 Chrome 浏览器登录百度后再试。'

    assert len(TOKEN) == 32, f'令牌长度[{len(TOKEN)}] 不等于32，令牌可能无效。去 https://github.com/ffreemt/baidu-tr-free/issues 反馈一下。'
else:
    if TOKEN is None:
        TOKEN = ''

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


def make_throttle_hook(timeout=0.67, exempt=1000):
    """
    Returns a response hook function which sleeps for `timeout` seconds if
    response is not cached

    the first exempt calls exempted from throttling
    """

    try:
        timeout = float(timeout)
    except Exception:
        timeout = .67

    try:
        exempt = int(exempt)
    except Exception:
        exempt = 100

    def hook(response, *args, **kwargs):  # pylint: disable=unused-argument
        if not getattr(response, 'from_cache', False):
            timeout_ = timeout + random() - 0.5
            timeout_ = max(0, timeout_)

            try:
                hook.flag
            except AttributeError:
                hook.flag = -1
            finally:
                hook.flag += 1
                quo, _ = divmod(hook.flag, exempt)
            # quo is 0 only for the first exempt calls

            LOGGER.debug('avg delay: %s, sleeping %s s, flag: %s', timeout, timeout_, bool(quo))

            # will not sleep (timeout_ * bool(quo)=0) for the first exempt calls
            sleep(timeout_ * bool(quo))

        return response
    return hook


URL = "https://fanyi.baidu.com/translate"
# SESS = requests.Session()
SESS = requests_cache.CachedSession(
    cache_name=CACHE_NAME,
    expire_after=EXPIRE_AFTER,
    allowable_methods=('GET', 'POST'),
)
SESS.hooks = {'response': make_throttle_hook(1, 200)}  # to play safe, default: 0.67, 1000
SESS.get(URL, headers=HEADERS)

# for js_sign below
exec(js2py.translate_js(JS))  # pylint: disable=exec-used


def _js_sign(text, gtk='320305.131321201'):
    '''gtk, does not play  role

    >>> assert _js_sign('test') == '431039.159886'
    '''
    return PyJs_anonymous_1_(text, gtk).to_py()  # pylint: disable=undefined-variable  # noqa: F821


_ = """
def jp_match(path, obj):
    '''emulate jsonpath_rw_ext\'s jp.match'''
    return [elm.value for elm in parse(path).find(obj)]
# """


def swap(token, bdid, func='bdtr'):  # pragma: no cover
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
    # except Exception as _:
    except Exception:
        # print(_)
        # raise Exception('bdtr must be called at least once before using swap()')

        # call bdtr once to activate bdtr's props
        bdtr('test')
        bdtr_.token, bdtr_.id = token, bdid
        bdtr_.headers['Cookie'] = f'BAIDUID={bdtr_.id}'
        bdtr_.sess.get(URL, headers=bdtr_.headers)


def bdtr(text, from_lang='auto', to_lang='zh', cache=True):  # pylint: disable=too-many-branches, too-many-statements  # noqa: C901
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
        LOGGER.error('%s', exc)
        text = ''
    if not text:  # pragma: no cover
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

    # 'auto' no longer works
    # temp fix
    # TODO: better logic to fix auto based on to_lang
    if from_lang in ['auto']:
        from_lang = 'en'

    if len(text) < 31:
        sign = py_sign(text, GTK)
    else:
        sign = js2py_sign(text)

    data = {
        'from': from_lang,
        'to': to_lang,
        'query': text,
        'transtype': 'translang',
        'simple_means_flag': '3',
        'sign': sign,
        # 'sign': js_sign(text, GTK),
        # 'token': bdtr.token,
        'token': TOKEN,
        # 'token': token,
    }

    def fetch():
        '''fetch for two cache cases'''
        try:
            # resp = bdtr.sess.post(url, data=data, headers=bdtr.headers)  # OK
            resp = SESS.post(url, data=data, headers=HEADERS)  # OK
            resp.raise_for_status()
            bdtr.text = resp.text
        except Exception as exc:
            LOGGER.error('%s', exc)
            bdtr.text = {'errors': str(exc)}
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

    # resu = jp_match('$..dst', jdata)
    # 'trans_result.data[0].dst'
    # if resu: return resu[0]
    # return ''

    resu = jmespath.search('trans_result.data[0].dst', jdata)

    if resu:
        return resu
    return ''


def main():  # pragma: no cover
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
