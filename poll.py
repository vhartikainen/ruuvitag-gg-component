import sys
import argparse
import ruuvitag_sensor
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import os
import json
import awsiot.greengrasscoreipc
import logging
import bleson

from ruuvitag_sensor.log import log
ruuvitag_sensor.log.enable_console()

import awsiot.greengrasscoreipc
from awsiot.greengrasscoreipc.model import (
    QOS,
    PublishToIoTCoreRequest
)

from ruuvitag_sensor.ruuvi import RuuviTagSensor

# TODO: Set the log level to something less verbose
bleson.logger.set_level(logging.ERROR)
# TODO: Parameterize
#mqtt_broker='test.mosquitto.org'
mqtt_broker='homeassistant.local'
mqtt_broker_username='mqtt'
mqtt_broker_password='mqtt'
topic='/ruuvi/{}/{}' # /ruuvi/<macaddress>/<measurement
iot_topic='/ruuvi/{}' # /ruuvi/<macaddress>

# The callback for when the client receives a CONNACK response from the MQTT server.
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")

client=""
ipc_client=""
gg=False

def initializeGGIPC():
    ipc_client = awsiot.greengrasscoreipc.connect()

def sendToIoTCore(topic, message):
    TIMEOUT = 10

    log.info("Sending to IoT Core - {} - {}".format(topic,message))
    qos = QOS.AT_LEAST_ONCE

    request = PublishToIoTCoreRequest()
    request.topic_name = topic
    request.payload = bytes(json.dumps(message), "utf-8")
    request.qos = qos
    operation = ipc_client.new_publish_to_iot_core()
    operation.activate(request)
    future = operation.get_response()
    future.result(TIMEOUT)


# TODO: Send over to IoT Core
measurements=["temperature","humidity","pressure","battery"]
def handle_data(found_data):
    mac=found_data[0].replace(":","").lower()
    log.info('MAC=%s', found_data[0])
    log.info("Temperature=%s", found_data[1]['temperature'])
    log.info("Data format=%s", found_data[1]['data_format'])
    print(found_data[1])
    if found_data[1]['data_format']<5:
        log.error("older data")

    # For IoT Core, just send the whole JSON document
    if gg:
        sendToIoTCore(iot_topic.format(mac),found_data[1])

    # TODO: Consider submitting a JSON with measurements: https://www.home-assistant.io/integrations/sensor.mqtt/#temperature-and-humidity-sensors
    for key in measurements:
        if key in found_data[1]:
            log.debug("{}={}".format(key,found_data[1][key]))
            mqtt_topic=topic.format(mac,key)
            try:
                log.info("send to mqtt topic {}".format(mqtt_topic))
                client.publish(mqtt_topic, found_data[1][key])
            except:
                log.error("Failed to publish to MQTT or IoT core")
        else:
            log.error("key {} not found".format(key))

if __name__ == '__main__':
    try:
        os.environ["AWS_GG_NUCLEUS_DOMAIN_SOCKET_FILEPATH_FOR_COMPONENT"]
        ipc_client = awsiot.greengrasscoreipc.connect()
        gg=True
        print("Starting: Running on GG")
        print("Initializing the IoT Core")
        initializeGGIPC()
    except:
        print("Starting: Not running on GG")

    # TODO: Publish single test message / move to handler

    client = mqtt.Client("ruuvi-poller")
    client.on_connect = on_connect
    if mqtt_broker_username!=None:
        client.username_pw_set(mqtt_broker_username,password=mqtt_broker_password)
    client.connect(mqtt_broker, 1883, 60)
    client.loop_start()
    
    # Start polling RuuviTags
    RuuviTagSensor.get_datas(handle_data)

