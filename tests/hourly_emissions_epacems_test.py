"""Test cases for the EPA CEMS data source."""

import pytest

from pudl_catalog.hourly_emissions_epacems import TestEpaCemsParquet

TEST_YEARS = [2020]
TEST_STATES = ["ID"]


@pytest.fixture(scope="module")
def epacems_tester():
    """Create an EPA CEMS testing object."""
    return TestEpaCemsParquet()


def test_direct(epacems_tester):
    """Test direct access via read_parquet()."""
    epacems_tester.test_direct(years=TEST_YEARS, states=TEST_STATES)


def test_intake(epacems_tester):
    """Test direct access via read_parquet()."""
    epacems_tester.test_intake(years=TEST_YEARS, states=TEST_STATES)
