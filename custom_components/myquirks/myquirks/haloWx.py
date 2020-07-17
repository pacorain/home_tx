from zigpy.quirks import CustomDevice, CustomCluster, CustomEndpoint
from zigpy.profiles import zha
from zigpy.zcl.clusters.general import Basic, Identify, Ota, OnOff, LevelControl
from zigpy.zcl.clusters.measurement import TemperatureMeasurement, PressureMeasurement, RelativeHumidity
from zigpy.zcl.clusters.security import IasWd, IasZone
from zigpy.zcl.clusters.lighting import Color
from zigpy.zcl.clusters.manufacturer_specific import ManufacturerSpecificCluster

from zhaquirks import PowerConfigurationCluster

from ..const import (
    MODELS_INFO,
    ENDPOINTS,
    PROFILE_ID,
    DEVICE_TYPE,
    INPUT_CLUSTERS,
    OUTPUT_CLUSTERS
)


class ZoneStatus(CustomCluster):
    cluster_id = 0x0500

class HaloGeneral(CustomCluster):
    cluster_id = 0xFD00

class HaloControl(CustomCluster):
    cluster_id = 0xFD01

class HaloMspSensors(CustomCluster):
    cluster_id = 0xFD02

class WeatherRadio(CustomCluster):
    cluster_id = 0xFD03


class HaloWx(CustomDevice):
    signature = {
        MODELS_INFO: [("HaloSmartLabs", "haloWX")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: IasZone.ZoneType.Fire_Sensor,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    PowerConfigurationCluster.cluster_id,
                    Identify.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    PressureMeasurement.cluster_id,
                    RelativeHumidity.cluster_id,
                    ZoneStatus.cluster_id,
                    IasWd.cluster_id
                ],
                OUTPUT_CLUSTERS: [
                    Ota.cluster_id
                ]
            },
            2: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.COLOR_DIMMABLE_LIGHT,
                INPUT_CLUSTERS: [
                    OnOff.cluster_id,
                    LevelControl.cluster_id,
                    Color.cluster_id
                ]
            },
            3: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: IasZone.ZoneType.Carbon_Monoxide_Sensor,
                INPUT_CLUSTERS:[
                    ZoneStatus.cluster_id
                ]
            },
            4: {
                PROFILE_ID: zha.PROFILE_ID,
                INPUT_CLUSTERS: [
                    HaloGeneral.cluster_id,
                    HaloControl.cluster_id,
                    HaloMspSensors.cluster_id
                ]
            },
            5: {
                PROFILE_ID: zha.PROFILE_ID,
                INPUT_CLUSTERS: [
                    WeatherRadio.cluster_id
                ]
            }
        }
    }

    replacement: {
        ENDPOINTS: {
            1: {
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    PowerConfigurationCluster.cluster_id,
                    Identify.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    PressureMeasurement.cluster_id,
                    RelativeHumidity.cluster_id,
                    ZoneStatus.cluster_id,
                    IasWd.cluster_id
                ],
                OUTPUT_CLUSTERS: [
                    Ota.cluster_id
                ]
            },
            2: {
                INPUT_CLUSTERS: [
                    OnOff.cluster_id,
                    LevelControl.cluster_id,
                    Color.cluster_id
                ]
            },
            3: {
                INPUT_CLUSTERS:[
                    ZoneStatus.cluster_id
                ]
            },
            4: {
                INPUT_CLUSTERS: [
                    HaloGeneral.cluster_id,
                    HaloControl.cluster_id,
                    HaloMspSensors.cluster_id
                ]
            },
            5: {
                INPUT_CLUSTERS: [
                    WeatherRadio.cluster_id
                ]
            }
        }
    }