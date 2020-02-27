# baidu-tr-free ![Python3.6 package](https://github.com/ffreemt/baidu-tr-free/workflows/Python3.6%20package/badge.svg)[![PyPI version](https://badge.fury.io/py/baidu-tr-free.svg)](https://badge.fury.io/py/baidu-tr-free)

Baidu translate for free -- local cache plus throttling. Let's hope it lasts.

### Broken or not
![Python3.6 package](https://github.com/ffreemt/baidu-tr-free/workflows/Python3.6%20package/badge.svg): failing indicates `broken`. In case of `failing`, try the following workaround: log in to https://passport.baidu.com first. Then use the Chrome browser to visit https://fanyi.baidu.com/v2transapi?from=en&to=zh&query=test, press F12 and then ctr-R (or any method) to open devtools' Network tab and reload. Locate `https://fanyi.baidu.com/v2transapi?from=en&to=zh` and obtain the BAIDUID and token strings in the headers. Plug in the BAIDUID and token strings to lines 66-67 in the  file `bdtr.py.`

### Fixed
* Text longer than 30 characters can be handled now.
* Auto-fetching BAIDUID and TOKEN

### Installation
```pip install -U baidu-tr-free```
or
* install (pip or whatever) necessary requirements, e.g. ```
pip install js2py requests_cache jsonpath_rw``` or ```
pip install -r requirements.txt```
* Drop the file bdtr.py in any folder in your PYTHONPATH (check with import sys; print(sys.path)
  * Several valid TOKEN/BAIDUID are included.
* or clone the repo (e.g., ```git clone https://github.com/ffreemt/baidu-tr-free.git``` or download https://github.com/ffreemt/baidu-tr-free/archive/master.zip and unzip) and change to the baidu-tr-free folder and do a ```
python setup.py develop```

### Usage
Log in to https://passport.baidu.com  using Chrome: `bdtr` needs the cookies info (`BAIDUID`) from the Chrome browser on baidu.com.

```
from bdtr import bdtr
print(bdtr('hello world'))  # -> '你好，世界'
print(bdtr('hello world', to_lang='de'))  # ->'Hallo Welt'
print(bdtr('hello world', to_lang='jp'))  # ->'ハローワールド'
```
`to_lang='fr'` does not seem to work tho.

### Validation and Pressure Tests
* pip install pytest
* pytest
  * Average delay for throttling set to 0.6 s, ajdust as needed

### Acknowledgments

* Thanks to everyone whose code was used
* JS_SIGN (javascript code for signing) can be found on the net. It's also not too difficult to obtain some similar code from Chrome's devtools.
