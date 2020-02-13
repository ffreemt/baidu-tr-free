"""
based on youdao_tr_list, no threading, no queue
"""

# pragma: no cover

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

    # len0 = len(seq)

    # introduce extra delay 0.5 + .5 after 300 calls
    seqout = []
    for elm in tqdm(seq, desc='converting...', unit='pars'):
        seqout += [bdtr(elm, from_lang=from_lang, to_lang=to_lang)]
        if bdtr_list.counter > 300:
            sleep(0.25 + random())
        bdtr_list.counter += 1
    return seqout
