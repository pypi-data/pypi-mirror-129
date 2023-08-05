# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlmt']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.0,<2.0.0', 'pandas>=1.0,<2.0']

setup_kwargs = {
    'name': 'mlmt',
    'version': '0.0.4',
    'description': 'A Machine Learning Multi-Tool',
    'long_description': "# A Machine Learning Multi-Tool (mlmt)\n\n![](https://img.shields.io/pypi/v/mlmt)\n![](https://img.shields.io/pypi/format/mlmt)\n![](https://img.shields.io/pypi/pyversions/mlmt)\n![](https://img.shields.io/pypi/l/mlmt)\n\nA collection of loosely organized code to assist machine learning research.\n\n## Installation\n\n```sh\npip install --upgrade mlmt\n```\n\n## Usage\n\n```python\nimport mlmt\n```\n\n## Developer's Guide\n\nSee project [wiki](https://github.com/rlan/mlmt/wiki).\n",
    'author': 'Rick Lan',
    'author_email': 'rlan@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rlan/mlmt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
