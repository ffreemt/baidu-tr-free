'''fetch baidu fanyi token baiduid
by chromedriver

Used to generate data in token-id.json

currently not used by bdtr -- for future use
'''
import logging
import re

from get_chrome_driver import CHROME_DRIVER

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def get_bd_token_baiduid():
    '''fetch baidu fanyi token baiduid from web via chromedriver'''

    url = "https://fanyi.baidu.com/translate"
    CHROME_DRIVER.get(url)

    _ = re.search(r'token: \'([a-z\d]{32})', CHROME_DRIVER.page_source)
    if _.groups():
        token = _.groups()[0]
    else:
        LOGGER.warning(' token not found: %s', _)
        token = 'token not found'

    baiduid = ''
    _ = [elm.get('value') for elm in CHROME_DRIVER.get_cookies() if elm.get('name') == 'BAIDUID']
    if _:
        baiduid = _[0]
    else:
        LOGGER.warning(' baiduid not found: %s', _)

    # CHROME_DRIVER.quit()

    return token, baiduid


# TOKEN_GTK = get_bd_token_gtk()
try:
    TOKEN, BAIDUID = get_bd_token_baiduid()
except Exception:
    TOKEN = '6482f137ca44f07742b2677f5ffd39e1'
    BAIDUID = '19288887A223954909730262637D1DEB:FG=1'


def main():
    """main"""
    print("TOKEN, BAIDUID: ", TOKEN, BAIDUID)
    print(get_bd_token_baiduid())


if __name__ == "__main__":
    main()
