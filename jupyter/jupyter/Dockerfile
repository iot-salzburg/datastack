# Copyright (c) Salzburg Research

FROM jupyter/all-spark-notebook:6c3390a9292e
LABEL maintainer="Christoph Schranz <iotlab@salzburgresarch.at>"

USER root

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  git apt-utils wget python-pip unzip && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

## installing es-hadoop
ENV PYSPARK_PYTHON /opt/conda/bin/python
RUN apt-get update \
 && curl -sL http://central.maven.org/maven2/org/elasticsearch/elasticsearch-hadoop/6.2.1/elasticsearch-hadoop-6.2.1.jar

RUN set -ex \
 && buildDeps=' \
    elasticsearch==6.3.1 \
    rpy2==2.9.2 \
 ' \
 && apt-get update \
 && apt-get -y upgrade \
 && apt-get -y install r-base \
 && pip install --no-cache-dir $buildDeps \
 && rm -rf /home/$NB_USER/.local \
 && fix-permissions $CONDA_DIR \
 && fix-permissions /home/$NB_USER

# Change jupyter_notebook_config.py
COPY jupyter_notebook_config.json /home/jovyan/.jupyter/jupyter_notebook_config.json

USER jovyan

