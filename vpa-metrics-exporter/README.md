# VPA metrics exporter

This container exports metrics from the VPA custom resource, to allow it to be scraped by Prometheus

## Build the docker image

```bash
docker buildx build --platform=linux/amd64 --load -f ./Dockerfile -t elotl/vpa-exporter:0.2 .
```

## Create the deployment and service:

```bash
kubectl apply -f “vpa-tracker/vpa-metrics-exporter/vpa_exporter.yaml”
```

## Create the secret needed to pull images

## Check that the metrics are available
 
