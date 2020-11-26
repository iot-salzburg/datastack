import json
from influxdb import InfluxDBClient

# create InfluxDB Connector and create database if not already done
client = InfluxDBClient('localhost', 8086, 'root', 'root', 'at.srfg.iot.dtz')
client.create_database('at.srfg.iot.dtz')
print(client.get_list_database())

result = client.query('select count(*) from "at.srfg.iot.dtz";')

for res in result.get_points():
    print(res)
