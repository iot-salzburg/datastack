# Datastack Adapter

#### This is the adapter between the [Panta Rhei](https://github.com/iot-salzburg/panta_rhei) messaging system and the [Datastack](https://github.com/iot-salzburg/dtz_datastack/tree/master/elasticStack).

The adapter is based on the Digital Twin client which allows the multi-tenant streaming of data easily.

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

* Install [Docker](https://www.docker.com/community-edition#/download) version **1.10.0+**
* Install [Docker Compose](https://docs.docker.com/compose/install/) version **1.6.0+**
* A running [Datastack](https://github.com/iot-salzburg/dtz_datastack/tree/master/elasticStack) which is in this repo
* A running [Panta Rhei](https://github.com/iot-salzburg/panta_rhei) messaging system
* Clone this repository

    

## Quickstart

This is an instruction on how to set up a demo scenario on your own hardware.
Here, we use Ubuntu 18.04.

```bash
git clone https://github.com/iot-salzburg/dtz_datastack.git
cd git_datastack/datastack-adapter
git clone https://github.com/iot-salzburg/panta_rhei.git adapter/panta_rhei
```

Configure the adapter in the `docker-compose.yml`:

```yml
services:
  datastore-adapter:
    ...
    environment:
      # Datastack configuration
      LOGSTASH_HOST: "192.168.48.71"
      # Panta Rhei configuration
      CLIENT_NAME: "datastore-adapter"
      SYSTEM_NAME: "at.srfg.iot.dtz"
      SENSORTHINGS_HOST: "192.168.48.71:8082"
      BOOTSTRAP_SERVERS: "192.168.48.71:9092,192.168.48.72:9092,192.168.48.73:9092,192.168.48.74:9092,192.168.48.75:9092"
```
 
Test the setup using testing parameters, e.g. `LOGSTASH_HOST: "localhost"`.

```bash
python3 datastack-adapter/adapter/datastore_adapter.py
```

## Deployment

Make sure you have a running [Docker Swarm](https://www.youtube.com/watch?v=x843GyFRIIY).
Add the service `add-datastore` with:

```bash
sh start-datastore-adapter.sh
```

Now, data from the Panta Rhei system will be streamed into the Datastack.

