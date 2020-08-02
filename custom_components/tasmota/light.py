from homeassistant.const import CONF_DEVICE_ID
from homeassistant.core import callsback
from homeassistant.components.light import LightEntity, PLATFORM_SCHEMA
from homeassistant.components.mqtt import (
    async_subscribe,
    async_subscribe_topics,
    async_publish
)
import homeassistant.helpers.config_validation as cv

import voluptuous as vol

import json

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DEVICE_ID): cv.string
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    topic = config[CONF_DEVICE_ID]

    # TODO: Validate the topic, and maybe test that a device is listening
    # TODO: Actually, I should set up subscriptions at the platform level

    add_entities([TasmotaLight(hass, topic)])

class TasmotaLight(LightEntity):
    def __init__(self, hass, topic):
        self._hass: HomeAssistant = hass
        self._topic = topic
        self._name = 'Tasmota {}'.format(topic)
        self._state = None
        self._sub_state = None
        
    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        await self._subscribe_topics()
    
    async def _subscribe_topics(self):
        self._sub_state = async_subscribe_topics(hass, self._sub_state, {
            "state_topic": {
                "topic": 'stat/{}/result',
                "msg_callback": self.result_recieved
            }
        })

    @callback
    def result_recieved(self, topic, payload, qos):
        try:
            values = json.loads(payload)
            if 'POWER' in values:
                self._state = 'ON' == values['POWER']
                await self.async_schedule_update_ha_state()

    @property
    def name(self):
        return self._name
    
    @property
    def is_on(self):
        return self._state

    async def async_turn_on(self, **kwargs):
        await async_publish(self._hass, 'cmnd/{}/Power'.format(self._topic), 'ON')

    async def async_turn_off(self, **kwargs):
        await async_publish(self._hass, 'cmnd/{}/Power'.format(self._topic), 'OFF')
    
    async def async_update(self):
        await async_publish(self._hass, 'cmnd/{}/state'.format(self._topic))

