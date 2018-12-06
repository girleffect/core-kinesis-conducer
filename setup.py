from setuptools import setup, find_packages

LONG_DESCRIPTION_FILES = ["README.rst", "AUTHORS.rst", "CHANGELOG.rst"]

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
)
