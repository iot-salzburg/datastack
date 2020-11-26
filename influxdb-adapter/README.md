# Panta Rhei - InfluxDB - Adapter

#### This is the Adapter between [Panta Rhei](https://github.com/iot-salzburg/panta_rhei) messaging system and this [DataStack](https://github.com/iot-salzburg/datastack).

The adapter is based on the Panta Rhei (or Digital Twin) client which allows the multi-tenant streaming of data easily.

```python3
from client.digital_twin_client import DigitalTwinClient
config = {"client_name": "demo_app1", "system_name": "demo-system",
          "kafka_bootstrap_servers": "localhost:9092", "gost_servers": "localhost:8082"}
client = DigitalTwinClient(**config)
client.register(instance_file="digital_twin_mapping/instances")
client.send(quantity="demo_temperature", result=23.4)
```


## Contents

1. [Requirements](#requirements)
2. [Quickstart](#quickstart)
3. [Deploy on a Cluster](#deployment)


## Requirements

* A running instance of InfluxDB, set it up is described [here](../InfluxDB_Grafana/README.md).
* A running [Panta Rhei](https://github.com/iot-salzburg/panta_rhei) messaging system with data.

    

## Quickstart

This is an instruction on how to set up a demo scenario on your own hardware.
Here, we use Ubuntu 18.04.

```bash
cd influxdb-adapter
git clone https://github.com/iot-salzburg/panta_rhei.git adapter/panta_rhei
```

Configure the adapter in the `docker-compose.yml`:

```yaml
version: '3.4'
services:
  datastore-adapter:
    image: 127.0.0.1:5001/datastore-adapter
    build: .
    network_mode: host
    environment:
      # InfluxDB configuration
      INFLUXDB_HOST: "localhost"
      # Panta Rhei configuration
      CLIENT_NAME: "influxdb-adapter"
      SYSTEM_NAME: "at.srfg.iot.dtz"
      SENSORTHINGS_HOST: "192.168.48.71:8082"
      BOOTSTRAP_SERVERS: "192.168.48.71:9092,192.168.48.71:9093,192.168.48.71:9094"
```
 
To start the adapter, run the following command:


```bash
python3 influxdb-adapter/adapter/influxdb_adapter.py
```
This step requires a reachable InfluxDB endpoint on [localhost:8086](localhost:8086).
In this connector, the package [influxdb-python](https://influxdb-python.readthedocs.io/en/latest/include-readme.html)
was used. The used InfluxDB table is called `at.srfg.iot.dtz`.


Check if data is stored in `InfluxDB` using this script
 (it counts the number of rows in a set database):
 
 ```bash
python3 InfluxDB_Grafana/db_interface.py
#> {'time': '1970-01-01T00:00:00Z', 'count_result': 321825}
```
 


## Deployment

Make sure you have a running [Docker Swarm](https://www.youtube.com/watch?v=x843GyFRIIY).
Add the service `datastore-adapter` with:

```bash
docker-compose up --build -d
```

Now, data from the **Panta Rhei system** will be streamed into the **DataStack**.
