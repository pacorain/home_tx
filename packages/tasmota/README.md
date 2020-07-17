# Tasmota

Author: Austin Rainwater

This package controls some [Tasmota](https://tasmota.github.io/docs/) lights with [MQTT 
automation](https://www.home-assistant.io/docs/automation/trigger/#mqtt-trigger). The automations
in this package serve as a bridge between custom [MQTT
lights](https://www.home-assistant.io/integrations/light.mqtt/) and the 
[MQTT topics](https://tasmota.github.io/docs/MQTT/) for Tasmota.

This requires an MQTT Broker. I'm using the official [Mosquitto addon for Home
Assistant](https://github.com/home-assistant/hassio-addons/tree/master/mosquitto).

