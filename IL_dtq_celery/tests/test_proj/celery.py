from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('proj',
             broker='redis://localhost',
             backend='redis://localhost',
             include=['IL_dtq_celery.tests.test_proj.tasks'])

app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()

