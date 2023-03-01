# transactions-system

### Build application
```
$ git clone https://github.com/Djama-Mo/transactions-system && cd transactions-system
$ python3 -m venv venv && . venv/bin/activate
$ pip install -r requirements.txt
```
### RUN
```
$ uvicorn main:app --reload
$ celery -A main.celery worker --loglevel=info -Q fund --concurrency=1
```

## Now visit http://localhost:8000/docs
