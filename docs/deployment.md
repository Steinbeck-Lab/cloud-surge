# Deployment configurations

## Redis deployment (yaml files)

### Pod configuration

```
apiVersion: v1
kind: Pod
metadata:
  name: redis-master
  labels:
    app: redis
spec:
  containers:
    - name: master
      image: redis
      env:
        - name: MASTER
          value: "true"
      ports:
        - containerPort: 6379
```

App

```
kubectl apply -f ./redis-pod.yaml
```

### Service configuration

```
apiVersion: v1
kind: Service
metadata:
  name: redis
spec:
  ports:
    - port: 6379
      targetPort: 6379
  selector:
    app: redis
```


Service

```
kubectl apply -f ./redis-service.yaml
```

Port forwarding to access from cloudshell

```
kubectl port-forward redis-master 6379:6379
```

## Jobs deployment

Building the worker container and pushing the image to google artifact registry

```
docker build -t surge-peq .
docker tag surge-peq us-central1-docker.pkg.dev/steffen-nfdi-spielplatz/surge-peqi-repository/surge-peq
docker push us-central1-docker.pkg.dev/steffen-nfdi-spielplatz/surge-peqi-repository/surge-peq
```

```
kubectl run -i --tty temp --image us-central1-docker.pkg.dev/steffen-nfdi-spielplatz/surge-peqi-repository/surge-peq:latest --command "/bin/sh"
```

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


```
kubectl apply -f ./job.yaml
```

```
kubectl apply -f ./secrets.yaml
```