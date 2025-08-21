import sys
from os.path import abspath, dirname, join, normpath
from setuptools import find_packages, setup

INSTALL_PYTHON_REQUIRES = []
# We are intending to keep up to date with the supported Django>=3.2,<6.0 versions.
# For the official support, please visit:
# https://docs.djangoproject.com/en/dev/faq/install/#what-python-version-can-i-use-with-django
if (py_minor_version := sys.version_info.minor) in [8, 9, 10, 11]:
    django_python_version_install = (
        f"Django>=3.2,<6.0{'6' if py_minor_version >= 10 else '5'}"
    )
    INSTALL_PYTHON_REQUIRES.append(django_python_version_install)

setup(
    # Basic package information
    name="django-twilio",
    version="0.14.3.4-a1",
    packages=find_packages(),
    python_requires=">=3.10",

    # Packaging options
    zip_safe=False,
    include_package_data=True,

    # Package dependencies
    install_requires=[
        "setuptools>=36.2",
        "twilio>=8,<10",
        "django-phonenumber-field>=0.6",
        "phonenumbers>=8.10.22",
    ] + INSTALL_PYTHON_REQUIRES,

    # Metadata for PyPI
    author="Randall Degges",
    author_email="rdegges@gmail.com",
    maintainer="Jason Held",
    maintainer_email="jasonsheld@gmail.com",
    license="UNLICENSE",
    url="https://github.com/yourfork/django-twilio",
    keywords="twilio telephony call phone voip sms django",
    description="Build Twilio functionality into your Django apps.",
    long_description=open(
        normpath(join(dirname(abspath(__file__)), "README.rst"))
    ).read(),
    long_description_content_type="text/x-rst",
    project_urls={
        "Documentation": "https://django-twilio.readthedocs.io/en/latest/",
        "Code": "https://github.com/yourfork/django-twilio",
        "Tracker": "https://github.com/yourfork/django-twilio/issues",
    },
    classifiers=[
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Intended Audience :: Developers",
        "License :: Public Domain",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Implementation :: CPython",
        "Programming Language :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
