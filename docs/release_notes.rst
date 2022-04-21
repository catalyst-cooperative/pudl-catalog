=======================================================================================
PUDL Data Catalog Release Notes
=======================================================================================

.. _release-v0-1-0:

---------------------------------------------------------------------------------------
0.1.0 (2022-04-21)
---------------------------------------------------------------------------------------

First Release
^^^^^^^^^^^^^
* We're excited to start providing bulk, versioned, programmatic access to the PUDL
  data, starting with the EPA CEMS hourly emissions data. This is still experimental.
* The data is available in a Google cloud object store, via an Intake data catalog, and
  is stored in Apache Parquet files.
* We're still working out some performance and metadata issues, but it's at least
  nominally functional, and we wanted to get it out early and see if we could get some
  feedback.
* Currently there's a single-file and a partitioned version of the same data. We
  recommend using the single-file version (the source named ``hourly_emissions_epacems``
  in the catalog) since performance is generally better and we need to work on making
  per-file local caching more efficient before its worth using the partitioned data.
* Thanks to :user:`martindurant` for helping us get things set up and helping us debug
  some issues.

Known Issues
^^^^^^^^^^^^
* Local caching of the Parquet files works, but with both the monolithic and partitioned
  versions of the data will typically cache the entire dataset immediately upon first
  access. This is because the metadata describing what data is in which file is only
  available within the Parquet files themseles, so every files has to be accessed in
  order to filter the entire dataset. Since the data is several GB, it can take a while
  to cache initially. Subsequent access is fast. See :issue:`4`
* Accessing the year-state partitioned version of the data is much slower than the
  monolithic single file version. We don't really understand why. For now it's
  recommended to use the monolithic EPA CEMS data. See :issue:`8`
