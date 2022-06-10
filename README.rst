The PUDL Data Catalog
=====================

.. readme-intro

.. image:: https://github.com/catalyst-cooperative/pudl-catalog/workflows/tox-pytest/badge.svg
   :target: https://github.com/catalyst-cooperative/pudl-catalog/actions?query=workflow%3Atox-pytest
   :alt: Tox-PyTest Status

.. image:: https://img.shields.io/codecov/c/github/catalyst-cooperative/pudl-catalog?style=flat&logo=codecov
   :target: https://codecov.io/gh/catalyst-cooperative/pudl-catalog
   :alt: Codecov Test Coverage

.. image:: https://img.shields.io/readthedocs/catalystcoop-pudl-catalog?style=flat&logo=readthedocs
   :target: https://catalystcoop-pudl-catalog.readthedocs.io/en/latest/
   :alt: Read the Docs Build Status

.. image:: https://img.shields.io/pypi/v/catalystcoop.pudl_catalog?style=flat&logo=python
   :target: https://pypi.org/project/catalystcoop.pudl_catalog/
   :alt: PyPI Latest Version

.. image:: https://img.shields.io/conda/vn/conda-forge/catalystcoop.pudl_catalog?style=flat&logo=condaforge
   :target: https://anaconda.org/conda-forge/catalystcoop.pudl_catalog
   :alt: conda-forge Version

.. image:: https://img.shields.io/pypi/pyversions/catalystcoop.pudl_catalog?style=flat&logo=python
   :target: https://pypi.org/project/catalystcoop.pudl_catalog
   :alt: Supported Python Versions

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Any color you want, so long as it's black.

This repository houses a data catalog distributing open energy system data
liberated by `Catalyst Cooperative <https://catalyst.coop>`__ as part of our
`Public Utility Data Liberation Project
<https://github.com/catalyst-cooperative/pudl>`__ (PUDL). It uses the `Intake
library <https://github.com/intake/intake>`__ developed by Anaconda to provide a
uniform interface to versioned data releases hosted on publicly accessible cloud
resources.

Catalog Contents
----------------

Currently available datasets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Raw FERC Form 1 DB (SQLite) -- `browse DB online <https://data.catalyst.coop/ferc1>`__
* PUDL DB (SQLite) -- `browse DB online <https://data.catalyst.coop/pudl>`__
* Census Demographic Profile 1 (SQLite)
* Hourly Emissions from the EPA CEMS (Apache Parquet)

Ongoing Development
-------------------

To track ongoing development of the PUDL Catalog you can follow these issues
in the main PUDL repository:

* `Intake SQLite Driver <https://github.com/catalyst-cooperative/pudl/issues/1156>`__
* `EPA CEMS Intake Catalog <https://github.com/catalyst-cooperative/pudl/issues/1564>`__
* `PUDL Intake Catalog <https://github.com/catalyst-cooperative/pudl/issues/1179>`__

See also:

* `pudl-catalog issues <https://github.com/catalyst-cooperative/pudl-catalog/issues>`__
* `intake-sqlite issues <https://github.com/catalyst-cooperative/pudl-catalog/issues>`__

PUDL Catalog Usage
------------------

Accessing Public Cloud Data with Requester Pays
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To control the cost of distributing potentially large quantities of public data, we are
using "requester pays." This means that whoever is downloading the data pays the modest
data egress fees. If you're not familiar with GCP or requester pays, we've written a
short guide to setting up a GCP project to work with this type of data. See the
`PUDL Catalog documentation <https://catalystcoop-pudl-catalog.readthedocs.io/en/latest/>`__.
for details, and also the
`GCP Documentation on accessing Requester Pays data <https://cloud.google.com/storage/docs/using-requester-pays#using>`__

Import the Intake Catalogs
~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``pudl_catalog`` registers itself as an available data source within Intake when
it's installed, so you can grab it from the top level Intake catalog. To see what data
sources are available within the catalog you turn it into a list (yes this is weird).

