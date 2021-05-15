import logging
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from homeassistant.core import HomeAssistant

from threading import Thread

from queue import Queue, Empty
from datetime import datetime
fromt time import sleep

from logging.handlers import QueueHandler, SysLogHandler

SYSLOG_LEVELS = {
    logging.CRITICAL: SysLogHandler.LOG_CRIT,
    logging.ERROR: SysLogHandler.LOG_ERR,
    logging.WARNING: SysLogHandler.LOG_WARNING,
    logging.INFO: SysLogHandler.LOG_INFO,
    logging.DEBUG: SysLogHandler.LOG_DEBUG,
}

NANOSECONDS_PER_SECOND = 1000000000

DOMAIN = "influx_logger"


logger = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config):
    root_logger = logging.getLogger()
    # Don't pass any InfluxDB logs to InfluxDB 
    q = Queue()
    logger.debug("Setting up InfluxDB Logging")
    handler = QueueHandler(q)
    handler.addFilter(lambda record: not logging.Filter('influxdb_client').filter(record))
    root_logger.addHandler(QueueHandler(q))
    token = "{}:{}".format(config[DOMAIN]["username"], config[DOMAIN]["password"])
    Thread(target=worker, args=(q, hass, token)).start()

    logger.info("Started logging to InfluxDB")
    return True


def worker(q, hass: HomeAssistant, token):
    """Runs in alternate thread to handle new logging records."""
    global wait_seconds
    wait_seconds = 1
    client = InfluxDBClient(url="http://a0d7b954-influxdb:8086", token=token, retries=5)
    logger.debug("InfluxDB logging client connected!")
    database = "debug/debug"
    batch = []
    while not hass.is_stopping:
        try:
            while len(batch) < 50:
                try:
                    record = q.get_nowait()
                    entry = parse_record(record)
                    batch.append(entry)
                except Empty:
                    break
            if batch:
                write_client = client.write_api(write_options=SYNCHRONOUS)
                write_client.write(bucket=database, org="", record=batch)
                write_client.close()
                batch = []
        except influxdb_client.rest.ApiException:
            logger.error(f"Something went wrong with InfluxDB logging. Will try again in {wait_seconds} seconds.", exc_info=True)
            time.sleep(wait_seconds)
            wait_seconds = min(wait_seconds * 2, 1800)
    logger.info("Logging to InfluxDB has stopped")
            
            

def parse_record(record):
    tags = {
        "host": "homeassistant",
        "hostname": "homeassistant",
        "level": SYSLOG_LEVELS.get(record.levelno, record.levelno),
        "level_name": logging.getLevelName(record.levelno),
        "severity": logging.getLevelName(record.levelno).lower(),
        "appname": record.name
    }
    msg = record.getMessage()
    fields = {
        "message": msg,
        "severity_code": SYSLOG_LEVELS.get(record.levelno, record.levelno),
        "procid": str(record.process),
        "timestamp": int(record.created * 1000000000),
        "file": record.pathname,
        "line": record.lineno,
        "function": record.funcName,
        "thread_name": record.threadName
    }
    if record.exc_info and not record.exc_text:
        # format exception information if present
        formatter = logging._defaultFormatter
        record.exc_text = formatter.formatException(record.exc_info)
    if record.exc_text:
        fields["full_message"] = "\n".join([msg, record.exc_text])
    skip_list = (
        "args", "asctime", "created", "exc_info",  "exc_text", "filename",
        "funcName", "id", "levelname", "levelno", "lineno", "module",
        "msecs", "message", "msg", "name", "pathname", "process",
        "processName", "relativeCreated", "thread", "threadName"
    )
    for key, value in record.__dict__.items():
        if value is None:
            continue
        if key not in skip_list and not key.startswith("_"):
            fields[key] = value
    return {
        "measurement": "syslog",
        "tags": tags,
        "fields": fields,
        "time": datetime.utcfromtimestamp(record.created)
    }

