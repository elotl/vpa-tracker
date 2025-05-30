# VPA Tracker to right size your pods

## Install kube-state-metrics

kube-state-metrics enables export of metrics associated with k8s resources such as deployments, jobs, etc.

This is what allows us to export metrics from the VPA custom resource.

Project repo: https://github.com/kubernetes/kube-state-metrics


We install kube-state-metrics using docs from here:

https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-state-metrics

```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install kube-state-metrics prometheus-community/kube-state-metrics [flags]
```

Its pod and svc is available as shown below:

```
% kubectl get svc                                
NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
kube-state-metrics   ClusterIP   10.100.242.107   <none>        8080/TCP   38m
kubernetes           ClusterIP   10.100.0.1       <none>        443/TCP    40d
selvik@Selvis-MacBook-Pro vpa-tracker % kubectl get pods                               
NAME                                 READY   STATUS    RESTARTS   AGE
kube-state-metrics-b49796bf8-sq7xv   1/1     Running   0          38m
```

Port forward the svc


View the metrics in the URL: http://localhost:8080/metrics
Home page of kube state metrics: http://localhost:8080/


https://github.com/kubernetes/kube-state-metrics/blob/master/docs/README.md#exposed-metrics


## Install Kube-Prometheus

git clone git@github.com:prometheus-operator/kube-prometheus.git

% kubectl apply --server-side -f manifests/setup --force-conflicts

Wait for all services:

kubectl wait \
	--for condition=Established \
	--all CustomResourceDefinition \
	--namespace=monitoring

Check all resources:
kubectl get all -n monitoring


kubectl apply -f manifests/

View all GUIS
kubectl --namespace monitoring port-forward svc/prometheus-k8s 9090
kubectl --namespace monitoring port-forward svc/grafana 3000

Ref: https://github.com/prometheus-operator/kube-prometheus/blob/main/docs/access-ui.md



## Install Prometheus

Prometheus is an open-source monitoring and alerting toolkit. It scrapes metrics from Kubernetes clusters.

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

kubectl port-forward svc/kube-prometheus-stack-grafana -n monitoring 3000:80
http://localhost:3000 


## VPA metrics' examples

Once Prometheus starts scraping, you'll find metrics like:

    vpa_target_container_recommendation

    vpa_recommendation_cpu_lower_bound

    vpa_recommendation_memory_upper_bound

S
