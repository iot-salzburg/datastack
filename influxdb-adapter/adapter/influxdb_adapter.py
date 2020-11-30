#!/usr/bin/env python3
"""
Example:
    app1 measures the temperature of a machine and sends it into Digital Twin Stack
    app2 is an application which regulates a fan. if the temperatur exceeds a limit,
        it turns on the fan until the temperature falls below a second limit.
        It also sends the fan data into Digital Twin Stack
    datastack subscribes both variables and stores it in InfluxDB
        Jupyter and Grafana helps to display the data.
"""

import os
import json
from influxdb import InfluxDBClient

# Append path of client to pythonpath in order to import the client from cli
try:
    from panta_rhei.client.digital_twin_client import DigitalTwinClient
except ImportError:
    from .panta_rhei.client.digital_twin_client import DigitalTwinClient

verbose = False
# InfluxDB host
INFLUXDB_HOST = os.environ.get("INFLUXDB_HOST", "localhost")  # "192.168.48.71"
# create InfluxDB Connector and create database if not already done
influx_client = InfluxDBClient(INFLUXDB_HOST, 8086, 'root', 'root', 'at.srfg.iot.dtz')
influx_client.create_database('at.srfg.iot.dtz')


# Panta Rhei configuration
config = {"client_name": os.environ.get("CLIENT_NAME", "influxdb-adapter"),
          "system": os.environ.get("SYSTEM_NAME", "at.srfg.iot.dtz"),  # "at.srfg.iot.dtz" in docker-compose env
          "gost_servers": os.environ.get("SENSORTHINGS_HOST", "192.168.48.71:8082"),
          "kafka_bootstrap_servers": os.environ.get("BOOTSTRAP_SERVERS",
                                                    "192.168.48.71:9092,192.168.48.71:9093,192.168.48.71:9094")
          }
# Get dirname from inspect module
dirname = os.path.dirname(os.path.abspath(__file__))
# INSTANCES = os.path.join(dirname, "instances.json")
SUBSCRIPTIONS = os.path.join(dirname, "subscriptions.json")


client = DigitalTwinClient(**config)
# client.register(instance_file=INSTANCES)
client.subscribe(subscription_file=SUBSCRIPTIONS)

# # Init logstash logging for data
# logging.basicConfig(level='WARNING')
# loggername_metric = 'influxdb-adapter'
# logger_metric = logging.getLogger(loggername_metric)
# logger_metric.setLevel(logging.INFO)


print("Loaded clients, InfluxDB-Adapter is ready.")
try:
    while True:
        # Receive all queued messages of 'demo_temperature'
        received_quantities = client.consume(timeout=1)
        new_row = list()
        for received_quantity in received_quantities:
            # The resolves the all meta-data for an received data-point
            # To view the whole data-point in a pretty format, uncomment:
            data = dict()
            data["Datastream"] = dict()
            data["Datastream"]["name"] = received_quantity["Datastream"]["name"].split(".")[-1]
            data["Datastream"]["@iot.id"] = received_quantity["Datastream"]["@iot.id"]
            data["Datastream"]["@iot.selfLink"] = received_quantity["Datastream"]["@iot.selfLink"]
            try:
                data["result"] = float(received_quantity["result"])
            except ValueError:
                print(f"couldn't cast '{received_quantity['result']}' of type '{type(received_quantity['result'])}' to float.")
                continue
            data["phenomenonTime"] = received_quantity["phenomenonTime"]
            # data["resultTime"] = received_quantity["resultTime"]

            # send to influxdb
            if verbose:
                print("Received new data: {}".format(json.dumps(data, indent=2)))
            # all tags and the time create together the key and must be unique
            new_row.append({
                "measurement": "at.srfg.iot.dtz",
                "tags": {
                    # "thing": record["thing"],
                    "quantity": data["Datastream"]["name"],
                    "@iot.id": data["Datastream"]["@iot.id"],
                    "@iot.selfLink": data["Datastream"]["@iot.selfLink"]
                    # "resultTime": data["resultTime"]
                },
                "time": data["phenomenonTime"],
                "fields": {
                    "result": data["result"]
                }
            })
        influx_client.write_points(new_row)

except KeyboardInterrupt:
    client.disconnect()
