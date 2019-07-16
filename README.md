# Heroku Kafka &middot; [![CircleCI](https://circleci.com/gh/HubbleHQ/heroku-kafka.svg?style=shield)](https://circleci.com/gh/HubbleHQ/heroku-kafka)

**THIS IS AN UNOFFICIAL PACKAGE**

Heroku Kafka is a python package to help you get setup quickly and easily with Kafka on Heroku. There is an [offical package](https://github.com/heroku/kafka-helper) that is possibly more secure however it has not been updated to support python 3 correctly and does not seem to be maintained anymore.

## Install

The easiest way to install the package is through pip.

```
pip install heroku-kafka
```

## Usage

This package uses the [kafka-python package](https://github.com/dpkp/kafka-python) and the `HerokuKafkaProducer` and `HerokuKafkaConsumer` classes both inherit from the kafka-python base classes, and will contain all the same methods.

Note: You can use this package on local by setting up an .env file using the same kafka
environment variables as you have on your heroku site.

Note: To test it is working on local I would install [heroku-kafka-util](https://github.com/osada9000/heroku-kafka-util) so you can see messages are being sent etc.

### Producer

```python
from heroku_kafka import HerokuKafkaProducer

"""
All the variable names here match the heroku env variable names.
Just pass the env values straight in and it will work.
"""
producer = HerokuKafkaProducer(
    url: KAFKA_URL, # Url string provided by heroku
    ssl_cert: KAFKA_CLIENT_CERT, # Client cert string
    ssl_key: KAFKA_CLIENT_CERT_KEY, # Client cert key string
    ssl_ca: KAFKA_TRUSTED_CERT, # Client trusted cert string
    prefix: KAFKA_PREFIX # Prefix provided by heroku
)

"""
The .send method will automatically prefix your topic with the KAFKA_PREFIX
NOTE: If the message doesn't seem to be sending try `producer.flush()` to force send.
"""
producer.send('topic_without_prefix', b"some message")
```

For all other methods and properties refer to: [KafkaProducer Docs](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html).

### Consumer

```python
from heroku_kafka import HerokuKafkaConsumer

"""
All the variable names here match the heroku env variable names,
just pass the env values straight in and it will work.

*topics are optional and you can pass as many as you want in for the consumer to track,
however if you want to subscribe after creation just use .subscribe as shown below.

Note: The KAFKA_PREFIX will be added on automatically so don't worry about passing it in.
"""
consumer = HerokuKafkaConsumer(
    'topic_without_prefix_1', # Optional: You don't need to pass any topic at all
    'topic_without_prefix_2', # You can list as many topics as you want to consume
    url: KAFKA_URL, # Url string provided by heroku
    ssl_cert: KAFKA_CLIENT_CERT, # Client cert string
    ssl_key: KAFKA_CLIENT_CERT_KEY, # Client cert key string
    ssl_ca: KAFKA_TRUSTED_CERT, # Client trusted cert string
    prefix: KAFKA_PREFIX # Prefix provided by heroku
)

"""
To subscribe to topic(s) after creating a consumer pass in a list of topics without the
KAFKA_PREFIX.
"""
consumer.subscribe(topics=('topic_without_prefix'))

"""
.assign requires a full topic name with prefix
"""
consumer.assign([TopicPartition('topic_with_prefix', 2)])

"""
Listening to events it is exactly the same as in kafka_python.
Read the documention linked below for more info!
"""
for msg in consumer:
    print (msg)
```

For all other methods and properties refer to: [KafkaConsumer Docs](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html).

## Known Issues

- `.assign` does not add in the topic prefix.
- .NamedTemporaryFile may not work properly on a Windows system

## Contribution

If you come across any issues feel free to fork and create a PR!

## Setup

Fork the repo, requires [Docker](https://www.docker.com/products/docker-desktop)

```bash
>>> git clone git@github.com:<fork-repo>.git
>>> cd <fork-repo>
>>> make dev-build
```

Create a .env file with working kafka information (that includes 2 working topics at the moment).

```
KAFKA_URL=
KAFKA_CLIENT_CERT=
KAFKA_CLIENT_CERT_KEY=
KAFKA_TRUSTED_CERT=
KAFKA_PREFIX=

TOPIC1=
TOPIC2=
```

NOTE: The way docker reads .env files is a bit strange. You can't have any quotes around your variable values and no new lines, replace all new lines with `\n`.

## Tests

**The only way to check to see if the package work is to run the tests.**

Please make sure that any extra code you write comes with a test, it doesn't need to be over the top but just check what you have written works.

All tests at the moment require a working kafka setup as its pretty hard to check it is connecting correctly without them. This means it will also require an internet connection. You can copy across the connection details from heroku's kafka environment variables - also note you will need 2 test topics.

To run the tests:

```bash
>>> make dev-test
```

## Distribution

To create & upload the package:

```bash
>>> make package
>>> make upload
```

NOTE: You will need to login to PIP to upload the package.

[https://packaging.python.org/tutorials/packaging-projects/](https://packaging.python.org/tutorials/packaging-projects/)
