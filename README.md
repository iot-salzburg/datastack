# Datastack for storing, visualizing and analysing data

composed by either an elastic, or influxDB based approach.

InfluxDB is very nice for storing metric data, as we deal with.
However, the open source variant doesn't support scaling on a cluster.
Therefore, the Elastic Stack is our choice.

The datastack is based on the following Components:
* [Elasticsearch 6.3](https://github.com/elastic/elasticsearch-docker)
* [Logstash 6.3](https://github.com/elastic/logstash-docker)
* [Kibana 6.3](https://github.com/elastic/kibana-docker)
* [Grafana 5](http://docs.grafana.org/)
* [Spark 2.1.1](http://spark.apache.org/docs/2.1.1)
* [Hadoop 2.7.3](http://hadoop.apache.org/docs/r2.7.3)
* [PySpark](http://spark.apache.org/docs/2.1.1/api/python)
* [Anaconda3-5](https://www.anaconda.com/distribution/)


Our method to feed data into the DataStack is from the
[Apache Kafka](https://kafka.apache.org/) message bus via the
[db-adapter](https://github.com/iot-salzburg/messaging-system/tree/master/compose/db-adapter).


## Contents

1. [Requirements](#requirements)
2. [Deployment](#deployment)
3. [Services](#services)
4. [Proxy Config](#proxy-config)
5. [Trouble-shooting](#trouble-shooting)



## Requirements

1. Install [Docker](https://www.docker.com/community-edition#/download) version **1.10.0+**
2. Install [Docker Compose](https://docs.docker.com/compose/install/) version **1.6.0+**
3. Setting up a [Docker Swarm](https://www.youtube.com/watch?v=x843GyFRIIY) on a cluster.
4. Clone this repository on the manager node of the docker swarm.


## Deployment

### Setting up the docker environement

This section requires a running `docker swarm`. If not already done, check out
[this video tutorial](https://www.youtube.com/watch?v=KC4Ad1DS8xU&t=192s)
to set up a docker swarm cluster.


Start the Data-Stack using `docker stack` on a manager node:

If not already done, start a registry instance to make the cumstomized jupyter-image
deployable: (we are using port 5001, as logstash's default port is 5000)

```bash
sudo docker service create --name registry --publish published=5001,target=5000 registry:2
curl 127.0.0.1:5001/v2/
```
This should output `{}`:

### Setting up the Elastic Stack, Jupyter and Grafana

Running these commands will build, push and deploy the stack:
```bash
git clone https://github.com/iot-salzburg/dtz_datastack.git
cd dtz_datastack/elasticStack/
./start_stack.sh
```

With these commands we can see if everything worked well:
```bash
./show_stack.sh
docker service ps service-name (e.g stack_elasticsearch)
```

### Setting up the Datastack Adapter

This step requires a running `Panta Rhei` environment.

Install the Panta Rhei client:

```bash
 git clone https://github.com/iot-salzburg/panta_rhei datastack-adapter/panta_rhei > /dev/null 2>&1 || echo "Repo already exists"
 2142  git -C datastack-adapter/panta_rhei/ checkout srfg-digitaltwin
 2143  git -C datastack-adapter/panta_rhei/ pull
 ```
 
 Configure the Panta Rhei system and substribe to datastreams:
 ```python
 # Set the configs, create a new Digital Twin Instance and register file structure
config = {"client_name": "datastore-adapter",
          "system": "at.srfg.iot.dtz",
          "kafka_bootstrap_servers": "192.168.48.71:9092,192.168.48.72:9092,192.168.48.73:9092,192.168.48.74:9092,192.168.48.75:9092"
          "gost_servers": "192.168.48.71:8082"}
client = DigitalTwinClient(**config)
# client.register(instance_file=INSTANCES)
client.subscribe(subscription_file=SUBSCRIPTIONS)
```


##  Services

Give Kibana a minute to initialize, then access the Kibana web UI by hitting
[http://localhost:5601](http://localhost:5601) with a web browser.
The indexing of elasticsearch could last 15 minutes or more, so we have to be patient.
On Kibana UI, DevTools we can trace the indexing success by hitting the REST request
`GET _cat/indices`.



By default, the stack exposes the following ports:
* 5000: Logstash TCP input
* 9600: Logstash HTTP
* **5601: Kibana:** User Interface for data in Elasticsearch
* **8080: Grafana** Grafic visualisation specialised for metric data
* **8888: Jupyter GUI:** Run Python and R notebooks along Spark
on elastic data

**bold** listings stand for User interfaces.



### Tracing

Watch if everything worked fine with:
```bash
sudo docker service ls
sudo docker service logs -f service-name
sudo docker service ps service-name --no-trunc
```




## Proxy Config

If used behind an apache2 proxy, make sure to enable additional moduls
```bash
sudo a2enmod ssl rewrite proxy proxy_http proxy_wstunnel
```

Use the following config (note that the notebook will
be available in https:/url/jupyter)

```
RewriteRule ^/jupyter$ jupyter/tree/ [R]
                RewriteRule ^/jupyter/$ jupyter/tree/ [R]

                <Location "/jupyter">
                    ProxyPass        http://localhost:8888/jupyter
                    ProxyPassReverse http://localhost:8888/jupyter
                </Location>

                <Location "/jupyter/api/kernels">
                    ProxyPass        ws://localhost:8888/jupyter/api/kernels
                    ProxyPassReverse ws://localhost:8888/jupyter/api/kernels
                </Location>
                <Location "/jupyter/terminals/websocket">
                        ProxyPass        ws://localhost:8888/jupyter/terminals/websocket
                        ProxyPassReverse ws://localhost:8888/jupyter/terminals/websocket
                </Location>


                #ProxyPass /jupyter/api/kernels/ ws://127.0.0.1:8888/jupyter/api/kernels/
                #ProxyPassReverse /jupyter/api/kernels/ ws://127.0.0.1:8888/jupyter/api/kernels/

                #ProxyPass /jupyter http://localhost:8888/jupyter connectiontimeout=15 timeout=30
                #ProxyPassReverse /jupyter http://localhost:8888/jupyter

                ProxyPass /jupyter/tree http://127.0.0.1:8888/jupyter/tree
                ProxyPassReverse /jupyter/tree http://127.0.0.1:8888/jupyter/tree


                #ProxyPass /jupyter http://127.0.0.1:8888/jupyter/
                #ProxyPassReverse /jupyter http://127.0.0.1:8888/jupyter/


                #<Location ~ "/(user/[^/]*)/(api/kernels/[^/]+/channels|terminals/websocket)/?">
                #       ProxyPass ws://localhost:8888/jupyter
                #       ProxyPassReverse ws://localhost:8888/jupyter
                #</Location>
```

For more help, see [here](https://stackoverflow.com/questions/23890386/how-to-run-ipython-behind-an-apache-proxy/28819231#28819231)





## Trouble-shooting

#### Can't apt-get update in Dockerfile:
Restart the service

```sudo service docker restart```

or add the file `/etc/docker/daemon.json` with the content:
```
{
    "dns": [your_dns, "8.8.8.8"]
}
```
where `your_dns` can be found with the command:

```bash
nmcli device show <interfacename> | grep IP4.DNS
```

####  Traceback of non zero code 4 or 128:

Restart service with
```sudo service docker restart```

or add your dns address as described above


####  Elasticsearch crashes instantly:

Check permission of `elasticsearch/data`.

```bash
sudo chown -r USER:USER .
sudo chmod -R 777 .
```

or remove redundant docker installations or reinstall it


#### Error starting userland proxy: listen tcp 0.0.0.0:9200: bind: address already in use

Bring down other services, or change the hosts port number in docker-compose.yml.

Find all running services by:
```bash
sudo docker ps
```


#### errors while removing docker containers:

Remove redundant docker installations


#### "entire heap max virtual memory areas vm.max_map_count [...] likely too low, increase to at least [262144]"

Run on host machine:

```bash
sudo sysctl -w vm.max_map_count=262144
```




