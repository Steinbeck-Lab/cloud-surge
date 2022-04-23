bucket: steinbeck-surge-results

```
gsutil -m cp -r "gs://steinbeck-surge-results/<jobid>/" .
gsutil -m cp -r "gs://steinbeck-surge-results/1dc6de65-37a1-496b-a993-63e3d1414bd8/" .
```

**Commands**

Redis:

App
```
kubectl apply -f ./redis/redis-pod.yaml
```
Service
```
kubectl apply -f ./redis/redis-service.yaml
```
Port forwarding to access from cloudshell
```
kubectl port-forward redis-master 6379:6379
```

Building the worker container and pushing the image to google artifact registry

```
docker build -t surge-peq .
docker tag surge-peq us-central1-docker.pkg.dev/steffen-nfdi-spielplatz/surge-peqi-repository/surge-peq
docker push us-central1-docker.pkg.dev/steffen-nfdi-spielplatz/surge-peqi-repository/surge-peq
```

```
docker build -t surge-peq-ss .
docker tag surge-peq-ss us-central1-docker.pkg.dev/steffen-nfdi-spielplatz/surge-peqi-repository/surge-peq-ss
docker push us-central1-docker.pkg.dev/steffen-nfdi-spielplatz/surge-peqi-repository/surge-peq-ss
```

```
kubectl run -i --tty temp --image us-central1-docker.pkg.dev/steffen-nfdi-spielplatz/surge-peqi-repository/surge-peq:latest --command "/bin/sh"
```

Miscellaneous commands

```
kubectl exec --stdin --tty surge-job-wq-kftlf -- /bin/bash

kubectl describe jobs/surge-job-wq

kubectl apply -f ./job.yaml

kubectl apply -f ./secrets.yaml

kubectl delete pod/temp

kubectl delete jobs `kubectl get jobs -o custom-columns=:.metadata.name`

kubectl get pods --all-namespaces | grep Evicted | awk '{print $2, "--namespace", $1}' | xargs kubectl delete pod

kubectl get svc --all-namespaces -o json | jq '.items[] | {name:.metadata.name, ns:.metadata.namespace, p:.spec.ports[] } | select( .p.nodePort != null ) | "\(.ns)/\(.name): localhost:\(.p.nodePort) -> \(.p.port) -> \(.p.targetPort)"'
```

**Links**

https://kubernetes.io/docs/reference/kubectl/cheatsheet/

https://github.com/StructureGenerator/surge

https://kubernetes.io/docs/tasks/job/fine-parallel-processing-work-queue/

https://github.com/sneumann/CloudSurge
