FROM grafana/grafana:6.2.5

USER root

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  gettext

# in the container you just started:
RUN chown -R root:root /etc/grafana && \
  chmod -R a+r /etc/grafana && \
  chown -R grafana:grafana /var/lib/grafana && \
  chown -R grafana:grafana /usr/share/grafana

RUN grafana-cli plugins install grafana-worldmap-panel \
 && grafana-cli plugins install natel-plotly-panel 0.0.5 \
 && grafana-cli plugins install ae3e-plotly-panel \
 && grafana-cli plugins install grafana-piechart-panel \
 && grafana-cli plugins install simpod-json-datasource

ENTRYPOINT su grafana && sh /run.sh
