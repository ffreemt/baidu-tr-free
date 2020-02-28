''' various tests '''
# from sys import maxsize
from random import randint
import pytest

from bdtr import bdtr


def test_to_chinese():
    ''' test test_to_chinese random '''
    rint = str(randint(1, 10000))
    assert rint in bdtr('test ' + rint, to_lang='chinese')


def test_from_chinese():
    ''' test test_from_chinese random '''
    rint = str(randint(1, 10000))
    assert rint in bdtr('测试 ' + rint, 'chinese', 'en')


def test_to_english():
    ''' test test_to_english random '''
    rint = str(randint(1, 10000))
    assert rint in bdtr('测试 ' + rint, 'zh', 'english')


def test_from_english_cache_disabled():
    ''' test test_from_english random '''
    rint = str(randint(1, 10000))
    assert rint in bdtr('test ' + rint, 'english', 'zh', cache=0)


def test_to_zhcn():
    ''' test test_to_zhcn random '''
    rint = str(randint(1, 10000))
    assert rint in bdtr('test ' + rint, to_lang='zh-cn')


def test_from_zhcn():
    ''' test test_from_zhcn random '''
    rint = str(randint(1, 10000))
    assert rint in bdtr('测试 ' + rint, 'zh-cn', 'en')
