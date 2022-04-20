#!/usr/bin/env python
"""A catalog of open data related to the US energy system."""
from pathlib import Path

from setuptools import find_packages, setup

readme_path = Path(__file__).parent / "README.rst"
long_description = readme_path.read_text()

setup(
    name="catalystcoop.pudl_catalog",
    use_scm_version=True,
    description=__doc__,
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Catalyst Cooperative",
    author_email="pudl@catalyst.coop",
    maintainer="Zane A. Selvans",
    maintainer_email="zane.selvans@catalyst.coop",
    url="https://github.com/catalyst-cooperative/pudl-catalog",
    project_urls={
        "Source": "https://github.com/catalyst-cooperative/pudl-catalog",
        "Issue Tracker": "https://github.com/catalyst-cooperative/pudl-catalog/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={"": ["*.yml", "*.yaml"]},
    zip_safe=False,
    python_requires=">=3.8,<3.11",
    install_requires=[
        "gcsfs>=2022,<2023",
        "intake>=0.6.5",
        "intake_parquet>=0.2.3",
        "intake_sql>=0.3.1",
        "msgpack>=1,<2",
        "pandas>=1.4,<1.5",
    ],
    extras_require={
        "release": [
            "twine>=3.3,<5.0",
        ],
        "tests": [
            "coverage>=5.3,<7.0",
            "flake8>=4,<5",
            "flake8-builtins~=1.5",
            "flake8-colors~=0.1",
            "flake8-docstrings~=1.5",
            "flake8-rst-docstrings~=0.2",
            "flake8-use-fstring~=1.0",
            "pre-commit>=2.9<3",
            "pytest>=6.2,<8",
            "pytest-cov>=2.10,<4.0",
            "tox>=3.20<4",
        ],
    },
    setup_requires=["setuptools_scm"],
    entry_points={
        "intake.catalogs": [
            "pudl_cat = pudl_catalog:pudl_cat",
        ]
    },
)
