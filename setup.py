try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': '一个简单的小说阅读软件',
    'author': 'zoemurmure',
    'url': 'https://github.com/zoemurmure/TextViewer',
    'download_url': 'https://github.com/zoemurmure/TextViewer',
    'author_email': 'zoemurmure@gmail.com',
    'version': '1.0',
    'install_requires': [''],
    'packages': ['TextViewer'],
    'include_package_data': True,  
    'scripts': ['bin/textviewer.py'],
    'name': 'TextViewer',
    'zip_safe': False,

}

setup(**config)