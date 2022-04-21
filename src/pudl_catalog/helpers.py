"""Helper functions for working with the PUDL Data Catalog."""
from itertools import product
from typing import Iterable, List, Tuple, Union


def year_state_filter(
    years: Iterable[int] = None, states: Iterable[str] = None
) -> List[List[Tuple[Union[str, int]]]]:
    """
    Create filters to read given years and states from partitioned parquet dataset.

    A subset of an Apache Parquet dataset can be read in more efficiently if files
    which don't need to be queried are avoideed. Some datasets are partitioned based
    on the values of columns to make this easier. The EPA CEMS dataset which we
    publish is partitioned by state and report year.

    However, the way the filters are specified can be unintuitive. They use DNF
    (disjunctive normal form) See this blog post for more details:

    https://blog.datasyndrome.com/python-and-parquet-performance-e71da65269ce

    This function takes a set of years, and a set of states, and returns a list of lists
    of tuples, appropriate for use with the read_parquet() methods of pandas and dask
    dataframes. The filter will include all combinations of the specified years and
    states. E.g. if years=(2018, 2019) and states=("CA", "CO") then the filter would
    result in getting 2018 and 2019 data for CO, as well as 2018 and 2019 data for CA.

    Args:
        years: 4-digit integers indicating the years of data you would like
            to read. By default it includes all available years.
        states: 2-letter state abbreviations indicating what states you would
            like to include. By default it includes all available states.

    Returns:
        A list of lists of tuples, suitable for use as a filter in the
        read_parquet() method of pandas and dask dataframes.

    """
    if years is not None:
        year_filters = [("year", "=", year) for year in years]
    if states is not None:
        state_filters = [("state", "=", state.upper()) for state in states]

    if states and not years:
        filters = [
            [
                tuple(x),
            ]
            for x in state_filters
        ]
    elif years and not states:
        filters = [
            [
                tuple(x),
            ]
            for x in year_filters
        ]
    elif years and states:
        filters = [list(x) for x in product(year_filters, state_filters)]
    else:
        filters = None

    return filters
