# MQTT Bed Sensor

This is a bed sensor I set up following [this 
tutorial](https://everythingsmarthome.co.uk/howto/building-a-bed-occupancy-sensor-for-home-assistant/)
from Lewis Barclay.

I've customized the code a little bit, however.

This essentially captures the weight on our bed to determine when someone (or more than one person)
is in it. This allows us to create automations such as turning on the lights when someone gets out 
of bed in the morning.

## Topics

The following MQTT topics are where data from the sensor come from (I use {bed} to define which bed)
the data is coming from, even though there is currently only one.

 - `bedsensor/{bed}/measurement`: The weight currently in the bed.
 - `bedsensor/{bed}/raw`: The raw output from the HX711 signal amplifier
 - `bedsensor/{bed}/available`: Information about the availability of the device, including if
   it's functioning.

## Commands

Right now, I only have one command I'm listening to for, and that's to tare (reset) the load 
sensors. The command being listened on is `bedsensor/master/tare`

## Development

I actually haven't deployed this yet, so I'm eager to see it work.

I'd eventually like to update the code to allow the ESP8266 to dynamically change the measurement
interval, and attach a battery to the circuit.