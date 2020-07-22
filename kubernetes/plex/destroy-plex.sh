helm uninstall plex --namespace plex
kubectl delete pvc pvc-k8s-plex-data -n plex
kubectl delete pvc pvc-k8s-plex-transcode -n plex
kubectl delete pvc pvc-k8s-plex-config -n plex