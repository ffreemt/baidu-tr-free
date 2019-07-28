# baidu-tr-free

Baidu translate for free -- local cache plus throttling. Let's hope it lasts.

### Installation
* ```pip install baidu-tr-free -U```
* or install (pip or whatever) necessary requirements, e.g. ```
pip install js2py requests_cache jsonpath_rw``` or ```
pip install -r requirements.txt```
* Drop the file bdtr.py in any folder in your PYTHONPATH (check with import sys; print(sys.path)
  * Several valid TOKEN/BAIDUID are included.
* or clone the repo (e.g., ```git clone https://github.com/ffreemt/baidu-tr-free.git``` or download https://github.com/ffreemt/baidu-tr-free/archive/master.zip and unzip) and change to the baidu-tr-free folder and do a ```
python setup.py develop```

### Usage

```
from bdtr import bdtr
print(bdtr('hello world'))  # -> '你好，世界'
print(bdtr('hello world', to_lang='de'))  # ->'Hallo Welt'
print(bdtr('hello world', to_lang='jp'))  # ->'ハローワールド'
```

### Validation and Pressure Tests
* pip install pytest
* pytest
  * Average delay for throttling set to 0.6 s, ajdust as needed

### Acknowledgments

* Thanks to everyone whose code was used
* JS_SIGN (javascript code for signing) can be found on the net. It's also not too difficult to obtain some similar code from Chrome's devtools.
