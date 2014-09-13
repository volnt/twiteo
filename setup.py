from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='twiteo',
    version='0.1',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'twiteo = twiteo.twiteo:main',
        ]
        },
    install_requires = [
        "tweepy==2.3",
        "pyowm==2.0"
    ],
)
