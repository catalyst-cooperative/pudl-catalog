#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="catalystcoop.pudl_catalog",
    version="0.0.1",
    description="A catalog of open data related to the US energy system.",
    packages=find_packages("src"),
    package_dir={"": "src"},
    maintainer="Zane Selvans",
    maintainer_email="zane.selvans@catalyst.coop",
    url="https://github.com/catalyst-cooperative/pudl-data-catalog",
    package_data={"": ["*.yaml"]},
    include_package_data=True,
    python_requires=">=3.8,<3.11",
    install_requires=[
        "intake>=0.6.5",
        "intake_parquet>=0.2.3",
        "intake_sql>=0.3.1",
    ],
    tests_require=["pytest"],
    zip_safe=False,
    license="MIT",
    entry_points={
        "intake.catalogs": [
            "pudl_cat = src/pudl_catalog:pudl_cat",
            "hourly_emissions_epacems = src/pudl_catalog:hourly_emissions_epacems",
        ]
    },
)
