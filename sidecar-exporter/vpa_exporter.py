from kubernetes import client, config
from prometheus_client import start_http_server, Gauge
import time
import logging
import re

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load Kubernetes config (in-cluster or local for testing)
try:
    config.load_incluster_config()
except config.ConfigException:
    config.load_kube_config()

# Kubernetes API client
api = client.CustomObjectsApi()

# Define Prometheus metrics
cpu_target_gauge = Gauge(
    'vpa_cpu_target_millicores',
    'VPA recommended target CPU for container (in millicores)',
    ['namespace', 'vpa_name', 'container']
)
cpu_uncapped_gauge = Gauge(
    'vpa_cpu_uncapped_target_millicores',
    'VPA uncapped target CPU for container (in millicores)',
    ['namespace', 'vpa_name', 'container']
)
mem_target_gauge = Gauge(
    'vpa_memory_target_bytes',
    'VPA recommended target memory for container (in bytes)',
    ['namespace', 'vpa_name', 'container']
)
mem_uncapped_gauge = Gauge(
    'vpa_memory_uncapped_target_bytes',
    'VPA uncapped target memory for container (in bytes)',
    ['namespace', 'vpa_name', 'container']
)

# Memory units for parsing strings like "500Mi"
MEMORY_UNITS = {
    'Ki': 1024,
    'Mi': 1024**2,
    'Gi': 1024**3,
    'Ti': 1024**4,
    'Pi': 1024**5,
    'Ei': 1024**6,
    'K': 1000,
    'M': 1000**2,
    'G': 1000**3,
    'T': 1000**4,
    'P': 1000**5,
    'E': 1000**6,
}

# Helpers to parse resource strings
def parse_cpu(cpu_val):
    if isinstance(cpu_val, (int, float)):
        return float(cpu_val) * 1000
    if isinstance(cpu_val, str):
        if cpu_val.endswith("m"):
            return float(cpu_val[:-1])
        try:
            return float(cpu_val) * 1000
        except ValueError:
            return 0.0
    return 0.0

def parse_memory(mem_val):
    if isinstance(mem_val, (int, float)):
        return float(mem_val)
    if isinstance(mem_val, str):
        match = re.match(r'^([0-9.]+)([a-zA-Z]*)$', mem_val)
        if match:
            number, unit = match.groups()
            factor = MEMORY_UNITS.get(unit, 1)
            try:
                return float(number) * factor
            except ValueError:
                return 0.0
    return 0.0

def update_metrics():
    try:
        crds = api.list_cluster_custom_object(
            group="autoscaling.k8s.io",   # Update to your CRD group
            version="v1",
            plural="verticalpodautoscalers"  # Update to your CRD plural
        )

        # Clear previous values
        cpu_target_gauge.clear()
        cpu_uncapped_gauge.clear()
        mem_target_gauge.clear()
        mem_uncapped_gauge.clear()

        for item in crds.get('items', []):
            meta = item.get('metadata', {})
            ns = meta.get('namespace', 'default')
            name = meta.get('name', 'unknown')

            containers = (
                item.get('status', {})
                    .get('recommendation', {})
                    .get('containerRecommendations', [])
            )

            for container in containers:
                cname = container.get('containerName', 'unknown')

                # CPU - target
                cpu_target = container.get('target', {}).get('cpu')
                cpu_target_val = parse_cpu(cpu_target)
                cpu_target_gauge.labels(namespace=ns, vpa_name=name, container=cname).set(cpu_target_val)
                logging.info(f"[{ns}/{name}] container={cname} target.cpu={cpu_target_val} millicores")

                # CPU - uncapped
                cpu_uncapped = container.get('uncappedTarget', {}).get('cpu')
                cpu_uncapped_val = parse_cpu(cpu_uncapped)
                cpu_uncapped_gauge.labels(namespace=ns, vpa_name=name, container=cname).set(cpu_uncapped_val)
                logging.info(f"[{ns}/{name}] container={cname} uncapped.cpu={cpu_uncapped_val} millicores")

                # Memory - target
                mem_target = container.get('target', {}).get('memory')
                mem_target_val = parse_memory(mem_target)
                mem_target_gauge.labels(namespace=ns, vpa_name=name, container=cname).set(mem_target_val)
                logging.info(f"[{ns}/{name}] container={cname} target.memory={mem_target_val} bytes")

                # Memory - uncapped
                mem_uncapped = container.get('uncappedTarget', {}).get('memory')
                mem_uncapped_val = parse_memory(mem_uncapped)
                mem_uncapped_gauge.labels(namespace=ns, vpa_name=name, container=cname).set(mem_uncapped_val)
                logging.info(f"[{ns}/{name}] container={cname} uncapped.memory={mem_uncapped_val} bytes")

    except Exception as e:
        logging.exception("Failed to update metrics")

if __name__ == "__main__":
    logging.info("Starting VPA metrics exporter on :8080/metrics")
    start_http_server(8080)
    while True:
        update_metrics()
        time.sleep(30)

