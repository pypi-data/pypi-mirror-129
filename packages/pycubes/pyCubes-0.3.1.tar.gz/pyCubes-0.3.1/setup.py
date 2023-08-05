# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cubes']

package_data = \
{'': ['*']}

install_requires = \
['nbtlib==2.0.4']

extras_require = \
{'docs': ['mkdocs-material>=7.3.6,<8.0.0',
          'mkdocs-static-i18n>=0.21,<0.23',
          'lazydocs>=0.4.8,<0.5.0',
          'pydocstyle>=6.1.1,<7.0.0']}

setup_kwargs = {
    'name': 'pycubes',
    'version': '0.3.1',
    'description': 'Library for creating servers and clients Minecraft Java Edition',
    'long_description': '<h1 align="center">pyCubes</h1>\n\n<p align="center">\n<a href="https://pypi.org/projects/pycubes"><img alt="PyPI" src="https://img.shields.io/pypi/v/pycubes"></a>\n<a href="https://pypi.org/projects/pycubes"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/pycubes"></a>\n<a href="https://pypi.org/projects/pycubes"><img alt="PyPI - License" src="https://img.shields.io/pypi/l/pyCubes"></a>\n<a href="https://pepy.tech/project/pycubes"><img alt="Downloads" src="https://pepy.tech/badge/pycubes/month"></a>\n</p>\n<p align="center">\n<a href="https://github.com/DavisDmitry/pyCubes/actions/workflows/test.yml"><img alt="Test" src="https://github.com/DavisDmitry/pyCubes/actions/workflows/test.yml/badge.svg"></a>\n<a href="https://github.com/DavisDmitry/pyCubes/actions/workflows/lint.yml"><img alt="Lint" src="https://github.com/DavisDmitry/pyCubes/actions/workflows/lint.yml/badge.svg"></a>\n<a href="https://codecov.io/gh/DavisDmitry/pyCubes"><img alt="codecov" src="https://codecov.io/gh/DavisDmitry/pyCubes/branch/master/graph/badge.svg?token=Y18ZNYT4YS"></a>\n</p>\n<p align="center">\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n<a href="https://pycqa.github.io/isort"><img alt="Imports: isort" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336"></a>\n</p>\n\n---\n<p align="center"><a href="https://pycubes.dmitrydavis.xyz/">Documentation</a></p>\n\n---\npyCubes is a library for creating servers and clients Minecraft Java Edition.\n\n**❗ 0.x versions are not stable. The library API is subject to change.**\n\nInstallation:\n\n```bash\npip install pyCubes\n```\n\n## Usage\n\nFirst you need to create application instance:\n\n```python3\nimport cubes\n\napp = cubes.Application()\n```\n\nAfter that add a low-level handler:\n\n```python3\nasync def process_handshake(packet_id: int, packet: cubes.ReadBuffer):\n    print(\'Protocol version:\', packet.varint)\n    print(\'Server host:\', packet.string)\n    print(\'Server port:\', packet.unsigned_short)\n    print(\'Next state:\', cubes.ConnectionStatus(packet.varint))\n\napp.add_low_level_handler(cubes.ConnectionStatus.HANDSHAKE, 0x00, process_handshake)\n```\n\nAll that remains is to launch the application:\n\n```python3\napp.run(\'127.0.0.1\', 25565)\n```\n\nA more detailed example can be found [here](https://github.com/DavisDmitry/pyCubes/blob/master/example.py).\n\nAll packages are described [here](https://wiki.vg/Protocol).\n',
    'author': 'Dmitry Davis',
    'author_email': 'dmitrydavis@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DavisDmitry/pyCubes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
