# VPA Tracker Reports via Slack

In this section we will use the alert manager to send a periodic report via a slack channel
of the maximum CPU recommendation from the VPA object for our sample workload.

```bash
% kubectl get alertmanager -n monitoring        
NAME                                 VERSION   REPLICAS   READY   RECONCILED   AVAILABLE   AGE
kube-prometheus-stack-alertmanager   v0.28.1   1          1       True         True        7d6h
```

## Create Alerts

vpa-weekly.rules.yaml: 

- This will be scanned by Prometheus
- This stores a recording rule
- The interval of 168hours corresponds to 7 days

selvik@Selvis-MacBook-Pro vpa-alerts % kubectl apply -f  vpa-weekly.rules.yaml
prometheusrule.monitoring.coreos.com/vpa-weekly configured

```bash
% kubectl apply -f vpa-weekly-alert.rules.yaml
prometheusrule.monitoring.coreos.com/vpa-weekly-alert created
```

Check that the rule exists here:
```bash
http://localhost:9090/rules?page=4
```

```bash
% kubectl get alertmanagerconfig -n monitoring        
NAME               AGE
vpa-slack-notify   136m
```




## View alerts via the Alertmanager UI

```bash
% kubectl port-forward svc/kube-prometheus-stack-alertmanager -n monitoring 9093

URL: http://localhost:9093/#/alerts



