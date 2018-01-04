# settings.py
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

KAFKA_URL = os.environ.get('KAFKA_URL')
KAFKA_CLIENT_CERT = os.environ.get('KAFKA_CLIENT_CERT')
KAFKA_CLIENT_CERT_KEY = os.environ.get('KAFKA_CLIENT_CERT_KEY')
KAFKA_TRUSTED_CERT = os.environ.get('KAFKA_TRUSTED_CERT')
KAFKA_PREFIX = os.environ.get('KAFKA_PREFIX')

TOPIC1 = os.environ.get('TOPIC1')
TOPIC2 = os.environ.get('TOPIC2')

TOPIC1_WITH_PREFIX = KAFKA_PREFIX + TOPIC1
TOPIC2_WITH_PREFIX = KAFKA_PREFIX + TOPIC2