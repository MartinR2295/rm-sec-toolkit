import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="rm-sec-toolkit",
    version="0.1.0",
    description="module based security toolkit framework for python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/MartinR2295/rm-sec-toolkit",
    author="Martin Rader",
    author_email="m1rader@edu.aau.at",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["rmsectkf"],
    include_package_data=True,
    install_requires=[
        "rm-options==1.2.0",
        "scapy==2.4.5"
    ],
    # add script which move rm-sec-toolkit.py to /usr/bin/rm-sec-toolkit
    # also move modules to /usr/share/rm-sec-toolkit/modules

    entry_points={
        "console_scripts": []
    },
)