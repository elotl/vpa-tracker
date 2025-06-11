kubectl patch alertmanager kube-prometheus-stack-alertmanager \
  -n monitoring \
  --type='merge' \
  -p '{
    "spec": {
      "alertmanagerConfigSelector": {
        "matchLabels": {
          "alertmanagerConfig": "enabled"
        }
      }
    }
  }'
