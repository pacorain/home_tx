from abc import ABC
from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant
from homeassistant.const import PERCENTAGE, TIME_MILLISECONDS
import logging
import asyncio
import aioping

_LOGGER = logging.getLogger(__name__)

DEFAULT_UPDATE_INTERVAL = 600
DEFAULT_COUNT = 20
DEFAULT_INTERVAL = 0.5
DEFAULT_TIMEOUT = 5

DOMAIN = "aioping"


def setup_platform(
    hass: HomeAssistant, config: dict, add_entities, discovery_info=None
):
    ping = Ping(config, hass)
    hass.async_create_task(ping._loop())
    name = config["name"]
    add_entities(
        [
            PacketLossEntity(name, ping),
            JitterEntity(name, ping),
            AveragePingEntity(name, ping),
            MaxPingEntity(name, ping),
            MinPingEntity(name, ping),
        ]
    )


class Ping:
    def __init__(self, config: dict, hass: HomeAssistant):
        self.data = None
        self.config = config
        self.hass = hass

    async def _loop(self):
        _LOGGER.debug("Starting ping loop")
        while self.hass.is_running and not self.hass.is_stopping:
            self.hass.async_create_task(self.do_ping())
            asyncio.sleep(self.get_config("every", DEFAULT_UPDATE_INTERVAL))

    def get_config(self, name, default=None, type=float):
        try:
            return type(self.config.get(name, default))
        except (TypeError, ValueError):
            _LOGGER.warn(
                f"Config {name} is not a valid value for sensor '{self.config['name']}'"
            )
            return default

    async def do_ping(self):
        try:
            success = 0
            fail = 0
            previous = None
            jitter = []
            _LOGGER.info(f"Starting pings for '{self.config['name']}'")
            results = await self.schedule_pings()
            for index, result in enumerate(list(results)):
                if result is None:
                    fail += 1
                    del results[index]
                else:
                    success += 1
                    if previous is not None:
                        jitter.append(abs(result - previous))
                    previous = result
            if len(results) == 0:
                _LOGGER.info(f"PING TIMEOUT for sensor {self.config['name']}")
                self.data = None
                return
            packet_loss = float(fail) / sum([success, fail])
            avg_jitter = sum(jitter) / len(jitter)
            avg_ping = sum(results) / len(results)
            max_ping = max(results)
            min_ping = min(results)
            self.data = {
                "loss": packet_loss,
                "jitter": avg_jitter,
                "avg": avg_ping,
                "max": max_ping,
                "min": min_ping,
            }
        except:
            _LOGGER.warn(
                f"UNKNOWN EXCEPTION: PING for sensor {self.config['name']} failed with unknown exception."
            )
            self.data = None

    async def schedule_pings(self):
        tasks = []
        for _ in range(self.get_config("count", DEFAULT_COUNT, int)):
            coro = self.ping(
                self.config["host"], timeout=self.get_config("timeout", DEFAULT_TIMEOUT)
            )
            task = self.hass.async_create_task(coro)
            tasks.append(task)
        return asyncio.gather(*tasks)

    @staticmethod
    async def ping(host, timeout):
        try:
            result = await aioping.ping(host, timeout)
            _LOGGER.debug(f"PING {host}: {result}")
        except TimeoutError:
            _LOGGER.debug(f"TIMEOUT from host {host}")
            return None


class PingEntity(Entity, ABC):
    entity_measures = ""
    data_value = ""
    unit = None

    def __init__(self, name: str, ping: Ping):
        self._name = name + " " + self.entity_measures
        self._ping = ping

    @property
    def name(self):
        return self._name

    @property
    def available(self):
        return bool(self._ping.data)

    @property
    def unit_of_measurement(self):
        return self.unit

    @property
    def state(self):
        if self._ping.data:
            return self._ping.data[self.data_value]
        else:
            return None


class PacketLossEntity(PingEntity):
    entity_measures = "Packet Loss"
    data_value = "loss"
    unit = PERCENTAGE

    @property
    def icon(self):
        if self.state == 0:
            return "mdi:check-network-outline"
        else:
            return "mdi:close-network-outline"


class JitterEntity(PingEntity):
    entity_measures = "Jitter"
    data_value = "jitter"
    unit = TIME_MILLISECONDS

    @property
    def icon(self):
        return "mdi:square-wave"


class MaxPingEntity(PingEntity):
    entity_measures = "Maximum Ping"
    data_value = "max"
    unit = TIME_MILLISECONDS


class AveragePingEntity(PingEntity):
    entity_measures = "Average Ping"
    data_value = "avg"
    unit = TIME_MILLISECONDS


class MinPingEntity(PingEntity):
    entity_measures = "Minimum Ping"
    data_value = "min"
    unit = TIME_MILLISECONDS
