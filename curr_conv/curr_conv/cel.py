from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

import requests, json
from celery import current_app
from celery.bin import worker
from celery import Celery
from celery.task import periodic_task

# set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
#
# app = Celery('conv')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app = current_app._get_current_object()

# app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

worker = worker.worker(app=app)

from datetime import timedelta

app = Celery('tasks', backend='amqp',  broker='amqp://guest@localhost//')

@periodic_task(run_every=timedelta(seconds=10))
def get_api_data(request):
    s = requests.Session()
    form = request.GET
    if 'from' in form:
        f_f = form['from']
    else:
        f_f = 'BTC'

    if 'to' in form:
        f_t = form['to']
    else:
        f_t = 'USD'
    data = json.loads(s.get('https://api.cryptonator.com/api/ticker/%s-%s' % (f_f.lower(), f_t.lower())).text)
    return data

if __name__ == '__main__':


    options = {
        # 'broker': 'amqp://guest:guest@localhost:5672//',
        'loglevel': 'INFO',
        'traceback': True,
    }

    worker.run(**options)
