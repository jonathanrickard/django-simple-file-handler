import os
from setuptools import (
    find_packages,
    setup,
)


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='django_simple_file_handler',
    version='0.1.4',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A Django app for uploading documents and images',
    long_description=README,
    url='http://www.jonathanrickard.com/',
    author='Jonathan Rickard',
    author_email='jonathan.rickard@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)


install_requires=[
   'Django>=1.11,<2.0',
]
