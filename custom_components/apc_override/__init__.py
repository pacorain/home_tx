from datetime import timedelta
from homeassistant.components import apcupsd

import logging
logger = logging.getLogger(__name__)

apcupsd.MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=3)
logger.log("Updated APC to allow updates after 3 seconds")