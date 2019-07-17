"""
based on youdao_tr_list, no threading, no queue
youdaoweb translates a list of text (str).

testq2.py
"""
from pathlib import Path
import logging
from time import sleep
from random import random
from tqdm import tqdm

from load_file_as_text import load_file_as_text
from text_to_paras import text_to_paras
from bdtr import bdtr

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def bdtr_list(seq, from_lang='en', to_lang='zh'):
    """Translate (bdtr) a list of text.

    :in: list of text
    :out: list of translated text
    """
    # record the # of func calls

    if not isinstance(seq, list):
        LOGGER.error("Input not a list, return the original")
        return seq

    try:
        bdtr_list.counter += 1
    except Exception as exc:
        bdtr_list.counter = 1
        del exc

    len0 = len(seq)

    # introduce delay 0.5 + .5 after 300 calls
    seqout = []
    for elm in tqdm(seq, desc='converting...', unit='pars'):
        seqout += [bdtr(elm, from_lang=from_lang, to_lang=to_lang)]
        if bdtr_list.counter > 300:
            sleep(0.25 + random())
        bdtr_list.counter += 1
    return seqout


def test_():
    """test_+++."""
    filepath = r'D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\test_files\files_for_testing_load\Folding_Beijing_ch1-en.txt'  # noqa

    text = load_file_as_text(filepath)
    # seqen = text_to_paras(text)

    filepath = r'C:\dl\Dropbox\mat-dir\pyqt\Sandbox\test_files\files_for_testing_load\Folding_Beijing_ch1-zh.txt'  # noqa
    assert Path(filepath).exists(), f'[{filepath}] does not exist.'

    text = load_file_as_text(filepath)
    seq = text_to_paras(text)

    out = bdtr_list(seq, 'zh', 'en')

    exp = ["A city in the morning light， folding， the ground collapsed.Tall buildings like the most humble servant， bent over， let oneself inferior to cut off the body， head to touch his feet， tightly together， then fracture bent over again， will head the arm bend distortion， inserted into the gap.Buildings after bending， curled up into a dense huge rubik's cube， thick is to aggregate together， into a deep sleep.Then turn on the ground， small small plots of land around its axis， turn one hundred and eighty degrees to the other side， to the other side of the building.In the building by the folding stand up， like waking up in the grey blue sky beast.City island in the orange light is conditioned， and stood， leaps of pale grey cloud.", 'Drivers in the sleepy and hungry appreciate the city theatre this scene infinite loop.']  # noqa

    # print(out[-2:])
    eq_(exp, out[-2:])
