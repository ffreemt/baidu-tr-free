# baidu-tr-free

Baidu translate for free -- local cache plus throttling. Hope it lasts.

### Installing
* Install (pip or whatever) necessary requirements (e.g. ```pip install js2py requests_cache jsonpath_rw`` or pip -r requirements.txt`）
* Drop the file bdtr.py in any folder in your PYTHONPATH (check with import sys; print(sys.path)
* Several valid TOKEN/BAIDUID are included.

### Usage:

``` from bdtr import bdtr
print(bdtr('hello world') # -> '你好，世界'
print(bdtr('hello world', to_lang='de')  # ->'Hallo Welt'
print(bdtr('hello world', to_lang='jp')  # 'ハローワールド'
```

### Validation and Pressure Tests
* pip install pytest
* pytest
  * Average delay for throttling set to 0.6 s, ajdust as needed

### Acknowledgments

* Thanks to all whose code was used
* JS_SIGN can be found on the net. It's also not too difficult to obtain similar code from devtools.
