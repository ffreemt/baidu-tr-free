'''
fetch and verify BAIDUID

fetch token from fanyi.baidu.com
'''

from typing import Tuple, Optional

import sys
import re
import httpx
import browser_cookie3
from pyquery import PyQuery as pq

from loguru import logger


def get_baiduid_token() -> Tuple[Optional[str], Optional[str]]:
    '''Optional
    fetch and verify BAIDUID

    fetch token from fanyi.baidu.com
    '''

    if sys.platform not in ['win32']:
        logger.warning('Only wroks in Windows, sorry')
        # for github flow only
        # to pass the export BDTR_DEBUG=1 && 'pytest -k empty' test
        return '', None

    logged_in = []
    cj = browser_cookie3.chrome(domain_name='baidu.com')

    baiduid = dict([(cookie.name, cookie.value) for cookie in cj]).get('BAIDUID')

    try:
        content = httpx.get('http://www.baidu.com', cookies=cj).content
    except Exception as exc:
        logger.error(exc)
        content = str(exc).encode()

    logged_in = pq(content)('.user-name')

    if not logged_in:
        logger.warning('未有登录百度，无法继续')
        return baiduid, None

    # fetch token from fanyi.baidu.com
    try:
        text = httpx.get('http://fanyi.baidu.com', cookies=cj).text
    except Exception as exc:
        logger.error(exc)
        text = str(exc)
    _ = re.findall(r"(?<=token:\s')\w+", text)
    token = ''
    if _:
        token, = _

    return baiduid, token
