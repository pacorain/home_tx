from .myquirks.alertme_smart_plug import AlertMeSmartPlug
from .myquirks.haloWx import HaloWx

import logging
logger = logging.getLogger(__name__)

DOMAIN = "myquirks"

def setup(hass, config):
    # No setup needed, we just need to import the quirks
    logger.info("myquirks loaded!")

    return True