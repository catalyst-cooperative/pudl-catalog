"""Verify that expected catalog files are available in Google Cloud Storage."""
import logging

import pytest
from google.cloud import storage

from pudl_catalog import CATALOG_VERSION, INTAKE_BUCKET

logger = logging.getLogger(__name__)

# For Requester Pays billing
BILLING_PROJECT = "catalyst-cooperative-pudl"


@pytest.mark.parametrize(
    "filename",
    [
        "censusdp1tract.sqlite",
        "ferc1.sqlite",
        "pudl.sqlite",
        "hourly_emissions_epacems.parquet",
        "hourly_emissions_epacems/epacems-2020-NY.parquet",
        "hourly_emissions_epacems/epacems-2020-CA.parquet",
        "hourly_emissions_epacems/epacems-2020-TX.parquet",
        "hourly_emissions_epacems/epacems-2020-FL.parquet",
    ],
)
def test_file_exists(filename: str) -> None:
    """Test that files expected in the catalog are available in GCS."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(INTAKE_BUCKET, user_project=BILLING_PROJECT)
    fullname = CATALOG_VERSION + "/" + filename
    blob = storage.blob.Blob(name=fullname, bucket=bucket)
    assert blob.exists()
