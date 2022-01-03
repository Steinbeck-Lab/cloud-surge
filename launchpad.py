import redis
import os
import uuid
from google.cloud import storage
import json

r = redis.Redis(
    host='127.0.0.1',
    port=6379,
    password='')

job_id = uuid.uuid4()
# r.delete('surge_jobs')
# print(job_id)

mf = []
with open("./formulae/formulaeMax10HA.txt") as f:
    lines = f.readlines()
    for line in lines:
        mf.append(line.rstrip() + "_" + str(job_id))

totalJobs = len(mf)
# r.lpush('surge_jobs', *mf)

# pendingJobs = r.lrange('surge_jobs', 0, -1)
# print(len(pendingJobs))

jobId = "3b5f8ea1-9c2e-4a9c-9a28-c717b72dcbf8"
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

# Export output
# parsedKeys=[]
# exportJobId = str('c74df038-d62e-40ff-af2c-b2f47cbf50a2')
# r.delete(exportJobId + ':failed')
# r.delete(exportJobId + ':completed')
# jobOutputFile = open("logs/" + exportJobId + '.txt',"a+")
# for key in r.scan_iter(exportJobId + ":*"):
#     nmap = key.decode("utf-8").rsplit(':', 1)
#     nkey = nmap[0]
#     mf = nmap[1]
#     if nmap not in parsedKeys and '.' not in nkey :
#         mObj = {}
#         value = json.loads(r.get(key).decode("utf-8"))
#         mObj['mf'] = mf
#         mObj['start'] = value['start']
#         mObj['end'] = value['end']
#         mObj['stdOut'] = value['stdOut'].rstrip().replace("/n", "|")
#         mObj['stdErr'] = value['stdErr'].rstrip().replace("/n", "|")
#         mObj['uploadStart'] = value['uploadStart']
#         mObj['uploadEnd'] = value['uploadEnd']
#         jobOutputFile.write(",".join(list(mObj.values()))+'\n')
#         r.delete(key)
#         parsedKeys.append(nkey)
#         print(len(parsedKeys))
# delete parsed keys
# jobOutputFile.close()


# Delete all keys
# for key in r.scan_iter("*"):
#     print(r.delete(key))