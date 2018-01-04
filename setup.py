from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    version='1.0',            # Update the version number for new releases
    name='heroku-kafka',        # This is the name of your PyPI-package.
    description='Python 2 & 3 kafka package for use with heroku\'s kafka.',
    classifiers=[
        'Development Status :: 5 - Production/Stable'
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ],
    url='https://github.com/HubbleHQ/heroku-kafka',
    author='Hubble'
    author_email='dev@hubblehq.com'
    license='MIT',
    scripts=['heroku_kafka']    # The name of your scipt, and also the command you'll be using for calling it
)