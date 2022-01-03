import redis
import os
import uuid
from google.cloud import storage

r = redis.Redis(
    host='127.0.0.1',
    port=6379,
    password='')

job_id = uuid.uuid4()
# print(job_id)

#  6834d916-3f9c-41b5-beda-6d4468f24685 - 6HA
#  98937c32-3dc5-4e89-aed0-0a318e3169b3 - 8HA

# r.delete('surge_jobs')

mf = []
with open("./formulae/formulaeMax8HA.txt") as f:
    lines = f.readlines()
    for line in lines:
        mf.append(line.rstrip() + "_" + str(job_id))

# ['C2H6_49b4ec2c-6431-42ea-975a-69033513e7fb','...]

totalJobs = len(mf)
# r.lpush('surge_jobs', *mf)

# pendingJobs = r.lrange('surge_jobs', 0, -1)
# print(pendingJobs)

jobId = "6834d916-3f9c-41b5-beda-6d4468f24685"
print("Job id:" + str(jobId))
pendingJobs = r.lrange('surge_jobs', 0, -1)
pendingJobsCount = len(pendingJobs)
print("Pending mfs:" + str(pendingJobsCount))
completedJobs = r.lrange(jobId + ':completed', 0, -1)
completedJobsCount = len(completedJobs)
print("Completed mfs:" + str(completedJobsCount))
failedJobs = r.lrange(jobId + ':failed', 0, -1)
# print(failedJobs)
failedJobsCount = len(failedJobs)
print("Failed mfs:" + str(failedJobsCount))
missingJobsCount = totalJobs - (completedJobsCount + failedJobsCount + pendingJobsCount)
print("Missing mfs:" + str(missingJobsCount))
# print(r.get((jobId+":C2Br2IH:stderr")))
# print(r.get('dbe40224-bb77-477b-a208-9a036d7f8544:'))
# print(r.lrange('surge_jobs', 0, -1))

# for key in r.scan_iter("*"):
#     print(key)