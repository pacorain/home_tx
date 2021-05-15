from zigpy.quirks import CustomDevice, CustomCluster, CustomEndpoint
from zigpy.profiles import zha
from zigpy.zcl.clusters.general import Basic, PowerConfiguration, Identify, Ota, OnOff, LevelControl
from zigpy.zcl.clusters.measurement import TemperatureMeasurement, PressureMeasurement, RelativeHumidity
from zigpy.zcl.clusters.security import IasWd, IasZone
from zigpy.zcl.clusters.lighting import Color
import zigpy.types as t

import logging

logger = logging.getLogger(__name__)

from ..const import (
    MODELS_INFO,
    ENDPOINTS,
    PROFILE_ID,
    DEVICE_TYPE,
    INPUT_CLUSTERS,
    OUTPUT_CLUSTERS
)

ENDPOINT_BASIC = 1
ENDPOINT_LIGHT = 2
ENDPOINT_CO = 3
ENDPOINT_HALO = 4
ENDPOINT_WEATHER = 5

CLUSTER_HALO = 0xFD00
ATTR_DEVICE_STATUS = 0x0000
ATTR_ROOM = 0x0002
CMD_DEVICE_STATUS_CHANGE_NOTIFICATION = 0x00

CLUSTER_HALO_CONTROL = 0xFD01
ATTR_TEST_STATUS = 0x0000
ATTR_HUSH_STATUS = 0x0001
CMD_HALO_TEST = 0x00
CMD_HALO_HUSH = 0x01

CLUSTER_HALO_SENSORS = 0xFD02
ATTR_CO_PPM = 0x0002

CLUSTER_WEATHER = 0xFD03
ATTR_WEATHER_ALERT_STATUS = 0x0000
ATTR_WEATHER_MUTE = 0x0001
ATTR_WEATHER_LOCATION = 0x0002
ATTR_WEATHER_EVENT_1 = 0x0003
ATTR_WEATHER_EVENT_2 = 0x0004
ATTR_WEATHER_EVENT_3 = 0x0005
ATTR_WEATHER_STATION = 0x0006
ATTR_WEATHER_STATION_RSSI1 = 0x0007
ATTR_WEATHER_STATION_RSSI2 = 0x0008
ATTR_WEATHER_STATION_RSSI3 = 0x0009
ATTR_WEATHER_STATION_RSSI4 = 0x000a
ATTR_WEATHER_STATION_RSSI5 = 0x000b
ATTR_WEATHER_STATION_RSSI6 = 0x000c
ATTR_WEATHER_STATION_RSSI7 = 0x000d

class HaloColor(Color):
    """
    I was able to get this to work by manually calling the service zha.issue_zigbee_cluster_command with the following data:

    ieee: '00:0d:6f:00:0e:bf:3d:e4'
    endpoint_id: 2
    cluster_id: 0x300
    cluster_type: in
    command: 6 # move_to_hue_and_saturation
    command_type: server
    args:
        - 0xFF # Orange-ish?
        - 0xFF # 100% saturation
        - 0x00

    Now I just have to figure out how to get Home Assistant to generate the same call (and what it's doing instead)

    ---

    From what I can TELL, Home Assistant is reading and writing XY values, but the Halo doesn't change them at all.

    So how to I a) tell HA to use Hue/Sat instead of XY, or b) patch the HaloColor class to execute a different command with calculated args when the
    other command is received? 
    """
    pass

class Halo(CustomCluster):
    cluster_id = CLUSTER_HALO
    ep_attribute = "halo"
    name = "Halo"
    manufacturer_attributes = {
        ATTR_DEVICE_STATUS: ("device_status", t.enum8), # TODO: Check this
        ATTR_ROOM: ("room", t.enum8)
    }
    
    def handle_cluster_request(self, tsn, command_id, args):
        logger.debug("Received Halo cluster request {}: ({}) {}".format(tsn, command_id, args))

class HaloControl(CustomCluster):
    cluster_id = 0xFD01

class HaloSensors(CustomCluster):
    cluster_id = 0xFD02

class WeatherRadio(CustomCluster):
    cluster_id = 0xFD03


class HaloWx(CustomDevice):
    signature = {
        MODELS_INFO: [("HaloSmartLabs", "haloWX")],
        ENDPOINTS: {
            ENDPOINT_BASIC: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.LEVEL_CONTROLLABLE_OUTPUT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    PowerConfiguration.cluster_id,
                    Identify.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    PressureMeasurement.cluster_id,
                    RelativeHumidity.cluster_id,
                    IasZone.cluster_id,
                    IasWd.cluster_id
                ],
                OUTPUT_CLUSTERS: [
                    Ota.cluster_id
                ]
            },
            ENDPOINT_LIGHT: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.IAS_WARNING_DEVICE,
                INPUT_CLUSTERS: [
                    Identify.cluster_id,
                    OnOff.cluster_id,
                    LevelControl.cluster_id,
                    HaloColor.cluster_id
                ]
            },
            ENDPOINT_CO: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.IAS_ZONE,
                INPUT_CLUSTERS:[
                    Identify.cluster_id,
                    IasZone.cluster_id
                ]
            },
            ENDPOINT_HALO: {
                PROFILE_ID: zha.PROFILE_ID,
                INPUT_CLUSTERS: [
                    Halo.cluster_id,
                    HaloControl.cluster_id,
                    HaloSensors.cluster_id
                ]
            },
            ENDPOINT_WEATHER: {
                PROFILE_ID: zha.PROFILE_ID,
                INPUT_CLUSTERS: [
                    WeatherRadio.cluster_id
                ]
            }
        }
    }

    replacement = {
        ENDPOINTS: {
            ENDPOINT_BASIC: {
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    PowerConfiguration.cluster_id,
                    Identify.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    PressureMeasurement.cluster_id,
                    RelativeHumidity.cluster_id,
                    IasZone.cluster_id,
                    IasWd.cluster_id
                ],
                OUTPUT_CLUSTERS: [
                    Ota.cluster_id
                ]
            },
            ENDPOINT_LIGHT: {
                DEVICE_TYPE: zha.DeviceType.COLOR_DIMMABLE_LIGHT,
                INPUT_CLUSTERS: [
                    Identify.cluster_id,
                    OnOff.cluster_id,
                    LevelControl.cluster_id,
                    HaloColor
                ]
            },
            ENDPOINT_CO: {
                INPUT_CLUSTERS:[
                    Identify.cluster_id,
                    IasZone.cluster_id
                ]
            },
            ENDPOINT_HALO: {
                INPUT_CLUSTERS: [
                    Halo,
                    HaloControl,
                    HaloSensors
                ]
            },
            ENDPOINT_WEATHER: {
                INPUT_CLUSTERS: [
                    WeatherRadio
                ]
            }
        }
    }
