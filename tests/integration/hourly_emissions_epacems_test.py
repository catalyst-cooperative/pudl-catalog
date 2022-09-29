"""Test cases for the EPA CEMS data source."""
import logging
import os
import time
from typing import Literal, Optional

import dask.dataframe as dd
import intake
import pandas as pd
import pytest
from dask.dataframe.utils import check_matching_columns, is_dataframe_like

from pudl_catalog import BASE_URLS
from pudl_catalog.helpers import year_state_filter

logger = logging.getLogger(__name__)

TEST_YEARS = [2020]
TEST_STATES = ["ID"]
TEST_FILTERS = year_state_filter(years=TEST_YEARS, states=TEST_STATES)


logger = logging.getLogger(__name__)

os.environ["PUDL_INTAKE_PATH"] = BASE_URLS["gs"]


def parquet_url(
    protocol: Literal["gs", "https"],
    table_name: str,
    partition_suffix: Optional[str] = None,
) -> str:
    """Construct the path to a particular parquet table resource."""
    try:
        url = BASE_URLS[protocol]
    except KeyError:
        raise ValueError(
            f"Received invalid protocol: {protocol}. Must be one of 'gs' or 'https'."
        )
    url = url + "/" + table_name
    if partition_suffix is None:
        url += ".parquet"
    return url


@pytest.fixture(scope="module")
def expected_df() -> pd.DataFrame:
    """Read parquet data directly for comparison with Intake outputs."""
    logger.debug("Reading remote test data for comparison using pd.read_parquet().")
    epacems_url = parquet_url(
        protocol="gs",
        table_name="hourly_emissions_epacems",
        partition_suffix=None,
    )
    expected_df = pd.read_parquet(
        epacems_url,
        filters=TEST_FILTERS,
        storage_options={"requester_pays": True},
    )
    is_dataframe_like(expected_df)
    assert expected_df.shape == (70_272, 19)
    return expected_df


@pytest.mark.parametrize(
    "protocol,partition_suffix",
    [
        ("gs", None),
        ("gs", "_partitioned"),
    ],
)
def test_read_parquet(
    protocol: Literal["gs", "https"],
    partition_suffix: str,
    expected_df: pd.DataFrame,
) -> None:
    """Test direct access via read_parquet()."""
    logger.debug(f"read_parquet, {protocol=}, {partition_suffix=}")
    epacems_url = parquet_url(
        protocol=protocol,
        table_name="hourly_emissions_epacems",
        partition_suffix=partition_suffix,
    )
    start_time = time.time()
    actual_dd = dd.read_parquet(epacems_url, storage_options={"requester_pays": True})
    elapsed_time = time.time() - start_time
    logger.debug(f"    elapsed time: {elapsed_time:.2f}s")
    is_dataframe_like(actual_dd)
    check_matching_columns(actual_dd, expected_df)


@pytest.mark.parametrize(
    "protocol,partition_suffix",
    [
        ("gs", None),
        ("gs", "_partitioned"),
    ],
)
def test_intake_catalog(
    protocol: Literal["gs", "https"],
    partition_suffix: str,
    expected_df: pd.DataFrame,
) -> None:
    """Test reading data from the intake catalog."""
    logger.debug(f"intake_catalog, {protocol=}, {partition_suffix=}")
    os.environ["PUDL_INTAKE_PATH"] = BASE_URLS[protocol]
    pudl_cat = intake.cat.pudl_cat
    src = "hourly_emissions_epacems"
    if partition_suffix is not None:
        src += partition_suffix
    start_time = time.time()
    actual_dd = pudl_cat[src](cache_method="").to_dask()
    elapsed_time = time.time() - start_time
    logger.debug(f"    elapsed time: {elapsed_time:.2f}s")
    is_dataframe_like(actual_dd)
    check_matching_columns(actual_dd, expected_df)
