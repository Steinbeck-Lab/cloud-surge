# Local Development (minikube)

Minikube is a tool that allows you to run a single-node Kubernetes cluster on your local machine for development and testing purposes. Here are the steps to install Minikube:

### Minikube Installation Steps:

1. Install Minikube: You can download and install Minikube from the official GitHub repository or use a package manager. Here, I'll provide instructions for downloading it directly:

- Linux: 

```
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

- macOS:

```
brew install minikube
```

- Windows:

Download the Windows installer from the Minikube releases page on GitHub (https://github.com/kubernetes/minikube/releases) and follow the installation instructions.

2. Start Minikube:

Open a terminal window and start Minikube with the following command:
```
minikube start
```

3. Check Minikube Status
```
minikube status
```

4. Use Minikube:

Now that Minikube is running, you can use kubectl to interact with your local Kubernetes cluster. For example, you can run:

```
kubectl get nodes
```

5. Stop Minikube:
When you're done working with your local cluster, you can stop Minikube with:

```
minikube stop
```
This will shut down the virtual machine and the Kubernetes cluster.

### Build docker image

```
docker build --no-cache -t <docker_image>:<tag> .

# Push image to docker hub
docker push <docker_image>:<tag>
```

Image pull policy

```
- name: cloud-surge
    image:  <docker_image>:<tag>
    imagePullPolicy: Always
- name: cheminformatics-microservice
    image: nfdi4chem/cheminformatics-microservice:lite
    imagePullPolicy: Always
```

### Start Redis app and expose the service

```
kubectl apply -f ./ops/redis/redis-pod.yaml
# pod/redis-master created

kubectl apply -f ./ops/redis/redis-service.yaml
# service/redis created / service/redis unchanged

kubectl port-forward redis-master 6379:6379
# Forwarding from 127.0.0.1:6379 -> 6379
# Forwarding from [::1]:6379 -> 6379
```

*In a new terminal*

```
kubectl get pods
NAME           READY   STATUS    RESTARTS   AGE
redis-master   1/1     Running   0          95s
```

### Load tasks to the redis queue

```
% cd ops

% python launchpad.py --stats
Pending Tasks Count: 0
Processing Tasks Count: 0

# load 9HA
% python launchpad.py --mfs=./../resources/formulae/9.txt
Loading tasks from input: ./../resources/formulae/9.txt
Tasks Session ID: ab0d38f4-c18b-476b-9883-0dccb81af630
Pending Tasks Count: 36977
Processing Tasks Count: 0

% python launchpad.py --stats                            
Pending Tasks Count: 36977
Processing Tasks Count: 0

# delete tasks
% python launchpad.py --delete
Pending Tasks Count: 0
Processing Tasks Count: 0

# load 7HA
% python launchpad.py --mfs=./../resources/formulae/7.txt
Loading tasks from input: ./../resources/formulae/7.txt
Tasks Session ID: bc050f70-1a23-4b8c-aeaf-9c4b382b8726
Pending Tasks Count: 9660
Processing Tasks Count: 0

# session stats
% python launchpad.py --session=bc050f70-1a23-4b8c-aeaf-9c4b382b8726
Session id:bc050f70-1a23-4b8c-aeaf-9c4b382b8726
Pending mfs:9660
Completed mfs:0
Failed mfs:0
Lease / processing mfs:0
```
### Apply secrets to upload files to google bucket

```
% kubectl apply -f ./secrets.yaml.example
```

### Launch Jobs

```
% kubectl apply -f ./job.local.yaml
job.batch/surge-job-wq created

% kubectl get pods                 
NAME                 READY   STATUS    RESTARTS   AGE
redis-master         1/1     Running   0          15m
surge-job-wq-8gh96   1/1     Running   0          34s

% python launchpad.py --stats
Pending Tasks Count: 3556
Processing Tasks Count: 1

% python launchpad.py --stats
Pending Tasks Count: 0
Processing Tasks Count: 0

% kubectl get pods           
NAME                 READY   STATUS      RESTARTS   AGE
redis-master         1/1     Running     0          36m
surge-job-wq-jvn6s   0/1     Completed   0          60s

% kubectl get pods
NAME           READY   STATUS    RESTARTS   AGE
redis-master   1/1     Running   0          37m
```

### Export Session - tasks stats

```
python launchpad.py --mfs=./../resources/formulae/7.txt --session=fd82b265-2e2e-41b3-a670-3a52a032dd35 --export
```

Generates

ops/logs/e18f9f54-579f-4374-a490-8ce4cc550141.csv file with runtimes and other stats

ops/logs/failed-e18f9f54-579f-4374-a490-8ce4cc550141.txt file with failed molecular formulae

### Download files from remote google cloud buckets

Install gsutils from here  - https://cloud.google.com/storage/docs/gsutil_install

```
gsutil -m cp -r "gs://<bucket_name>/<session_id>/" .
```

### Loginto the container 

```
kubectl exec --stdin --tty surge-job-wq-<id> -c cloud-surge -- /bin/bash
kubectl exec --stdin --tty surge-job-wq-<id> -c cheminformatics-microservice -- /bin/bash
```

### Check logs

```
kubectl logs surge-job-wq-<id> -c cloud-surge
kubectl logs surge-job-wq-<id> -c cheminformatics-microservice
```

### Delete Tasks

```
kubectl delete jobs `kubectl get jobs -o custom-columns=:.metadata.name`
```

### Debugging-

*Get all images*

```
kubectl get pods --all-namespaces -o jsonpath="{.items[*].spec.containers[*].image}" |\
tr -s '[[:space:]]' '\n' |\
sort |\
uniq -c
```

*Get all images*

```
kubectl get pods --all-namespaces -o jsonpath="{.items[*].spec.containers[*].image}" |\
tr -s '[[:space:]]' '\n' |\
sort |\
uniq -c
```

*Debug pod*
```
kubectl run -i --tty temp --image nfdi4chem/cloud-surge:v1.0.0-beta --command "/bin/sh"

kubectl delete pod/temp
```

*Debug job*
```
kubectl exec --stdin --tty surge-job-wq-kftlf -- /bin/bash

kubectl describe jobs/surge-job-wq
```