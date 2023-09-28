# Pod configuration and Scaling

## Requirements

- Memory to CPU ratio should be atleast 1:1 (range 1-6.5). Charged for lot of memory but we use very little (1000 jobs ~ < 1GB memory)

- Max 400 nodes (can be extended upon request) ~ 12,800 pods. Other regional limits might be applicable

- API rate limiting 3000 requests / 100 secs (not going to surpass this) but good to keep in mind when scaled infinitely

- Other limit set by compute engine quotas such as CPU but can be extended

- 10 Gi max ephemeral storage (more after a few slides)

## Current limits and potential fix

10 Gi max ephemeral storage (more after a few slides)
Pods fail when output exceeds the limit

Pipe and split output into files of few Gb and then upload (going to be just a work around)
Efficient zip libraries to compress output, if available
Use Surge -m splitting option
Criteria to split into n chunks?? (more later)
Additional advantage is to be able to use multi cores on the pod (currently a single job uses single core) - needs to be implemented as a wrapper to Surge at the moment (worker.py)
Validation of the output files?
Large files
Explore db dumps for efficient search and filtering
MySQL is known to handle few billion entries