.. code:: py

   import intake
   import pandas as pd
   from pudl_catalog.helpers import year_state_filter

   pudl_cat = intake.cat.pudl_cat
   list(pudl_cat)

.. code:: text

  [
    'hourly_emissions_epacems',
    'hourly_emissions_epacems_partitioned',
    'pudl',
    'ferc1',
    'censusdp1tract'
  ]

Inspect the catalog data source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Printing the data source will show you the YAML that defines the source,
but with all the Jinja template fields interpolated and filled in:

.. code:: py

   pudl_cat.hourly_emissions_epacems

.. code:: text

   hourly_emissions_epacems:
     args:
       engine: pyarrow
       storage_options:
         simplecache:
           cache_storage: /home/zane/.cache/intake
       urlpath: simplecache::gs://intake.catalyst.coop/dev/hourly_emissions_epacems.parquet
     description: Hourly pollution emissions and plant operational data reported via
       Continuous Emissions Monitoring Systems (CEMS) as required by 40 CFR Part 75.
       Includes CO2, NOx, and SO2, as well as the heat content of fuel consumed and gross
       power output. Hourly values reported by US EIA ORISPL code and emissions unit
       (smokestack) ID.
     driver: intake_parquet.source.ParquetSource
     metadata:
       catalog_dir: /home/zane/code/catalyst/pudl-catalog/src/pudl_catalog/
       license:
         name: CC-BY-4.0
         path: https://creativecommons.org/licenses/by/4.0
         title: Creative Commons Attribution 4.0
       path: https://ampd.epa.gov/ampd
       provider: US Environmental Protection Agency Air Markets Program
       title: Continuous Emissions Monitoring System (CEMS) Hourly Data
       type: application/parquet

Data source specific metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``source.discover()`` method will show you some internal details of
the data source, including what columns are available and their data
types:

.. code:: py

   pudl_cat.hourly_emissions_epacems.discover()

.. code:: text

   {'dtype': {'plant_id_eia': 'int32',
     'unitid': 'object',
     'operating_datetime_utc': 'datetime64[ns, UTC]',
     'year': 'int32',
     'state': 'int64',
     'facility_id': 'int32',
     'unit_id_epa': 'object',
     'operating_time_hours': 'float32',
     'gross_load_mw': 'float32',
     'heat_content_mmbtu': 'float32',
     'steam_load_1000_lbs': 'float32',
     'so2_mass_lbs': 'float32',
     'so2_mass_measurement_code': 'int64',
     'nox_rate_lbs_mmbtu': 'float32',
     'nox_rate_measurement_code': 'int64',
     'nox_mass_lbs': 'float32',
     'nox_mass_measurement_code': 'int64',
     'co2_mass_tons': 'float32',
     'co2_mass_measurement_code': 'int64'},
    'shape': (None, 19),
    'npartitions': 1,
    'metadata': {'title': 'Continuous Emissions Monitoring System (CEMS) Hourly Data',
     'type': 'application/parquet',
     'provider': 'US Environmental Protection Agency Air Markets Program',
     'path': 'https://ampd.epa.gov/ampd',
     'license': {'name': 'CC-BY-4.0',
      'title': 'Creative Commons Attribution 4.0',
      'path': 'https://creativecommons.org/licenses/by/4.0'},
     'catalog_dir': '/home/zane/code/catalyst/pudl-catalog/src/pudl_catalog/'}}

Read some data from the catalog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To read data from the source you call it with some arguments. Here we’re
supplying filters (in “disjunctive normal form”) that select only a subset of
the available years and states. This limits the set of Parquet files that need
to be scanned to find the requested data (since the files are partitioned by
``year`` and ``state``) and also ensures that you don’t get back a 100GB
dataframe that crashes your laptop. These arguments are passed through to
`dask.dataframe.read_parquet()
<https://docs.dask.org/en/latest/generated/dask.dataframe.read_parquet.html>`__
since Dask dataframes are the default container for Parquet data. Given those
arguments, you convert the source to a Dask dataframe and the use ``.compute()``
on that dataframe to actually read the data and return a pandas dataframe:

