"""Verify that expected catalog files are available in Google Cloud Storage."""
import logging
from contextlib import contextmanager

import intake
import pytest

logger = logging.getLogger(__name__)


@contextmanager
def does_not_raise():
    """No-op to allow non-raising parametrization."""
    yield


@pytest.mark.parametrize(
    "required_field,expectation",
    [
        ("title", does_not_raise()),
        ("license", does_not_raise()),
        ("provider", does_not_raise()),
        ("path", does_not_raise()),
        ("wtf", pytest.raises(ValueError)),
    ],
)
def test_catalog_metadata(required_field: str, expectation) -> None:
    """
    Test that all catalog entries have required metadata fields.

    It would be better to parametrize this both by catalog entry and by metadata field,
    and to automate that parametrization so that any time new data is added to the
    catalog it happens without intervention. The CarbonPlan catalog does some magic
    like this. See:

    https://github.com/carbonplan/data/blob/main/carbonplan_data/tests/__init__.py
    """
    pudl_cat = intake.cat["pudl_cat"]

    with expectation:
        for entry in pudl_cat:
            if not pudl_cat[entry].metadata.get(required_field, False):
                raise ValueError(
                    f"Required metadata field {required_field} missing from {entry}."
                )
