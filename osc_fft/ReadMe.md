## python 3, Flask api
#### import: numpy, scipy, matplotlib

---
### push CF 設定檔

【reference】
https://github.com/ihuston/python-cf-examples/blob/master/02-pydata-spyre-app/sine_wave.py
https://github.com/cloudfoundry/python-buildpack/tree/db6474a50b99348da6c5256bb2133e03745ffd52/fixtures/miniconda_python_3


#### _tkinter error message on local server.
因為matplotlib中，需要在environment中安裝 _tkinter，
否則會出現no module的error message，
在local server可以使用command line安裝：
```
$ sudo apt-get install python3-tk
```


#### _tkinter error message on CF.
push到CF上，無法使用command line安裝，
需要在code中調整import matplotlib的部份。
```
# file: test.py

# import完matplotlib後，加上 matplotlib.use('Agg')，
# (需要加在code最一開頭)
# push到CF上之後，不會跳_tkinter的error message
# 在那行之後再import其他matplotlib使用到的module

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
```
※ code中不能使用plt.show()，這類會跳出畫圖框的function。


#### manifest.yml
※ buildpack：選擇python_buildpack。_tkinter的問題，可以import外部的python_buildpack處理。
※ command：要執行python api的指令。
```
 ---
applications:
- name: osc_api
  memory: 2048MB
  buildpack: python_buildpack
  command: gunicorn -w 16 -b 0.0.0.0:8080 osc_api:app
```


#### requirements.txt
※ 需要import的python lib
```
Flask
requests
numpy
scipy
matplotlib
gunicorn
configparser
```


#### runtime.txt
※ 使用的python 版本
```
python-3.6.1
```


#### Procfile
※ web後面接要執行python api的指令。
```
web: gunicorn -w 16 -b 0.0.0.0:8080 osc_api:app
```

---

### python code

#### test_simple_json.py
push到CF，port要改成8080
```
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5500, debug=True)
```

---

### use gunicorn for multi-thread api
使用gunicorn加上flask，讓flask的api可以用multi-thread的方式執行。

#### install
```
# 使用pipenv 虛擬環境與lib管理tool進行安裝

$ pipenv install gunicorn
```

#### execute command line
```
# origin: use flask

$ python {filename.py}
```

```
# use gunicorn
# gunicorn -w {core_num} -b {ip:port} {file_name(no .py)}:{variable of Flask(__name__) use in file}
# 若要push到CF，port要改成8080

$ gunicorn -w 8 -b 0.0.0.0:8080 osc_api:app
```

執行指令改變，push到CF的manifest.yml, Procfile的執行指令都要更改。
requirements.txt檔案中要加入gunicorn，才能執行multi-process。

