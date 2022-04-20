"""Test cases for the EPA CEMS data source."""
import logging
import os
import time
from dataclasses import dataclass
from pathlib import Path

import intake
import pandas as pd

from pudl_catalog import BASE_URLS
from pudl_catalog.helpers import year_state_filter

logger = logging.getLogger(__name__)


@dataclass
class TestEpaCemsParquet(object):
    """Test the EPA CEMS Intake Catalog."""

    table_name: str = "hourly_emissions_epacems"
    gs_base: str = BASE_URLS["gs"]
    https_base: str = BASE_URLS["https"]
    local_base: str = str(Path(__file__).parent.parent.parent / "data")
    pudl_catalog_yml: str = "../src/catalog/pudl-catalog.yml"

    def __post_init__(self):
        """Make it easier to access paths by protocol."""
        self.base_paths = {
            "gs": self.gs_base,
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
        if protocol == "local":
            pudl_cat = intake.cat.pudl_cat(cache_method="")
        else:
            pudl_cat = intake.cat.pudl_cat
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

    def test_direct(self, years, states, verify_df=True):
        """Test direct access using different protocols and partitions."""
        expected_df = self.direct(
            protocol="local", partition=False, years=years, states=states
        )
        direct_kwargs = [
            dict(protocol="local", partition=True),
            dict(protocol="gs", partition=False),
            dict(protocol="gs", partition=True),
            # Tries to download the entire 4.7GB file and runs out of memory
            # dict(protocol="https", partition=False),
            # https *must* refer to individual files. Can't list a directory or match patterns.
            # dict(protocol="https", partition=True),
        ]
        for kwargs in direct_kwargs:
            kwargs.update(dict(years=years, states=states))
            test_df = self.direct(**kwargs)
            if verify_df:
                logger.info("    verifying that dataframe matches expected output.")
                pd.testing.assert_frame_equal(expected_df, test_df)

    def test_intake(self, years, states, verify_df=True):
        """Test Intake catalog access using different protocols and partitions."""
        expected_df = self.direct(
            protocol="local", partition=False, years=years, states=states
        )
        intake_kwargs = [
            dict(protocol="local", partition=False),
            dict(protocol="local", partition=True),
            dict(protocol="gs", partition=False),
            dict(protocol="gs", partition=True),
            # Tries to download the entire 4.7GB file and runs out of memory
            # dict(protocol="https", partition=False),
            # Results in a 403 Forbidden error on parquet file parent directory
            # dict(protocol="https", partition=True),
        ]
        for kwargs in intake_kwargs:
            kwargs.update(dict(years=years, states=states))
            test_df = self.intake(**kwargs)
            if verify_df:
                logger.info("    verifying that dataframe matches expected output.")
                pd.testing.assert_frame_equal(expected_df, test_df)
