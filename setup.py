from setuptools import setup, find_packages

import guardianpie as app

setup(
    name="django-guardianpie",
    version=app.__version__,
    description="Tastypie authorization class that handles guardian permissions.",
    author="Zenobius Jiricek",
    author_email="airtonix@gmail.com",
    url="http://github.com/airtonix/django-guardianpie",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django-guardian',
        'django-tastypie',
    ],
)
