import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journey_hub.settings')

app = Celery('journey_hub')

# Using Redis as the message broker
app.conf.broker_url = os.getenv('CELERY_BROKER_URL')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(['tasks.processing'])
