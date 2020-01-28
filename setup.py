"""
Flask-Wiki
-------------

This is the description for that library
"""
from setuptools import setup


setup(
    name='Flask-Wiki',
    version='0.0.1',
    url='http://github.com/jma/flask-wiki/',
    license='BSD',
    author='Johnny Mariéthoz',
    author_email='Johnny.Mariethoz@rero.ch',
    description='A simple file based wiki using Flask.',
    long_description=__doc__,
    py_modules=['flask_wiki'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    packages=['flask_wiki'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)