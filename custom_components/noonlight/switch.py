"""Create a switch to trigger an alarm in Noonlight."""
import logging

from datetime import timedelta

from noonlight import NoonlightClient

from homeassistant.components import persistent_notification
from homeassistant.components.switch import SwitchDevice
from homeassistant.helpers.event import async_track_time_interval

from . import (DOMAIN, EVENT_NOONLIGHT_TOKEN_REFRESHED,
               NOTIFICATION_ALARM_CREATE_FAILURE)

DEFAULT_NAME = 'Noonlight Switch'

CONST_ALARM_STATUS_ACTIVE = 'ACTIVE'
CONST_ALARM_STATUS_CANCELED = 'CANCELED'

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
        hass, config, async_add_entities, discovery_info=None):
    """Create a switch to create an alarm with the Noonlight service."""
    noonlight_integration = hass.data[DOMAIN]
    noonlight_switch = NoonlightSwitch(noonlight_integration)
    async_add_entities([noonlight_switch])

    def noonlight_token_refreshed():
        noonlight_switch.schedule_update_ha_state()

    hass.helpers.dispatcher.async_dispatcher_connect(
        EVENT_NOONLIGHT_TOKEN_REFRESHED, noonlight_token_refreshed)


class NoonlightSwitch(SwitchDevice):
    """Representation of a Noonlight alarm switch."""

    def __init__(self, noonlight_integration):
        """Initialize the Noonlight switch."""
        self.noonlight = noonlight_integration
        self._name = DEFAULT_NAME
        self._alarm = None
        self._state = False

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def available(self):
        """Ensure that the Noonlight access token is valid."""
        return self.noonlight.access_token_expires_in.total_seconds() > 0

    @property
    def is_on(self):
        """Return the status of the switch."""
        return self._state

    async def update_alarm_status(self):
        """Update the status of the current alarm."""
        if self._alarm is not None:
            return await self._alarm.get_status()

    async def async_turn_on(self, **kwargs):
        """Activate an alarm."""
        # [TODO] read list of monitored sensors, use sensor type to determine
        #   whether medical, fire, or police should be notified
        if self._alarm is None:
            try:
                self._alarm = await self.noonlight.client.create_alarm(
                    body={
                        'location.coordinates': {
                            'lat': self.noonlight.latitude,
                            'lng': self.noonlight.longitude,
                            'accuracy': 5
                        }
                    }
                )
            except NoonlightClient.ClientError as client_error:
                persistent_notification.create(
                    self.hass,
                    "Failed to send an alarm to Noonlight!\n\n"
                    "({}: {})".format(type(client_error).__name__,
                                      str(client_error)),
                    "Noonlight Alarm Failure",
                    NOTIFICATION_ALARM_CREATE_FAILURE)
            if self._alarm and self._alarm.status == CONST_ALARM_STATUS_ACTIVE:
                _LOGGER.debug(
                    'noonlight alarm has been initiated. '
                    'id: %s status: %s',
                    self._alarm.id,
                    self._alarm.status)
                self._state = True
                cancel_interval = None

                async def check_alarm_status_interval(now):
                    _LOGGER.debug('checking alarm status...')
                    if await self.update_alarm_status() == \
                            CONST_ALARM_STATUS_CANCELED:
                        _LOGGER.debug(
                            'alarm %s has been canceled!',
                            self._alarm.id)
                        if cancel_interval is not None:
                            cancel_interval()
                        await self.async_turn_off()
                        self.schedule_update_ha_state()
                cancel_interval = async_track_time_interval(
                    self.hass,
                    check_alarm_status_interval,
                    timedelta(seconds=15)
                    )

    async def async_turn_off(self, **kwargs):
        """Turn off the switch if the active alarm is canceled."""
        if self._alarm is not None:
            if self._alarm.status == CONST_ALARM_STATUS_CANCELED:
                self._alarm = None
        if self._alarm is None:
            self._state = False
