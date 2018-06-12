# settings.py
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

KAFKA_URL = os.getenv('KAFKA_URL')
KAFKA_CLIENT_CERT = os.getenv('KAFKA_CLIENT_CERT')
KAFKA_CLIENT_CERT_KEY = os.getenv('KAFKA_CLIENT_CERT_KEY')
KAFKA_TRUSTED_CERT = os.getenv('KAFKA_TRUSTED_CERT')
KAFKA_PREFIX = os.getenv('KAFKA_PREFIX')

TOPIC1 = os.getenv('TOPIC1')
TOPIC2 = os.getenv('TOPIC2')

TOPIC1_WITH_PREFIX = KAFKA_PREFIX + TOPIC1
TOPIC2_WITH_PREFIX = KAFKA_PREFIX + TOPIC2