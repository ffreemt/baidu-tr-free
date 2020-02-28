'''
fetch and verify BAIDUID

fetch token from fanyi.baidu.com
'''

from typing import Tuple, Optional

import sys
import re
import httpx  # cant seem to get the correct token
import requests
import browser_cookie3
from pyquery import PyQuery as pq

from loguru import logger
import socket
socket.setdefaulttimeout(90)


def get_baiduid_token() -> Tuple[Optional[str], Optional[str]]:
    '''Optional
    fetch and verify BAIDUID

    fetch token from fanyi.baidu.com
    '''

    if sys.platform not in ['win32']:
        logger.warning('Only tested in Windows, Linux/OSx may not work')
        # for github flow only
        # to pass the export BDTR_DEBUG=1 && 'pytest -k empty' test
        # return '', None

    logged_in = []
    try:
        cj = browser_cookie3.chrome(domain_name='baidu.com')
    except Exception as exc:
        logger.error('unable to get cookies: %s, exiting...' % exc)
        return '', None

    cj_dict = dict([(elm.name, elm.value) for elm in cj if elm.name in ['BAIDUID', 'BDUSS']])

    baiduid = cj_dict.get('BAIDUID')
    # sess = httpx.Client()
    sess = requests.Session()
    # sess.get('http://www.baidu.com', cookies=cj)

    try:
        content = sess.get('http://www.baidu.com', cookies=cj_dict).content
        # content = httpx.get('http://www.baidu.com',  cookies=cj).content
        # content = requests.get('http://www.baidu.com', cookies=cj).content
    except Exception as exc:
        logger.error(exc)
        content = str(exc).encode()

    logged_in = pq(content)('.user-name')

    if not logged_in:
        logger.warning('未有登录百度，无法继续')
        return baiduid, None

    # fetch token from fanyi.baidu.com
    try:
        # httpx cant seem to get the correct token
        # text = httpx.get('http://fanyi.baidu.com', cookies=cj).text
        # text = requests.get('http://fanyi.baidu.com', cookies=cj).text
        _ = 'https://fanyi.baidu.com'
        text = sess.get(_, cookies=cj_dict).text
        # text = sess.get(_, cookies=cj_dict).text
    except Exception as exc:
        logger.error(exc)
        text = str(exc)
    _ = re.findall(r"(?<=token:\s')\w+", text)
    token = ''
    if _:
        token, = _

    sess.close()

    return baiduid, token


def main():
    ''' main '''
    print(get_baiduid_token())


if __name__ == '__main__':
    main()
