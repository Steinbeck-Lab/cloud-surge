https://kubernetes.io/docs/reference/kubectl/cheatsheet/

https://github.com/StructureGenerator/surge

https://kubernetes.io/docs/tasks/job/fine-parallel-processing-work-queue/

docker build -t surge-peq .

docker tag surge-peq us-central1-docker.pkg.dev/steffen-nfdi-spielplatz/surge-peqi-repository/surge-peq

docker push us-central1-docker.pkg.dev/steffen-nfdi-spielplatz/surge-peqi-repository/surge-peq

kubectl exec --stdin --tty surge-job-wq-kftlf -- /bin/bash

kubectl describe jobs/surge-job-wq

kubectl apply -f ./job.yaml

kubectl apply -f ./secrets.yaml

kubectl delete pod/temp

kubectl port-forward redis-master 6379:6379

kubectl delete jobs `kubectl get jobs -o custom-columns=:.metadata.name`

https://github.com/sneumann/CloudSurge
