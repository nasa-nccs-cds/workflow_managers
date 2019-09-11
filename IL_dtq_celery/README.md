### Celery installation
```
$ python3 -m venv celery
$ source celery/bin/activate
(celery)$ pip install "celery[redis]"
(celery)$ pip install pydap dask distributed xarray 
```

### Start Redis
```
(celery)$ redis-server
```

### Start Demo Worker Service
```
(celery)$ cd .../workflows
(celery)$ celery --app=IL_dtq_celery.tests.test_proj.celery:app worker -l info
```

### Run Demo Task

```
(celery)$ cd .../workflows
(celery)$ python IL_dtq_celery/tests/call_proj_task.py
```
