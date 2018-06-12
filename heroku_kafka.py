import collections
import tempfile
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from kafka import KafkaProducer, KafkaConsumer

class HerokuKafka():

    def __init__(self, url, ssl_cert, ssl_key, ssl_ca, prefix, *args, **kwargs):
        """
        Runs setup
        """
        self.kafka_url = url
        self.topic_prefix = prefix
        self.ssl = {
            "cert": {"suffix": ".crt", "content": ssl_cert},
            "key": {"suffix": ".key", "content": ssl_key},
            "ca": {"suffix": ".crt", "content": ssl_ca}
        }

        self.config = kwargs
        self.get_config()

    def get_config(self):
        """
        Sets up the basic config from the variables passed in
        all of these are from what Heroku gives you.
        """
        self.create_ssl_certs()

        config = {
            "bootstrap_servers": self.get_brokers(),
            "security_protocol": 'SSL',
            "ssl_cafile": self.ssl["ca"]["file"].name,
            "ssl_certfile": self.ssl["cert"]["file"].name,
            "ssl_keyfile": self.ssl["key"]["file"].name,
            "ssl_check_hostname": False,
            "ssl_password": None
        }
        self.config.update(config)

    def get_brokers(self):
        """
        Parses the KAKFA_URL and returns a list of hostname:port pairs in the format
        that kafka-python expects.
        """
        return ['{}:{}'.format(parsedUrl.hostname, parsedUrl.port) for parsedUrl in
                [urlparse(url) for url in self.kafka_url.split(',')]]

    def create_ssl_certs(self):
        """
        Creates SSL cert files
        """
        for key, file in self.ssl.items():
            file["file"] = self.create_temp_file(file["suffix"], file["content"])


    def create_temp_file(self, suffix, content):
        """ 
        Creates file, because environment variables are by default escaped it
        encodes and then decodes them before write so \n etc. work correctly.
        """
        temp = tempfile.NamedTemporaryFile(suffix=suffix)
        temp.write(content.encode('latin1').decode('unicode_escape').encode('utf-8'))
        temp.seek(0) # Resets the temp file line to 0
        return temp

    def prefix_topic(self, topics):
        """
        Adds the topic_prefix to topic(s) supplied
        """
        if not self.topic_prefix or not topics:
            return topics

        if not isinstance(topics, str) and isinstance(topics, collections.Iterable):
            return [self.topic_prefix + topic for topic in topics]

        return self.topic_prefix + topics


class HerokuKafkaProducer(KafkaProducer):
    """
    Heroku Kafka Producer
    Inherits from: kafka.KafkaProducer (python_kafka lib)
    """

    def __init__(self, *args, **kwargs):
        """
        HerokuKafka turns heroku's kafka env variables into settings
        that python_kafka understands.
        """
        self.heroku_kafka = HerokuKafka(**kwargs)
        super(HerokuKafkaProducer, self).__init__(*args, **self.heroku_kafka.config)

    def send(self, topic, *args, **kwargs):
        """
        Appends the prefix to the topic before sendingf
        """
        prefix_topic = self.heroku_kafka.prefix_topic(topic)
        return super(HerokuKafkaProducer, self).send(prefix_topic, *args, **kwargs)


class HerokuKafkaConsumer(KafkaConsumer):
    """
    Heroku Kafka Consumer
    Inherits from: kafka.KafkaConsumer (python_kafka lib)
    """

    def __init__(self, *topics, **kwargs):
        """
        HerokuKafka turns heroku's kafka env variables into settings
        that python_kafka understands.
        Prefixes topic with the kafka topic_prefix
        """
        self.heroku_kafka = HerokuKafka(**kwargs)
        prefix_topics = self.heroku_kafka.prefix_topic(topics)
        super(HerokuKafkaConsumer, self).__init__(*prefix_topics, **self.heroku_kafka.config)

    def subscribe(self, topics=(), *args, **kwargs):
        prefix_topics = self.heroku_kafka.prefix_topic(topics)
        return super(HerokuKafkaConsumer, self).subscribe(topics=prefix_topics, *args, **kwargs)


