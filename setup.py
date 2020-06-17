try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': '一个简单的小说阅读软件',
    'author': 'zoemurmure',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'zoemurmure@gmail.com',
    'version': '1.0',
    'install_requires': ['nose'],
    'packages': ['TextViewer'],
    'scripts': [],
    'name': 'TextViewer'
}

setup(**config)