"""Verify that expected catalog files are available in Google Cloud Storage."""
import logging

import boto3
import pytest
from botocore import UNSIGNED
from botocore.config import Config
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
def test_gcs_file_exists(filename: str) -> None:
    """Test that files expected in the catalog are available in GCS."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(INTAKE_BUCKET, user_project=BILLING_PROJECT)
    fullname = CATALOG_VERSION + "/" + filename
    blob = storage.blob.Blob(name=fullname, bucket=bucket)
    assert blob.exists()


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
def test_s3_file_exists(filename: str) -> None:
    """Test that files expected in the catalog are available in s3."""
    # Disable signing so we don't need to load credentials.
    # From https://github.com/boto/boto3/issues/1200#issuecomment-319141394
    # Have to request all of the files because we get an authentication
    # error when using Client().get_object_attributes().
    s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))

    paginator = s3.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(Bucket=INTAKE_BUCKET)
    files = []
    for page in page_iterator:
        files += page["Contents"]

    filenames = [file["Key"] for file in files]
    fullname = CATALOG_VERSION + "/" + filename

    assert (
        fullname in filenames
    ), f"{fullname} is not in the {INTAKE_BUCKET}/{CATALOG_VERSION} bucket."
