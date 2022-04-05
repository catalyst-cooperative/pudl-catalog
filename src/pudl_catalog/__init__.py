import os
import warnings
from pathlib import Path

import intake

import helpers

KNOWN_DATA_LOCATIONS = [
    "https://storage.googleapis.com/catalyst.coop/intake/test",
    "gcs://catalyst.coop/intake/test",
]

# Ensure that the user has set the relevant environment variables
if os.getenv("PUDL_INTAKE_PATH") is None:
    msg = (
        f"Environment variable PUDL_INTAKE_PATH not set, `catalystcoop.pudl_catalog` may not work as expected."
        f"Known data locations include: {KNOWN_DATA_LOCATIONS}."
    )
        warnings.warn(msg)

if os.getenv("PUDL_INTAKE_CACHE") is None:
    msg = (
        f"Environment variable PUDL_INTAKE_CACHE not set, `catalystcoop.pudl_catalog` may not work as expected."
        f"Choose a location for local file caching to speed repeated data queries."
    )
        warnings.warn(msg)

# The catalog is a YAML file in the same directory as this init file
pudl_catalog_path = Path(__file__).parent.resolve() / "pudl_catalog.yaml"
# After installation the catalog intake.cat.pudl_cat should be available
pudl_cat = intake.open_catalog(pudl_catalog_path)
# The data source intake.cat.hourly_emissions_epacems should also be available.
hourly_emissions_epacems = cat.hourly_emissions_epacems()

