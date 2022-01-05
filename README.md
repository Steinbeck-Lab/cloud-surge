Mapping:
```
4d10411e-6eb6-439a-9f03-1cb9ed3479bc : 6HA ~ 20
c74df038-d62e-40ff-af2c-b2f47cbf50a2 : 6HA (1CPU) ~ 20
a5f66062-95b0-4611-8b58-b6d005ce1700: 8HA ~ 20
4fef755a-8222-465b-94be-8b6a86e8bd4b: 8HA (1CPU) ~ 20
73440fb3-2846-45d7-abbd-8dfdb9f84a0f: 9HA ~ 20
90be208f-c7a3-4796-a414-4d4201747a30: 9HA (1CPU) ~ 20
47e42994-e03c-41aa-8d25-6a6aed513105: 10HA ~ 20
76d07192-f338-4397-b3b3-4de71d5711d6: 10HA (1CPU) ~ 20
3b5f8ea1-9c2e-4a9c-9a28-c717b72dcbf8: 10HA (1CPU) ~ 100
8cfa67bb-476f-4544-af77-11a252b13dff: 10HA (2CPU) ~ 100
1dc6de65-37a1-496b-a993-63e3d1414bd8: 11HA (1CPU) ~ 100 ~ 37mins
7acadc37-0a46-4d04-a999-f0c6eea0357e: 11HA (2CPU) ~ 100 ~ 27mins ??
a313c5f4-0b30-408b-945d-dd4b5a22a324: 12HA (1CPU) ~ 100 ~ failed (ephemeral storage limit reached 4g)
b27dc908-a5a3-4333-bfc9-c1a56e2d443c: 12HA (1CPU) ~ 100 ~ 16g es 
b44c4a6d-bbaf-43e7-b23c-27ecdd6284b4: 12HA (2CPU) ~ 100 ~ 16g es (199065)
```

outputfolder: logs (mf,start time, endtime, stdout, stderr, upload start, upload end, filesize)

bucket: steinbeck-surge-results

```
gsutil -m cp -r "gs://steinbeck-surge-results/<jobid>/" .
gsutil -m cp -r "gs://steinbeck-surge-results/1dc6de65-37a1-496b-a993-63e3d1414bd8/" .
```

Investigate
1) With the increase in number of jobs will the total time to generate structures increase or not (yes obviously)
2) With current GKE limitations whats the maximum jobs we can deploy
Any limitations because of our job deployment architecture
3) Memory footprint
4) CPU vs runtime
5) Upload times and % of the total runtime is upload time
6) Filesize vs HA or put it in another way total structures generated vs HA (valency dependence)
7) estimates of total run time for 14HA, 15HA, 16HA....
8) estimates of total ouput filesizes (compressed and total)
9) estimates of costs on GKE for 14HA, 15HA ....
10) cost savings on using committed compute 1year, 3years and zones based variation
11) Estimates of costs for storage
12) Final output for 14HA and host it publicly for anyone to download (cost estimates to do this for next few years)
13) Estimates for 18HA generation / filesizes / hosting


**Commands**

Redis:

App
kubectl apply -f ./redis/redis-pod.yaml

Service
kubectl apply -f ./redis/redis-service.yaml

kubectl port-forward redis-master 6379:6379

docker build -t surge-peq .

docker tag surge-peq us-central1-docker.pkg.dev/steffen-nfdi-spielplatz/surge-peqi-repository/surge-peq

docker push us-central1-docker.pkg.dev/steffen-nfdi-spielplatz/surge-peqi-repository/surge-peq

kubectl run -i --tty temp --image us-central1-docker.pkg.dev/steffen-nfdi-spielplatz/surge-peqi-repository/surge-peq:latest --command "/bin/sh"

kubectl exec --stdin --tty surge-job-wq-kftlf -- /bin/bash

kubectl describe jobs/surge-job-wq

kubectl apply -f ./job.yaml

kubectl apply -f ./secrets.yaml

kubectl delete pod/temp

kubectl delete jobs `kubectl get jobs -o custom-columns=:.metadata.name`

kubectl get pods --all-namespaces | grep Evicted | awk '{print $2, "--namespace", $1}' | xargs kubectl delete pod

kubectl get svc --all-namespaces -o json | jq '.items[] | {name:.metadata.name, ns:.metadata.namespace, p:.spec.ports[] } | select( .p.nodePort != null ) | "\(.ns)/\(.name): localhost:\(.p.nodePort) -> \(.p.port) -> \(.p.targetPort)"'

**Links**

https://kubernetes.io/docs/reference/kubectl/cheatsheet/

https://github.com/StructureGenerator/surge

https://kubernetes.io/docs/tasks/job/fine-parallel-processing-work-queue/

https://github.com/sneumann/CloudSurge