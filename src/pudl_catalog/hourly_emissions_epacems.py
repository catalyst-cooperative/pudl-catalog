"""Test cases for the EPA CEMS data source."""
import logging
import os
from dataclasses import dataclass

import pandas as pd
from intake import open_catalog

from pudl_catalog.helpers import year_state_filter

logger = logging.getLogger(__name__)


@dataclass
class TestEpaCemsParquet(object):
    """Test the EPA CEMS Intake Catalog."""

    table_name: str = "hourly_emissions_epacems"
    gcs_base: str = "gcs://catalyst.coop/intake/test"
    https_base: str = "https://storage.googleapis.com/catalyst.coop/intake/test"
    local_base: str = os.getcwd() + "/"
    pudl_catalog_yml: str = "../src/catalog/pudl-catalog.yml"

    def __post_init__(self):
        """Make it easier to access paths by protocol."""
        self.base_paths = {
            "gcs": self.gcs_base,
            "https": self.https_base,
            "local": self.local_base,
        }

    def urlpath(self, protocol: str, partition=False):
        """Return full urlpath based on protocol and partitioning."""
        if partition:
            assert protocol != "https"

        urlpath = self.base_paths[protocol] + "/" + self.table_name
        if not partition:
            urlpath += ".parquet"
        return urlpath

    def direct(self, protocol, partition, years, states):
        """Read EPA CEMS data directly using read_parquet()."""
        filters = year_state_filter(years=years, states=states)
        start_time = time.time()
        urlpath = self.urlpath(protocol=protocol, partition=partition)
        logger.info(f"read_parquet, {protocol=}, {partition=}, {years=}, {states=}:")
        df = pd.read_parquet(urlpath, filters=filters)
        elapsed_time = time.time() - start_time
        logger.info(f"    elapsed time: {elapsed_time:.2f}s")
        return df

    def intake(self, protocol, partition, years, states):
        """Read EPA CEMS data from Parquet using Intake."""
        filters = year_state_filter(years=years, states=states)
        os.environ["PUDL_INTAKE_PATH"] = self.base_paths[protocol]
        pudl_cat = open_catalog(self.pudl_catalog_yml)
        if partition:
            src = pudl_cat["hourly_emissions_epacems_partitioned"](filters=filters)
        else:
            src = pudl_cat["hourly_emissions_epacems"](filters=filters)
        start_time = time.time()
        logger.info(f"intake, {protocol=}, {partition=}, {years=}, {states=}:")
        df = src.to_dask().compute()
        elapsed_time = time.time() - start_time
        logger.info(f"    elapsed time: {elapsed_time:.2f}s")
        return df

    def test_direct(self, years, states, expected_df):
        """Test direct access using different protocols and partitions."""
        expected_df = self.direct(
            protocol="local", partition=False, years=years, states=states
        )
        direct_kwargs = [
            dict(protocol="local", partition=True),
            dict(protocol="gcs", partition=False),
            dict(protocol="gcs", partition=True),
            # Tries to download the entire 4.7GB file and runs out of memory
            # dict(protocol="https", partition=False),
            # https *must* refer to individual files. Can't list a directory or match patterns.
            # dict(protocol="https", partition=True),
        ]
        for kwargs in direct_kwargs:
            kwargs.update(dict(years=years, states=states))
            test_df = self.direct(**kwargs)
            pd.testing.assert_frame_equal(expected_df, test_df)

    def test_intake(self, years, states):
        """Test Intake catalog access using different protocols and partitions."""
        expected_df = self.direct(
            protocol="local", partition=False, years=years, states=states
        )
        intake_kwargs = [
            dict(protocol="local", partition=False),
            dict(protocol="local", partition=True),
            dict(protocol="gcs", partition=False),
            dict(protocol="gcs", partition=True),
            # Tries to download the entire 4.7GB file and runs out of memory
            # dict(protocol="https", partition=False),
            # Results in a 403 Forbidden error on parquet file parent directory
            # dict(protocol="https", partition=True),
        ]
        for kwargs in intake_kwargs:
            kwargs.update(dict(years=years, states=states))
            test_df = self.intake(**kwargs)
            logger.info("Verifying that dataframe matches expected output.")
            pd.testing.assert_frame_equal(expected_df, test_df)
