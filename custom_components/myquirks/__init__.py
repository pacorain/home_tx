from .myquirks.alertme_smart_plug import AlertMeSmartPlug
from .myquirks.haloWx import HaloWx

import logging
logger = logging.getLogger(__name__)

from datetime import timedelta
from homeassistant.components import apcupsd

apcupsd.MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=3)
logger.info("Updated APC to allow updates after 3 seconds")

DOMAIN = "myquirks"

def setup(hass, config):
    # No setup needed, we just need to import the quirks
    logger.info("myquirks loaded!")

    return True
