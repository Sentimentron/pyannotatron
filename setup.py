from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyannotatron',
    version='0.2.3',
    description='Python bindings for Annotatron - a data management system for machine learning applications',
    long_description=long_description,
    url='https://github.com/Sentimentron/pyannotatron',
    author_email='richard@sentimentron.co.uk',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4'
   ],
   keywords='ml database',
   py_modules=['pyannotatron.models'],
   install_requires=['requests'],
   project_urls={
    'Bug Reports': 'https://github.com/Sentimentron/pyannotatron/issues',
    'Source': 'https://github.com/Sentimentron/pyannotatron'
   },
)
