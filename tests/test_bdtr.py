''' vrious tests '''
from sys import maxsize
from random import randint

from bdtr import bdtr


def test_def():
    ''' test1 '''
    text = '为乐为魂之语与通〜'
    from_lang = 'wyw'
    to_lang = 'en'
    assert bdtr(text, from_lang, to_lang) == 'For music is the language and communication of soul ~'  # NOQA


def test_pressure():
    '''pressure_test'''
    from time import perf_counter
    from tqdm import trange
    for _ in trange(10):
        tick = perf_counter()
        res = bdtr('test ' + str(randint(1, maxsize)))
        print(res, f'time: {(perf_counter() - tick):.2f} s')
        assert res, 'probably need to increase the value in SESS.hooks = {\'response\': make_throttle_hook(0.6)}'


def test_long_test():
    ''' test text longer than 30 '''
    text = 'A second Canadian plane carrying 185 passengers from Wuhan arrived in Vancouver just before 1 a.m. Eastern Time, according to CTV. '

    res = bdtr(text)
    assert len(res) > 10
    assert res, 'To see res'

