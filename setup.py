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
        "Documentation": "https://catalystcoop-pudl-catalog.readthedocs.io",
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
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={"": ["*.yml", "*.yaml"]},
    zip_safe=False,
    python_requires=">=3.8,<3.12",
    install_requires=[
        "boto3==1.24.59",
        "s3fs>=2021.7,<2022.11.1",
        "gcsfs>=2021.7,<2022.11.1",
        "intake_parquet>=0.2.3,<0.3",
        "intake_sqlite>=0.2.0",
        "msgpack>=1,<2",
    ],
    extras_require={
        "dev": [
            "black>=22,<23",  # A deterministic code formatter
            "isort>=5,<6",  # Standardized import sorting
            "tox>=3.20,<5",  # Python test environment manager
            "twine>=3.3,<5.0",  # Used to make releases to PyPI
        ],
        "docs": [
            "doc8>=0.9,<1.1",  # Ensures clean documentation formatting
            "furo>=2022.4.7",
            "sphinx>=4.0,<5.4",  # The default Python documentation redering engine
            "sphinx-autoapi>=1.8,<2.1",  # Generates documentation from docstrings
            "sphinx-issues>=1.2,<4.0",  # Allows references to GitHub issues
        ],
        "tests": [
            "bandit>=1.6,<2",  # Checks code for security issues
            "coverage>=5.3,<8",  # Lets us track what code is being tested
            "doc8>=0.9,<1.1",  # Ensures clean documentation formatting
            "flake8>=4,<7",  # A framework for linting & static analysis
            "flake8-builtins>=1.5,<3",  # Avoid shadowing Python built-in names
            "flake8-colors>=0.1.9,<0.2",  # Produce colorful error / warning output
            "flake8-docstrings>=1.5,<2",  # Ensure docstrings are formatted well
            "flake8-rst-docstrings>=0.2,<0.4",  # Allow use of ReST in docstrings
            "flake8-use-fstring>=1,<2",  # Highlight use of old-style string formatting
            "mccabe>=0.6,<0.8",  # Checks that code isn't overly complicated
            "pandas>=1.4,<1.6",
            "pep8-naming>=0.12,<0.14",  # Require PEP8 compliant variable names
            "pre-commit>=2.9,<3",  # Allow us to run pre-commit hooks in testing
            "pydocstyle>=5.1,<7",  # Style guidelines for Python documentation
            "pytest>=6.2,<8",  # Our testing framework
            "pytest-cov>=2.10,<5.0",  # Pytest plugin for working with coverage
            "rstcheck[sphinx]>=5,<7",  # ReStructuredText linter
            "tox>=3.20,<5",  # Python test environment manager
        ],
    },
    setup_requires=["setuptools_scm"],
    entry_points={
        "intake.catalogs": [
            "pudl_cat = pudl_catalog:pudl_cat",
        ]
    },
)