.. code:: py

   filters = year_state_filter(
       years=[2019, 2020],
       states=["ID", "CO", "TX"],
   )
   epacems_df = (
       pudl_cat.hourly_emissions_epacems(filters=filters)
       .to_dask()
       .compute()
   )
   epacems_df[[
       "plant_id_eia",
       "unitid",
       "operating_datetime_utc",
       "year",
       "state",
       "facility_id",
       "unit_id_epa",
       "operating_time_hours",
       "gross_load_mw",
       "heat_content_mmbtu",
       "co2_mass_tons",
   ]].head()

.. csv-table::
   :header: plant_id_eia, unitid, operating_datetime_utc, year, state, facility_id, unit_id_epa, operating_time_hours, gross_load_mw, heat_content_mmbtu, co2_mass_tons

   469,4,2019-01-01 07:00:00+00:00,2019,CO,79,298,1.0,203.0,2146.2,127.2
   469,4,2019-01-01 08:00:00+00:00,2019,CO,79,298,1.0,203.0,2152.7,127.6
   469,4,2019-01-01 09:00:00+00:00,2019,CO,79,298,1.0,204.0,2142.2,127.0
   469,4,2019-01-01 10:00:00+00:00,2019,CO,79,298,1.0,204.0,2129.2,126.2
   469,4,2019-01-01 11:00:00+00:00,2019,CO,79,298,1.0,204.0,2160.6,128.1

For more usage examples see `the Jupyter notebook <https://github.com/catalyst-cooperative/pudl-catalog/blob/main/notebooks/pudl-catalog.ipynb>`__ at ``notebooks/pudl-catalog.ipynb``


Planned data distribution system
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We’re in the process of implementing automated nightly builds of all of our data
products for each development branch with new commits in the main PUDL
repository. This will allow us to do exhaustive integration testing and data
validation on a daily basis. If all of the tests and data validation pass, then
a new version of the data products (SQLite databases and Parquet files) will be
produced, and placed into cloud storage.

These outputs will be made available via a data catalog on a corresponding
branch in this ``pudl-catalog`` repository. Ingeneral only the catalogs and data
resources corresponding to the ``HEAD`` of development and feature branches will
be available. Releases that are tagged on the ``main`` branch will be retained
long term.

The idea is that for any released version of PUDL, you should also be able to
install a corresponding data catalog, and know that the software and the data
are compatible. You can also install just the data catalog with minimal
dependencies, and not need to worry about the PUDL software that produced it at
all, if you simply want to access the DBs or Parquet files directly.

In development, this arrangement will mean that every morning you should have
access to a fully processed set of data products that reflect the branch of code
that you’re working on, rather than the data and code getting progressively
further out of sync as you do development, until you take the time to re-run the
full ETL locally yourself.

Benefits of Intake Catalogs
---------------------------

The Intake docs list a bunch of `potential use cases
<https://intake.readthedocs.io/en/latest/use_cases.html>`__. Here are some
features that we’re excited to take advantage of:

Rich Metadata
~~~~~~~~~~~~~

The Intake catalog provides a human and machine readable container for metadata
describing the underlying data, so that you can understand what the data
contains before downloading all of it. We intend to automate the production of
the catalog using PUDL’s metadata models so it’s always up to date.

Local data caching
~~~~~~~~~~~~~~~~~~

Rather than downloading the same data repeatedly, in many cases it’s possible to
transparently cache the data locally for faster access later. This is especially
useful when you’ve got plenty of disk space and a slower network connection, or
typically only work with a small subset of a much larger dataset.

Manage data like software
~~~~~~~~~~~~~~~~~~~~~~~~~

Intake data catalogs can be packaged and versioned just like Python software
packages, allowing us to manage depedencies between different versions of
software and the data it operates on to ensure they are compatible. It also
allows you to have multiple versions of the same data installed locally, and to
switch between them seamlessly when you change software environments. This is
especially useful when doing a mix of development and analysis, where we need to
work with the newest data (which may not yet be fully integrated) as well as
previously released data and software that’s more stable.

