from .myquirks.alertme_smart_plug import AlertMeSmartPlug

DOMAIN = "myquirks"

def setup(hass, config):
    # No setup needed, we just need to import the quirks
    return True