# Datastack for storing, visualizing and analysing data

#### Composed by the Elastic Stack, Grafana and Jupyter


The datastack is based on the following Components:
* [Elasticsearch 6.2](https://github.com/elastic/elasticsearch-docker)
* [Logstash 6.2](https://github.com/elastic/logstash-docker)
* [Kibana 6.2](https://github.com/elastic/kibana-docker)
* [Grafana 6](http://docs.grafana.org/)
* [Spark](http://spark.apache.org/docs/2.1.1)
* [Hadoop](http://hadoop.apache.org/docs/r2.7.3)
* [PySpark](http://spark.apache.org/docs/2.1.1/api/python)
* [Anaconda3-5](https://www.anaconda.com/distribution/)

The easiest way to feed data into the DataStack is to use the
[datastack-adapter](https://github.com/iot-salzburg/dtz_datastack/tree/master/datastack-adapter) to stream data
from the [panta-rhei messaging system](https://github.com/iot-salzburg/dtz_datastack/tree/master/elasticStack).



## Setup

1. [Requirements](#requirements)
2. [Elastic Stack](elasticStack/README.md) (in sub-directory)
3. [Datastack Adapter](datastack-adapter/README.md) (in sub-directory)
4. [Grafana](grafana/README.md) (in sub-directory)
5. [Jupyter Notebook](jupyter/README.md) (in sub-directory)
4. [Proxy Config](#proxy-config)
5. [Trouble Shooting](#trouble-shooting)


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

4. Clone this repository on the manager node of the docker swarm or on a master node.

    ```bash
    git clone https://github.com/iot-salzburg/dtz_datastack.git
    cd dtz_datastack/
    ```

5. Set `vm.max_map_count` permanently in `/etc/sysctl.conf`:
    ```bash
    grep vm.max_map_count /etc/sysctl.conf
    # -> vm.max_map_count=262144
    
    # or set it temporarily 
    sysctl -w vm.max_map_count=262144
    ```

### Contiue with

2. [Elastic Stack](elasticStack/README.md) (in sub-directory)
3. [Datastack Adapter](datastack-adapter/README.md) (in sub-directory)
4. [Grafana](grafana/README.md) (in sub-directory)
5. [Jupyter Notebook](jupyter/README.md) (in sub-directory)



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


#### "entire heap max virtual memory areas vm.max_map_count [...] likely too low, increase to at least [262144]"

Run on host machine:

```bash
sudo sysctl -w vm.max_map_count=262144
```
