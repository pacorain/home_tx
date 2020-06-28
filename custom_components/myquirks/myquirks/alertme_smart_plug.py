from zigpy.quirks import CustomDevice

from ..const import (
    MODELS_INFO,
    ENDPOINTS,
    PROFILE_ID,
    INPUT_CLUSTERS,
    OUTPUT_CLUSTERS
)

AM_PROFILE_ID = 0xC216

CLUSTER_JOIN = 246
CMD_SET_MODE = 0xFA
CMD_RANGE_TEST = 0xFD

CLUSTER_GENERAL = 240
CMD_HELLO_RQST = 0xFC
CMD_STOP_POLLING = 0xFD

CLUSTER_PWR_CTRL = 238
CMD_SET_OPERATING_MODE = 0x01

class AlertMeSmartPlug(CustomDevice):
    signature = {
        MODELS_INFO: [('AlertMe.com', 'SmartPlug2.5')],
        ENDPOINTS: {
            0x02: { # General/Power clusters
                PROFILE_ID: AM_PROFILE_ID,
                INPUT_CLUSTERS: [
                    # 0x00F0 - CLUSTER_GENERAL
                    # 0x00EE - CLUSTER_PWR_CTRL
                    # 0x00EF - CLUSTER_PWR_MON
                ],
                OUTPUT_CLUSTERS: [

                ]
            },
            0xF0: { # Upgrade cluster

            }
        }
    }

    replacement = {
        ENDPOINTS: {
            0x02: { # General/Power clusters
                PROFILE_ID: AM_PROFILE_ID,
                INPUT_CLUSTERS: [
                    # 0x00F0 - CLUSTER_GENERAL
                    # 0x00EE - CLUSTER_PWR_CTRL
                    # 0x00EF - CLUSTER_PWR_MON
                ],
                OUTPUT_CLUSTERS: [

                ]
            },
            0xF0: { # Upgrade cluster

            }
        }
    }

