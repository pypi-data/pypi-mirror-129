# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['databank']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy>=1.4.27,<2.0.0']

setup_kwargs = {
    'name': 'databank',
    'version': '0.1.1',
    'description': 'Databank is an easy-to-use Python library for making raw SQL queries in a multi-threaded environment.',
    'long_description': '# Databank\n\n[![PyPI](https://img.shields.io/pypi/v/databank.svg)](https://pypi.org/project/databank) ![GitHub Actions](https://github.com/snapADDY/databank/actions/workflows/main.yml/badge.svg)\n\nDatabank is an easy-to-use Python library for making raw SQL queries in a multi-threaded environment.\n\nNo ORM, no frills. Only raw SQL queries and parameter binding. Thread-safe. Built on top of [SQLAlchemy](https://www.sqlalchemy.org/).\n\n## Installation\n\nYou can install the latest stable version from [PyPI](https://pypi.org/project/databank/)\n\n```\n$ pip install databank\n```\n\n**Adapters not included.** Install e.g. `psycopg2` for PostgreSQL:\n\n```\n$ pip install psycopg2\n```\n\n## Usage\n\nConnect to the database of your choice:\n\n```python\n>>> from databank import Database\n>>> db = Database("postgresql://user:password@localhost/db", pool_size=2)\n```\n\nThe keyword arguments are passed directly to SQLAlchemy\'s `create_engine()` function. Depending on the database you connect to, you have options like setting the size of connection pools.\n\n> If you are using `databank` in a multi-threaded environment (e.g. in a web application), make sure the pool size is at least the number of threads.\n\nLet\'s create a simple table:\n\n```python\n>>> db.execute("CREATE TABLE beatles (id SERIAL PRIMARY KEY, member TEXT NOT NULL);")\n```\n\nYou can insert multiple rows at once:\n\n```python\n>>> params = [\n...     {"id": 0, "member": "John"},\n...     {"id": 1, "member": "Paul"},\n...     {"id": 2, "member": "George"},\n...     {"id": 3, "member": "Ringo"}\n... ]\n>>> db.execute_many("INSERT INTO beatles (id, member) VALUES (:id, :member);", params)\n```\n\nFetch a single row:\n\n```python\n>>> db.fetch_one("SELECT * FROM beatles;")\n{\'id\': 0, \'member\': \'John\'}\n```\n\nBut you can also fetch `n` rows:\n\n```python\n>>> db.fetch_many("SELECT * FROM beatles;", n=2)\n[{\'id\': 0, \'member\': \'John\'}, {\'id\': 1, \'member\': \'Paul\'}]\n```\n\nOr all rows:\n\n```python\n>>> db.fetch_all("SELECT * FROM beatles;")\n[{\'id\': 0, \'member\': \'John\'},\n {\'id\': 1, \'member\': \'Paul\'},\n {\'id\': 2, \'member\': \'George\'},\n {\'id\': 3, \'member\': \'Ringo\'}]\n```\n',
    'author': 'snapADDY GmbH',
    'author_email': 'info@snapaddy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
