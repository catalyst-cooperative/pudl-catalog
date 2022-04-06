"""An installable catalog of open data related to the US energy system."""
import os
import warnings
from pathlib import Path

import intake

import pudl_catalog.helpers

KNOWN_DATA_LOCATIONS = [
    "https://storage.googleapis.com/catalyst.coop/intake/test",
    "gcs://catalyst.coop/intake/test",
]

# Ensure that the user has set the relevant environment variables
if os.getenv("PUDL_INTAKE_PATH") is None:
    msg = (
        "Environment variable PUDL_INTAKE_PATH not set, `catalystcoop.pudl_catalog`\n"
        "may not work as expected. Known data locations include:\n"
        "{KNOWN_DATA_LOCATIONS}."
    )
    warnings.warn(msg)

if os.getenv("PUDL_INTAKE_CACHE") is None:
    msg = (
        f"Environment variable PUDL_INTAKE_CACHE not set, `catalystcoop.pudl_catalog`\n"
        "may not work as expected. Choose a location for local file caching to speed\n"
        "repeated data queries."
    )
    warnings.warn(msg)

# The catalog is a YAML file in the same directory as this init file
_pudl_catalog_path = Path(__file__).parent.resolve() / "pudl_catalog.yaml"
# After installation the catalog intake.cat.pudl_cat should be available
pudl_cat = intake.open_catalog(_pudl_catalog_path)
