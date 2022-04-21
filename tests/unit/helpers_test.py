"""Unit tests for the pudl_catalog.helpers module."""
import logging

import pytest

from pudl_catalog.helpers import year_state_filter

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "years,states,expected_filter",
    [
        ([2020], ["ID"], [[("year", "=", 2020), ("state", "=", "ID")]]),
        (None, ["ID"], [[("state", "=", "ID")]]),
        ([2020], None, [[("year", "=", 2020)]]),
        (None, None, None),
    ],
)
def test_year_state_filter(years, states, expected_filter):
    """Test the generation of DNF pushdown filters for Parquet files."""
    assert year_state_filter(years=years, states=states) == expected_filter
