"""An installable catalog of open data related to the US energy system."""
import logging
import os
import warnings
from pathlib import Path

import intake
import pkg_resources

import pudl_catalog.helpers  # noqa: F401

BASE_URLS = {
    "gs": "gs://intake.catalyst.coop/test",
    "https": "https://storage.googleapis.com/intake.catalyst.coop/test",
}

# Ensure that the user has set the relevant environment variables
if os.getenv("PUDL_INTAKE_PATH") is None:
    msg = (
        "Environment variable PUDL_INTAKE_PATH is not set. Without that path \n"
        "`catalystcoop.pudl_catalog` will not work as expected.\n"
        f"Known data locations include: {list(BASE_URLS.values())}.\n"
        f"Defaulting to {BASE_URLS['gs']}"
    )
    warnings.warn(msg)

if os.getenv("PUDL_INTAKE_CACHE") is None:
    msg = (
        "Environment variable PUDL_INTAKE_CACHE not set, `catalystcoop.pudl_catalog`\n"
        "may not work as expected. Set a location for local file caching to speed\n"
        "repeated data queries."
    )
    warnings.warn(msg)

# The catalog is a YAML file in the same directory as this init file
_pudl_catalog_path = Path(__file__).parent.resolve() / "pudl_catalog.yaml"
# After installation the catalog intake.cat.pudl_cat should be available
pudl_cat = intake.open_catalog(_pudl_catalog_path)

__author__ = "Catalyst Cooperative"
__contact__ = "pudl@catalyst.coop"
__license__ = "MIT License"
__maintainer__ = "Zane Selvans"
__maintainer_email__ = "zane.selvans@catalyst.coop"
__version__ = pkg_resources.get_distribution("catalystcoop.pudl_catalog").version
__docformat__ = "restructuredtext en"
__description__ = "An catalog of open data related to the US energy system."
__projecturl__ = "https://github.com/catalyst-cooperative/pudl-catalog"
__downloadurl__ = "https://github.com/catalyst-cooperative/pudl-catalog"

logging.getLogger(__name__).addHandler(logging.NullHandler())
