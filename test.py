import unittest

from test_settings import (
    KAFKA_URL, 
    KAFKA_CLIENT_CERT, 
    KAFKA_CLIENT_CERT_KEY, 
    KAFKA_TRUSTED_CERT,
    KAFKA_PREFIX,
    TOPIC1,
    TOPIC2,
    TOPIC1_WITH_PREFIX,
    TOPIC2_WITH_PREFIX
)
from heroku_kafka import HerokuKafkaProducer, HerokuKafkaConsumer
from kafka import KafkaProducer, KafkaConsumer

kafka_params = {
    'url': KAFKA_URL,
    'ssl_cert': KAFKA_CLIENT_CERT,
    'ssl_key': KAFKA_CLIENT_CERT_KEY,
    'ssl_ca': KAFKA_TRUSTED_CERT,
    'prefix': KAFKA_PREFIX
}

class TestKafka(unittest.TestCase):

    def test_kafka_producer(self):
        """
        Test that HerokuKafakProducer does not create any errors
        and is an instance of KafkaProducer (python_kafka)
        """
        producer = HerokuKafkaProducer(**kafka_params)
        assert isinstance(producer, KafkaProducer)
        producer.close()

    def test_kafka_message_send(self):
        """
        Test that no errors are thrown, and it doesn't hang when you send a message
        """
        producer = HerokuKafkaProducer(**kafka_params)
        #producer.send(TOPIC1, b"some message")
        producer.flush() # Force event send
        producer.close()

    def test_kafka_message_send_with_key(self):
        """
        Test that no errors are thrown, and it doesn't hang when you send a message
        """
        producer = HerokuKafkaProducer(**kafka_params)
        result = producer.send(
            topic=TOPIC1, 
            key=b"hello",
            value=b"some message"
            )
        producer.flush() # Force event send
        producer.close()

    def test_kafka_consumer(self):
        """
        Test that the HerokuKafkaConsumer does not create any errors 
        and is an instance of KafkaConsumer (python_kafka)
        """
        consumer = HerokuKafkaConsumer(TOPIC1, **kafka_params)
        assert isinstance(consumer, KafkaConsumer)
        consumer.close()

    def test_kafka_consumer_single_topic(self):
        """
        Test that consumer works with a single topic and prefixes it correctly
        """
        consumer = HerokuKafkaConsumer(TOPIC1, **kafka_params)
        assert consumer.subscription() == {TOPIC1_WITH_PREFIX, }
        consumer.close()

    def test_kafka_consumer_multiple_topic(self):
        """
        Test that the consumer works with multiple topics and prefixes them correctly
        """
        consumer = HerokuKafkaConsumer(TOPIC1, TOPIC2, **kafka_params)
        assert consumer.subscription() == {TOPIC1_WITH_PREFIX, TOPIC2_WITH_PREFIX}
        consumer.close()

    def test_kafka_consumer_subscribe(self):
        """
        Test that the consumer works with subscribe and prefixes topics correctly
        """
        consumer = HerokuKafkaConsumer(**kafka_params)
        consumer.subscribe(topics=(TOPIC1, TOPIC2))
        assert consumer.subscription() == {TOPIC1_WITH_PREFIX, TOPIC2_WITH_PREFIX}
        consumer.close()

            
if __name__ == '__main__':
    unittest.main()