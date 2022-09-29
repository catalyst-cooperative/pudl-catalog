"""An installable catalog of open data related to the US energy system."""
import logging
import os
from pathlib import Path

import intake
import pkg_resources

import pudl_catalog.helpers  # noqa: F401

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

INTAKE_BUCKET = "intake.catalyst.coop"
# Ideally we would set this version automatically using setuptools_scm...
CATALOG_VERSION = "v0.1.1"

BASE_URLS = {
    "gs": f"gs://{INTAKE_BUCKET}/{CATALOG_VERSION}",
    # HTTPS access doesn't really work well, so we're hiding it from users for now.
    "https": f"https://storage.googleapis.com/{INTAKE_BUCKET}/{CATALOG_VERSION}",
}

# Ensure that the user has set the relevant environment variables
if os.getenv("PUDL_INTAKE_PATH") is None:
    logger.info(
        "Environment variable PUDL_INTAKE_PATH is not set. "
        f"Defaulting to {BASE_URLS['gs']}"
    )
    os.environ["PUDL_INTAKE_PATH"] = BASE_URLS["gs"]

if os.getenv("PUDL_INTAKE_CACHE") is None:
    logger.info(
        "Environment variable PUDL_INTAKE_CACHE is not set. "
        f"Defaulting to {os.getenv('HOME')}/.intake/cache"
    )
    os.environ["PUDL_INTAKE_CACHE"] = str(Path.home() / ".intake/cache")

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
