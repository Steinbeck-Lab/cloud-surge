# Deployment configurations

## **Start a storage service**

### Redis deployment (yaml files)

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

Apply this configuration to deploy the pod

```
kubectl apply -f ./ops/redis/redis-pod.yaml
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
kubectl apply -f ./ops/redis/redis-service.yaml
```

Port forwarding to access from cloudshell (Optional)

```
kubectl port-forward redis-master 6379:6379
```

Use the launchpad.py script to connect to Redis and then populate the queue with the tasks.

## Jobs deployment

Build the worker container and push the image to google artifact registry or docker hub

```
cd ./ops
docker build -t cloud-surge .
docker tag surge-peq us-central1-docker.pkg.dev/steffen-nfdi-spielplatz/surge-peqi-repository/surge-peq
docker push us-central1-docker.pkg.dev/steffen-nfdi-spielplatz/surge-peqi-repository/surge-peq
```

*Test if the pod is running*

```
kubectl run -i --tty temp --image us-central1-docker.pkg.dev/steffen-nfdi-spielplatz/surge-peqi-repository/surge-peq:latest --command "/bin/sh"
```

### Job yaml file

```
apiVersion: batch/v1
kind: Job
metadata:
  name: surge-job-wq-14ha
spec:
  ttlSecondsAfterFinished: 10
  parallelism: 400
  backoffLimit: 10
  template:
    metadata:
      name: surge-job-wq-14ha
    spec:
      containers:
      - name: c
        image: us-central1-docker.pkg.dev/steffen-nfdi-spielplatz/surge-peqi-repository/surge-peq
        resources:
          requests:
            ephemeral-storage: "5Gi"
            memory: 2048Mi
            cpu: 2000m
          limits:
            ephemeral-storage: "5Gi"
            memory: 2048Mi
            cpu: 2000m
        volumeMounts:
        - name: service-account-credentials-volume
          mountPath: /etc/gcp
          readOnly: true
        env:
        - name: GOOGLE_APPLICATION_CREDENTIALS
          value: /etc/gcp/sa_credentials.json
      volumes:
      - name: service-account-credentials-volume
        secret:
          secretName: surge-service-account-credentials
          items:
          - key: sa_json
            path: sa_credentials.json
      restartPolicy: OnFailure
```

```
kubectl apply -f ./job.yaml
```

```
kubectl apply -f ./secrets.yaml
```

*Helper Commands*

```
kubectl exec --stdin --tty surge-job-wq-kftlf -- /bin/bash

kubectl describe jobs/surge-job-wq

kubectl delete pod/temp

kubectl delete jobs `kubectl get jobs -o custom-columns=:.metadata.name`

kubectl get pods --all-namespaces | grep Evicted | awk '{print $2, "--namespace", $1}' | xargs kubectl delete pod

kubectl get svc --all-namespaces -o json | jq '.items[] | {name:.metadata.name, ns:.metadata.namespace, p:.spec.ports[] } | select( .p.nodePort != null ) | "\(.ns)/\(.name): localhost:\(.p.nodePort) -> \(.p.port) -> \(.p.targetPort)"'
```

**Links**

https://kubernetes.io/docs/reference/kubectl/cheatsheet/

https://github.com/StructureGenerator/surge

https://kubernetes.io/docs/tasks/job/fine-parallel-processing-work-queue/
