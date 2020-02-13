''' __main__
'''
# pragma: no cover
import sys
from random import randint

from bdtr import bdtr

if not sys.argv[3:]:
    to_lang = 'zh'
else:
    to_lang = sys.argv[-1]

if not sys.argv[2:]:
    from_lang = 'en'
else:
    from_lang = sys.argv[-2]

if sys.argv[1:]:
    print('Provide some English text')
    text = 'test ' + str(randint(0, sys.maxsize))
else:
    text = sys.argv[1:-2]

# resu = bdtr(text, from_lang, to_lang, cache=False)

resu = bdtr(text, from_lang, to_lang)

print(f'{text} trans: [{resu}]')
