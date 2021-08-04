# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    version="3.0.0",  # Update the version number for new releases
    name="heroku-kafka",  # This is the name of your PyPI-package.
    description="Python kafka package for use with heroku's kafka.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
    ],
    url="https://github.com/HubbleHQ/heroku-kafka",
    author="Hubble",
    author_email="dev@hubblehq.com",
    license="MIT",
    py_modules=["heroku_kafka"],
    install_requires=["kafka-python==1.4.6"],
)
