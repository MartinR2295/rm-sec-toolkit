import pathlib
from setuptools import setup, find_packages
from rmsectkf.core.helpers.update_helper import UpdateHelper

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="rm-sec-toolkit",
    version=UpdateHelper.get_current_version_number(),
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
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "rm-options==2.0.1",
        "scapy==2.4.5",
        "requests==2.25.1"
    ],
    scripts=[
        "rm-sec-toolkit"
    ],
    entry_points={
        "console_scripts": []
    },
)
