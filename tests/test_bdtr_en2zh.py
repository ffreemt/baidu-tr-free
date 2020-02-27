''' vrious tests '''
# from sys import maxsize
from random import randint
import pytest

from bdtr import bdtr


def test_en2zh_def_random():
    ''' test en2zh random '''
    rint = str(randint(1, 10000))
    assert rint in bdtr('test ' + rint)


def test_def_long_random():
    ''' test text longer than 30 '''
    rint = str(randint(1, 10000))
    text = 'A second Canadian plane carrying 185 passengers from Wuhan arrived in Vancouver just before 1 a.m. Eastern Time, according to CTV. '

    res = bdtr(text + rint)

    assert rint in res


def test_en2de_long_random():
    ''' test text longer than 30 '''
    rint = str(randint(1, 10000))
    text = 'A second Canadian plane carrying 185 passengers from Wuhan arrived in Vancouver just before 1 a.m. Eastern Time, according to CTV. '

    res = bdtr(text + rint, 'en', 'de')

    assert rint in res


def test_en2de_random():
    ''' test en2de random '''
    rint = str(randint(1, 10000))
    assert rint in bdtr('test ' + rint, to_lang='de')


# @pytest.mark.skip("'fr' does not seem to work")
@pytest.mark.xfail(raises=AssertionError)
def test_en2fr_random():
    ''' test en2fr random '''
    rint = str(randint(1, 10000))
    assert rint in bdtr('test ' + rint, to_lang='fr')
    # 'fr' does not seem to work

    # assert 1