A Uniform API
~~~~~~~~~~~~~

All the data sources of a given type (parquet, SQL) would have the same
interface, reducing the number of things a user needs to remember to access the
data.

Decoupling Data Location and Format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Having users access the data through the catalog rather than directly means that
the underlying storage location and file formats can change over time as needed
without requiring the user to change how they are accessing the data.

Additional Intake Resources
---------------------------

*  `Intake Repo <https://github.com/intake/intake>`__
*  `Intake Docs <https://intake.readthedocs.io/en/latest/start.html>`__
*  `Intake Examples <https://github.com/intake/intake-examples>`__
*  `Intake talk from AnacondaCon
   2019 <https://www.youtube.com/watch?v=oyZJrROQzUs>`__
*  `Intake Parquet Repo <https://github.com/intake/intake-parquet>`__
*  `Intake Parquet
   Docs <https://intake-parquet.readthedocs.io/en/latest/quickstart.html>`__
*  `Intake SQL Repo <https://github.com/intake/intake-sql>`__
*  `Intake SQL Docs <https://intake-sql.readthedocs.io/en/latest/>`__
*  `PUDL intake
   issues <https://github.com/catalyst-cooperative/pudl/issues?q=is%3Aissue+is%3Aopen+label%3Aintake>`__

Other Related Energy & Climate Data Catalogs
--------------------------------------------

`CarbonPlan <https://github.com/carbonplan/data>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CarbonPlan is a non-profit research organization focused on climate and energy
system data analysis. They manage their data inputs and products using Intake,
and the catalogs are public.

`Pangeo Forge <https://pangeo-forge.readthedocs.io/en/latest/>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pangeo Forge is a collaborate project providing analysis read cloud optimzed
(ARCO) scientific datasets, primarily related to the earth sciences, including
climate data. The motiviation and benefits of this approach are described in
this paper: `Pangeo Forge: Crowdsourcing Analysis-Ready, Cloud Optimized Data
Production <https://doi.org/10.3389/fclim.2021.782909>`__

Licensing
---------

Our code, data, and other work are permissively licensed for use by anybody, for
any purpose, so long as you give us credit for the work we've done.

* For software we use `the MIT License <https://opensource.org/licenses/MIT>`__.
* For data, documentation, and other non-software works we use the
  `CC-BY-4.0 <https://creativecommons.org/licenses/by/4.0/>`__ license.

Contact Us
----------

* For general support, questions, or other conversations around the project
  that might be of interest to others, check out the
  `GitHub Discussions <https://github.com/catalyst-cooperative/pudl/discussions>`__
* If you'd like to get occasional updates about our projects
  `sign up for our email list <https://catalyst.coop/updates/>`__.
* Want to schedule a time to chat with us one-on-one? Join us for
  `Office Hours <https://calend.ly/catalyst-cooperative/pudl-office-hours>`__
* Follow us on Twitter: `@CatalystCoop <https://twitter.com/CatalystCoop>`__
* More info on our website: https://catalyst.coop
* For private communication about the project or to hire us to provide customized data
  extraction and analysis, you can email the maintainers:
  `pudl@catalyst.coop <mailto:pudl@catalyst.coop>`__

About Catalyst Cooperative
--------------------------

`Catalyst Cooperative <https://catalyst.coop>`__ is a small group of data
wranglers and policy wonks organized as a worker-owned cooperative consultancy.
Our goal is a more just, livable, and sustainable world. We integrate public
data and perform custom analyses to inform public policy (`Hire us!
<https://catalyst.coop/hire-catalyst>`__). Our focus is primarily on mitigating
climate change and improving electric utility regulation in the United States.

Funding
-------

This work is supported by a generous grant from the `Alfred P. Sloan Foundation
<https://sloan.org/>`__ and their `Energy & Environment Program
<https://sloan.org/programs/research/energy-and-environment>`__
