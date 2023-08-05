# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vanoma_api_utils',
 'vanoma_api_utils.django',
 'vanoma_api_utils.response_types',
 'vanoma_api_utils.rest_framework']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.9,<4.0.0',
 'dataclasses-json>=0.5.6,<0.6.0',
 'djangorestframework-camel-case>=1.2.0,<2.0.0',
 'djangorestframework>=3.12.4,<4.0.0',
 'phonenumbers>=8.12.37,<9.0.0',
 'pytest>=6.2.5,<7.0.0',
 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'vanoma-api-utils',
    'version': '0.10.0',
    'description': 'Python utils for vanoma APIs',
    'long_description': None,
    'author': 'Vanoma',
    'author_email': 'contact@vanoma.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
