from setuptools import setup, find_packages

LONG_DESCRIPTION_FILES = ["README.rst", "AUTHORS.rst", "CHANGELOG.rst"]

# TODO replace long_description
setup(
    name="core-kinesis-conducer",
    version="0.0.1",
    description="Girl Effect Core Kinesis Conducer",
    #long_description="".join(open(filename, "r").read() for filename in LONG_DESCRIPTION_FILES),
    author="Praekelt Consulting",
    author_email="dev@praekelt.com",
    license="BSD",
    url="https://github.com/girleffect/core-kinesis-conducer",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
    # TODO: Cleanup not all are required
    install_requires=[
        "atomicwrites==1.2.1",
        "attrs==18.2.0",
        "boto3==1.9.57",
        "botocore==1.12.57",
        "docutils==0.14",
        "environs==4.0.0",
        "filelock==3.0.10",
        "jmespath==0.9.3",
        "jsonschema==2.6.0",
        "kinesis-python==0.1.8",
        "marshmallow==2.16.3",
        "mccabe==0.6.1",
        "mock==2.0.0",
        "more-itertools==4.3.0",
        "offspring==0.1.1",
        "pbr==5.1.1",
        "pluggy==0.8.0",
        "py==1.7.0",
        "pycodestyle==2.4.0",
        "pyflakes==2.0.0",
        "python-dateutil==2.7.5",
        "python-dotenv==0.10.0",
        "pytz==2018.7",
        "s3transfer==0.1.13",
        "six==1.11.0",
        "toml==0.10.0",
        "tox==3.5.3",
        "urllib3==1.24.1",
        "virtualenv==16.1.0"
    ]
)
