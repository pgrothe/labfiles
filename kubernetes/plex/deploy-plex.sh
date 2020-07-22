kubectl create -f /mnt/c/lab/kubernetes/plex/pvc-k8s-plex-data.yaml -n plex
kubectl create -f /mnt/c/lab/kubernetes/plex/pvc-k8s-plex-transcode.yaml -n plex
kubectl create -f /mnt/c/lab/kubernetes/plex/pvc-k8s-plex-config.yaml -n plex
helm install plex /mnt/c/lab/helm/charts/kube-plex \
    --namespace plex \
    --set ingress.enabled=true