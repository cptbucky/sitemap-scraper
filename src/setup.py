from setuptools import setup

setup(
    name='sitemapcli',
    version='0.0.1',
    packages=['sitemapcli'],
    entry_points={
        'console_scripts': [
            'sitemapcli = sitemapcli.__main__:main'
        ]
    })