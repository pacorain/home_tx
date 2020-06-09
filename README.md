# Austin Rainwater's Home Assistant Config

[![GitHub issues](https://img.shields.io/github/issues/pacorain/home)](https://github.com/pacorain/home/issues)

## About

This is my (Austin Rainwater) [Home Assistant](https://www.home-assistant.io) configuration. It has
some of the device configuration, as well as my automations, groups, etc.

My goals in setting up my smart home are security, comfort, convenience, and innovation 
without compromise. 

I started with [Lowe's Iris](https://www.irisbylowes.com) before it was shut down. I then switched 
to SmartThings and Ring, and found they were not as compatible and flexible as I was hoping. As 
a result, I have a large mix of devices, some of which most platforms have no idea what to do with.

I also use multiple platforms that can serve as "clients" of Smart Homes, including HomeKit, Alexa,
and Google Home. My configuration contains customizations for my devices.

## Featured Integrations

Some of the things that I wanted to do required a little bit of work, and I've been able to get
Home Assitant to do what I want.

  - Security with the [manual alarm control panel](https://www.home-assistant.io/integrations/manual/)
    - I use [groups](https://github.com/pacorain/home/tree/master/groups/security) to manage the
      devices that are monitored when the security system is armed.
    - I have special [template sensors](https://github.com/pacorain/home/blob/master/entities/sensor/security.yaml) 
      that [`expand`](https://www.home-assistant.io/docs/configuration/templating/#working-with-groups)
      the security devices recursively and complie the statuses of all of them.
    - Finally, I use a series of [automations](https://github.com/pacorain/home/tree/master/automations/security)
      to manage what happens when security devices trip, when the alarm is fully triggered, etc.
  - [Automatic updating when I push to GitHub](https://github.com/pacorain/home/blob/master/automations/github_webhook.yaml)
  - [Turn on the light for the pizza delivery driver](https://github.com/pacorain/home/blob/master/automations/pizza_delivery_light.yaml)



