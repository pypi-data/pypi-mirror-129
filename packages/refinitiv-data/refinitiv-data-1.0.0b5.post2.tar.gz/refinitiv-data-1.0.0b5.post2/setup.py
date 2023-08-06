# coding: utf-8
import os
import re

from setuptools import setup, find_packages

module_file = open("refinitiv/data/__init__.py").read()
metadata = dict(re.findall(r'__([a-z]+)__\s*=\s*"([^"]+)"', module_file))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="refinitiv-data",
    version=metadata["version"],
    description="Python package for retrieving data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-library-for-python",
    author="REFINITIV",
    author_email="",
    license="Apache 2.0",
    data_files=[("", ["LICENSE.md", "CHANGES.txt"])],
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests", "tests_*"]
    ),
    package_data={"": [os.path.join("_data", "refinitiv-data.config.json")]},
    zip_safe=False,
    python_requires=">3.6",
    install_requires=[
        "appdirs>=1.4.3",
        "eventemitter>=0.2.0",
        "httpx>=0.18",
        "mysql-connector-python",
        "nest_asyncio",
        "numpy>=1.11.0",
        "pandas>=1.1.0",
        "python-configuration>=0.8.2",
        "python-dateutil",
        "requests",
        "scipy",
        "six",
        "urllib3>=1.26.6",
        "validators",
        "watchdog>=0.10.2",
        "websocket-client>=0.58.0",
        # requests-async requirements
        "certifi",
        "chardet==3.*",
        "h2==3.*",
        "idna==2.*",
        "rfc3986==1.*", 
    ],
)
