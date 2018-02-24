## python 3, Flask + gunicorn api

---

### use gunicorn for multi-thread api
使用gunicorn加上flask，讓flask的api可以用multi-thread的方式執行。

#### execute command line
```
# origin: use flask

$ python {filename.py}
```

```
# use gunicorn
# gunicorn -w {core_num} -b {ip:port} {file_name(no .py)}:{variable of Flask(__name__) use in file}

$ gunicorn -w 8 -b 0.0.0.0:8080 osc_api:app
```

執行指令改變，push到CF的manifest.yml, Procfile的執行指令都要更改。
requirements.txt檔案中要加入gunicorn，才能執行multi-process。

