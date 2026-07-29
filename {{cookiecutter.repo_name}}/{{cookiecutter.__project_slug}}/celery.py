from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "aghamohandes_backend.settings"
)


# set the default Django settings module for the 'celery' program.
app = Celery(
    "aghamohandes-backend",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

app.config_from_object("django.conf:settings")
app.conf.timezone = "Asia/Tehran"
packages = []
app.autodiscover_tasks(packages=packages)


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
