# Pod configuration and Scaling

## Parallelism (jobs)

You use parallelism to specify the maximum number of tasks that can run in parallel. By default, tasks will be started as quickly as possible, up to a maximum that varies depending on how many CPUs you are using.

Lowering parallelism limits how many tasks run in parallel. This is useful in cases where one of your backing resources, such as a database, has limited scaling and cannot handle a large number of parallel requests.

```
apiVersion: run.googleapis.com/v1
kind: Job
metadata:
  name: JOB_NAME
spec:
  template:
    spec:
      parallelism: PARALLELISM
      template:
        spec:
          containers:
          - image: IMAGE
```

## Restrictions on GKE AutoPilot mode

- Memory to CPU ratio should be atleast 1:1 (range 1-6.5). Charged for lot of memory but we use very little (1000 jobs ~ < 1GB memory)

- Max 400 nodes (can be extended upon request) ~ 12,800 pods. Other regional limits might be applicable

- API rate limiting 3000 requests / 100 secs (not going to surpass this) but good to keep in mind when scaled infinitely

- Other limit set by compute engine quotas such as CPU but can be extended

- 10 Gi max ephemeral storage

## Current limits

- 5 Gi max ephemeral storage (parallel upload to google buckets) ~ Pods fail when output exceeds the limit
- Pipe and split output into files of few Gb and then upload
- Efficient zip libraries to compress output, if available
- Use Surge -m splitting option
    Criteria to split into n chunks??
    Additional advantage is to be able to use multi cores on the pod (currently a single job uses single core) - needs to be implemented as a wrapper to Surge at the moment (worker.py)
- Validation of the output files
