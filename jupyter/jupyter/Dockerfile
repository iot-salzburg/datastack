# Copyright (c) Salzburg Research
FROM jupyter/all-spark-notebook:6c3390a9292e
LABEL maintainer="Christoph Schranz <iotlab@salzburgresarch.at>"

USER root

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  git apt-utils wget python-pip unzip && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

#ENV PYSPARK_PYTHON /opt/conda/bin/python
# Install es-hadoop
RUN apt-get update \
 && curl -sL http://central.maven.org/maven2/org/elasticsearch/elasticsearch-hadoop/6.8.1/elasticsearch-hadoop-6.8.1.jar

RUN set -ex \
 && buildDeps=' \
    elasticsearch==6.3.1 \
#    rpy2==2.9.4 \
 ' \
 && apt-get update \
 && apt-get -y upgrade \
 && apt-get -y install r-base \
 && pip install --no-cache-dir $buildDeps \
 && rm -rf /home/$NB_USER/.local \
 && fix-permissions $CONDA_DIR \
 && fix-permissions /home/$NB_USER

# Install rpy2 to share data between Python and R
RUN conda install rpy2=2.9.4

RUN jupyter labextension install @jupyterlab/github
RUN jupyter labextension install jupyterlab-drawio

# Change jupyter_notebook_config.py
COPY jupyter_notebook_config.json /home/jovyan/.jupyter/jupyter_notebook_config.json

RUN mkdir /home/$NB_USER/.local
RUN chmod -R 755 /home/$NB_USER/.local
RUN chown -R $NB_USER:users /home/$NB_USER/.local
USER $NB_USER
