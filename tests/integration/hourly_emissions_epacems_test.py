"""Test cases for the EPA CEMS data source."""
import logging
import os
import time
from typing import Literal

import intake
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from pudl_catalog import BASE_URLS
from pudl_catalog.helpers import year_state_filter

logger = logging.getLogger(__name__)

TEST_YEARS = [2020]
TEST_STATES = ["ID"]
TEST_FILTERS = year_state_filter(years=TEST_YEARS, states=TEST_STATES)

os.environ["PUDL_INTAKE_PATH"] = BASE_URLS["gs"]


def parquet_url(
    protocol: Literal["gs", "https"],
    partition: bool,
    table_name: str,
) -> str:
    """Construct the path to a particular parquet table resource."""
    try:
        url = BASE_URLS[protocol]
    except KeyError:
        raise ValueError(
            f"Received invalid protocol: {protocol}. Must be one of 'gs' or 'https'."
        )
    url = url + "/" + table_name
    if not partition:
        url += ".parquet"
    return url


@pytest.fixture(scope="module")
def expected_df() -> pd.DataFrame:
    """Read parquet data directly for comparison with Intake outputs."""
    logger.info("Reading remote test data for comparison using pd.read_parquet().")
    epacems_url = parquet_url(
        protocol="gs",
        partition=False,
        table_name="hourly_emissions_epacems",
    )
    return pd.read_parquet(epacems_url, filters=TEST_FILTERS)


@pytest.mark.parametrize(
    "protocol,partition",
    [
        ("gs", False),
        ("gs", True),
    ],
)
def test_read_parquet(
    protocol: Literal["gs", "https"],
    partition: bool,
    expected_df: pd.DataFrame,
) -> None:
    """Test direct access via read_parquet()."""
    logger.info(
        f"read_parquet, {protocol=}, {partition=}, {TEST_YEARS=}, {TEST_STATES=}:"
    )
    epacems_url = parquet_url(
        protocol=protocol, partition=partition, table_name="hourly_emissions_epacems"
    )
    start_time = time.time()
    df = pd.read_parquet(epacems_url, filters=TEST_FILTERS)
    elapsed_time = time.time() - start_time
    logger.info(f"    elapsed time: {elapsed_time:.2f}s")
    assert_frame_equal(df, expected_df)


@pytest.mark.parametrize(
    "protocol,partition",
    [
        ("gs", False),
        ("gs", True),
    ],
)
def test_intake_catalog(
    protocol: Literal["gs", "https"],
    partition: bool,
    expected_df: pd.DataFrame,
) -> None:
    """Test reading data from the intake catalog."""
    logger.info(
        f"intake_catalog, {protocol=}, {partition=}, {TEST_YEARS=}, {TEST_STATES=}:"
    )
    os.environ["PUDL_INTAKE_PATH"] = BASE_URLS[protocol]
    pudl_cat = intake.cat.pudl_cat
    src = "hourly_emissions_epacems"
    if partition:
        src += "_partitioned"
    start_time = time.time()
    df = pudl_cat[src](filters=TEST_FILTERS, cache_method="").to_dask().compute()
    elapsed_time = time.time() - start_time
    logger.info(f"    elapsed time: {elapsed_time:.2f}s")
    assert_frame_equal(df, expected_df)
