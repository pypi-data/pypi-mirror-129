# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_nest_thermostat']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.27,<2.0.0',
 'cleo>=0.8.1,<0.9.0',
 'httpx>=0.20.0,<0.21.0',
 'psycopg2>=2.9.1,<3.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'python-dotenv>=0.19.1,<0.20.0',
 'questionary>=1.10.0,<2.0.0',
 'rich>=10.13.0,<11.0.0']

entry_points = \
{'console_scripts': ['py-nest = py_nest_thermostat.main:application.run']}

setup_kwargs = {
    'name': 'py-nest-thermostat',
    'version': '0.0.0a2',
    'description': 'A Python CLI Nest Thermostat controller and dashborading tool',
    'long_description': "Version: `v0.0.0-a2`\n\n# py-nest-thermostat\n\nPython CLI Nest Controller and Reporting Tool.\n\n**Disclaimer:**\nThis project is very much work in progress while in version 0 anything can change, anything can break and some parts of the code are probably very ugly. Feel free to test it, contribute (see [CONTRIBUTING.md]()), report bugs\n\n**Get device stats:**\n![py nest stats](https://p56.f1.n0.cdn.getcloudapp.com/items/E0uKZLBb/dd63f9ff-a65e-4a95-9067-bc4c6f09d77a.gif?source=viewer&v=3e9c6a77683dd232609d610395417e58)\n\n**Set Device Temperature:**\n![py nest set temp](https://p56.f1.n0.cdn.getcloudapp.com/items/E0uKZLBZ/ca47db6b-3d8c-479c-b350-a0fdfd7416b1.gif?source=viewer&v=898e9184fbb67ee4471646039837bae8)\n\n## Features:\n\n- print device stats\n- set target temperature\n\n## Future Features:\n\n- capture device statistics into a database\n- plot device statistics over time\n- some ML?\n\n# Installation\n\nThe tool is intallable from [PyPI](https://pypi.org) via `pip` or [`pipx`](https://pypa.github.io/pipx/). But you must first set up access via Google's Developer console (which currently costs a one time $5 fee and is a bit of a pain).\n\n## Set Up Google and Authorization\n\nThis part of the process is a real pain, especially if you've never set up Authorization via Google. Luckily [Wouter Nieuwerth](https://www.wouternieuwerth.nl/about/) made a really nice [guide](https://www.wouternieuwerth.nl/controlling-a-google-nest-thermostat-with-python/) with pictures that I encourage you to check out\n\n### Google Documentation Links\n\nGoogle has some pretty extensive documentation:\n\n- [Nest Getting Started](https://developers.google.com/nest/device-access/get-started)\n- [Device Registration](https://developers.google.com/nest/device-access/registration)\n\nOnce setup, you will be able to access your nest devicesc, and manage your authorizations in the following places:\n\n- [Nest Device Access](https://console.nest.google.com/device-access/)\n- [Google Developers Console](https://console.developers.google.com/)\n\nIf you have issues, and neither the [step by step guide from Wouter](https://www.wouternieuwerth.nl/controlling-a-google-nest-thermostat-with-python/) nor the links above help you feel free to open an issue and if I have time I'll try and help out.\n\n## Install `py-nest-thermostat`\n\nIf you want to be able to access the tool from anywhere I recomment setting it up via [pipx](https://pypa.github.io/pipx/). Pipx will give you access to `py-nest` globally while keeping it in an isolated python virtual environment. The best of both worlds really!\n\nYou can install with pipx like so:\n\n```bash\npipx install py-nest-thermostat\n```\n\nIf you prefer to use regular `pip`, follow those steps:\n\n1. create a python3 virtual environment (with `venv` or `virtualenv` --up to you)\n2. activate the virtual environment (`source /path/to/virtual/environment`)\n3. `pip install py-nest-thermostat`\n\n# Usage\n\nUntil I write some more extensive docs, once you have installed the tool use use the CLI `--help` command\n\n```bash\npy-nest --help\n```\n",
    'author': 'Bastien Boutonnet',
    'author_email': 'bastien.b1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bastienboutonnet/py-nest-thermostat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
