# DataStack for Storing, Visualizing and Analysing data

#### Composed of Grafana, Jupyter and InfluxDB or optionally Elastic Stack


The DataStack is based on the following Components:
* [Anaconda](https://www.anaconda.com/distribution/)
* [Jupyter](https://jupyter.org/)
* [GPU-Jupyter](https://github.com/iot-salzburg/gpu-jupyter)
* [Grafana](http://docs.grafana.org/)
* [InfluxDB](https://www.influxdata.com/)
* [Elasticsearch](https://github.com/elastic/elasticsearch-docker)
* [Logstash](https://github.com/elastic/logstash-docker)
* [Kibana](https://github.com/elastic/kibana-docker)

Additionally, a DataStack Adapter is provided to feed data into the respective database.
The DataStack Adapter is based on the [Panta Rhei project](https://github.com/iot-salzburg/panta_rhei), 
i.e., it expects data to be accessible as in Panta Rhei with a Kafka 
messaging layer and SensorThings semantic. 
This Adapter, however, can be easily changed to other data sources. 


## Requirements

1. Install [Docker](https://www.docker.com/community-edition#/download) version **1.10.0+**
2. Install [Docker Compose](https://docs.docker.com/compose/install/) version **1.6.0+**
3. Setting up a [Docker Swarm](https://www.youtube.com/watch?v=x843GyFRIIY) on a cluster. **(optional)**.

    If not already done, start a registry instance to make the cumstomized images
    deployable: (we are using port 5001, as logstash's default port is 5000)
    
    ```bash
    sudo docker service create --name registry --publish published=5001,target=5000 registry:2
    curl 127.0.0.1:5001/v2/
    ```
    This should output `{}`:

4. Clone this repository recursively on the manager node of the docker swarm or on a master node.

    ```bash
    git clone --recurse-submodules  https://github.com/iot-salzburg/dtz_datastack.git
    cd datastack/
    ```

5. **(only for the Elastic Stack)** Set `vm.max_map_count` permanently in `/etc/sysctl.conf`:
    ```bash
    grep vm.max_map_count /etc/sysctl.conf
    # -> vm.max_map_count=262144
    
    # or set it temporarily 
    sysctl -w vm.max_map_count=262144
    ```

6. Create a new virtualenv and install the requirements:

   ```bash
   cd ../datastack
   pip3 install virtualenv
   source .venv/bin/activate
   pip3 install -r influxdb-adapter/requirements.txt
   ```


## Setup

Continue the setup with the following parts. Note that there are two possible 
databases, however, InfluxDB is recommended:

1. [InfluxDB and Grafana](InfluxDB_Grafana/README.md) (in a sub-directory)
2. (Alternative to InfluxDB) [Elastic Stack](elasticStack/README.md) and [Grafana](grafana/README.md) (in a sub-directory)
3. [InfluxDB Adapter](influxdb-adapter/README.md) (in a sub-directory)
3. (Alternative to InfluxDB) [ElaticStack Adapter](elastic-adapter/README.md) (in a sub-directory)
5. [Jupyter Notebook](jupyter/README.md) (in a sub-directory)
4. [Proxy Config](#proxy-config)
5. [Trouble Shooting](#trouble-shooting)



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

```bash
sudo service docker restart
# or
sudo service apparmor restart
```

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


#### curl 127.0.0.1:5001/v2/ gives no response

If `192.168.48.XX:5001/v2/` works when `XX` is another node, then a restart fixed the problem. Maybe also a docker restart works.


#### "entire heap max virtual memory areas vm.max_map_count [...] likely too low, increase to at least [262144]"

Run on host machine:

```bash
sudo sysctl -w vm.max_map_count=262144
```
