# Pod resource consumption tracker

## Install kube-state-metrics

kube-state-metrics enables export of metrics associated with k8s resources.

https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-state-metrics


## Install Prometheus

Prometheus is a open-source monitoring and alerting toolkit. It scrapes metrics from Kubernetes clusters.

Install Prometheus using the steps here:

https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack

## Install grafana

Grafana is an open-source monitoring platform for visualizing metrics.

## Grafana dashboard for VPA metrics

https://grafana.com/grafana/dashboards/14588-vpa-recommendations/



## Allow VPA to export metrics:

### Step 1: Expose the VPA Recommender Metrics

By default, the VPA recommender exposes metrics on port 8942.

You need to ensure there's a Kubernetes Service for the recommender pod that maps to this port.

kubectl apply -f ~/stuff/vpa-tracker/vpa-metrics-expose-svc.yaml


### Step 2: For the Prometheus Operator, create a ServiceMonitor:


Apply
kubectl apply -f ~/stuff/vpa-tracker/vpa-recommender-servicemonitor.yaml


## Access different services:

1. Prometheus service:


% kubectl port-forward svc/luna-prometheus-kube-prome-prometheus 9090:9090
http://localhost:9090


2. See the list of kube state metrics being exported:

% kubectl port-forward svc/kube-state-metrics 8080:8080

http://localhost:8080/metrics

3. Viewing Grafana 


% kubectl port-forward service/grafana 3000:3000 --namespace=my-grafana

http://localhost:3000 


## VPA metrics' examples

Once Prometheus starts scraping, you'll find metrics like:

    vpa_target_container_recommendation

    vpa_recommendation_cpu_lower_bound

    vpa_recommendation_memory_upper_bound


