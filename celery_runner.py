import os
from wsgi import app

from mrhlab.extensions import celery

app.app_context().push()