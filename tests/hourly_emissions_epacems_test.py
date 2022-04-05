"""Test cases for the EPA CEMS data source."""

from pudl_catalog.hourly_emissions_epacems import TestEpaCemsParquet

EPACEMS = TestEpaCemsParquet()
TEST_YEARS = [2020]
TEST_STATES = ["ID"]


def test_direct():
    """Test direct access via read_parquet()."""
    EPACEMS.test_direct(years=TEST_YEARS, states=TEST_STATES)
