import redis
import os
import uuid
from google.cloud import storage
import json

r = redis.Redis(
    host='127.0.0.1',
    port=6379,
    password='')

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# r.delete('surge_jobs')

job_id = uuid.uuid4()
# print(job_id)

mf = []
with open("./formulae/formulaeMax12HA.txt") as f:
    lines = f.readlines()
    for line in lines:
        mf.append(line.rstrip() + "_" + str(job_id))

totalJobs = len(mf)
# r.lpush('surge_jobs', *mf)

# pendingJobs = r.lrange('surge_jobs', 0, -1)
# print(len(pendingJobs))

jobId = "b44c4a6d-bbaf-43e7-b23c-27ecdd6284b4"
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
processingJobsCount = totalJobs - (completedJobsCount + failedJobsCount + pendingJobsCount)
print("Lease / processing mfs:" + str(processingJobsCount))

# # Export output
# parsedKeys=[]
# exportJobId = str('b27dc908-a5a3-4333-bfc9-c1a56e2d443c')
# r.delete(exportJobId + ':failed')
# r.delete(exportJobId + ':completed')
# jobOutputFile = open("logs/" + exportJobId + '.csv',"a+")
# with open("./formulae/formulaeMax12HA.txt") as f:
#     lines = f.readlines()
#     nkey = exportJobId
#     for mfs in chunks(lines, 500):
#         smfs = []
#         for mf in mfs:
#             if mf not in parsedKeys:
#                 smfs.append(nkey + ":" + mf.rstrip())
#         mfdata = r.mget(smfs)
#         for mfd in mfdata:
#             mObj = {}
#             if mfd:
#                 value = json.loads(mfd.decode("utf-8"))
#                 sout = value['stdErr'].rstrip().replace('\n', '|').replace('\r', '|')
#                 mObj['mf'] = sout.split("  ")[0]
#                 mObj['start'] = value['start']
#                 mObj['end'] = value['end']
#                 mObj['stdOut'] = value['stdOut'].rstrip().replace('\n', '|').replace('\r', '|')
#                 mObj['stdErr'] = sout
#                 mObj['uploadStart'] = value['uploadStart']
#                 mObj['uploadEnd'] = value['uploadEnd']
#                 mObj['oFileSize'] = str(value['oFileSize'])
#                 jobOutputFile.write(",".join(list(mObj.values()))+'\n')
#                 # r.delete(key)
#                 parsedKeys.append(nkey)
#             else:
#                 print(mfd)
#         print(len(parsedKeys))
# # delete parsed keys
# jobOutputFile.close()

# Delete all keys
# for key in r.scan_iter("*"):
#     print(r.delete(key))