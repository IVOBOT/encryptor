from setuptools import setup

APP = ['main.py']
OPTIONS = {
    'argv_emulation': False,
    'packages': ['Frontend', 'cryptography', 'cffi', 'key_generator'],
    'iconfile':'resources/lock.ico'
}

setup(
    name='encryptor',
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)