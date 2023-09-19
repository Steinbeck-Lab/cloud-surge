import redis
import os
import uuid
from google.cloud import storage
import json

r = redis.Redis(host="127.0.0.1", port=6379, password="")


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


# r.delete('surge_jobs')
# r.delete('surge_jobs:processing')

job_id = uuid.uuid4()
# job_id=""
print(job_id)

mf = []
with open("./resources/formulae/14.txt") as f:
    lines = f.readlines()
    for line in lines:
        mf.append(line.rstrip() + "_" + str(job_id))

totalJobs = len(mf)
# r.lpush('surge_jobs', *mf)

# pendingJobs = r.lrange('surge_jobs', 0, -1)
# pendingJobsCount = len(pendingJobs)
# print(pendingJobsCount)

# processingJobs = r.lrange('surge_jobs:processing', 0, -1)
# processingJobsCount = len(processingJobs)
# print("processing: " +str(processingJobsCount))
# # r.delete('surge_jobs:processing')

jobId = job_id
print("Job id:" + str(jobId))
pendingJobs = r.lrange("surge_jobs", 0, -1)
pendingJobsCount = len(pendingJobs)
print("Pending mfs:" + str(pendingJobsCount))
completedJobs = r.lrange(jobId + ":completed", 0, -1)
completedJobsCount = len(completedJobs)
print("Completed mfs:" + str(completedJobsCount))
failedJobs = r.lrange(jobId + ":failed", 0, -1)
# print(failedJobs)
failedJobsCount = len(failedJobs)
print("Failed mfs:" + str(failedJobsCount))
processingJobsCount = totalJobs - (
    completedJobsCount + failedJobsCount + pendingJobsCount
)
print("Lease / processing mfs:" + str(processingJobsCount))

# # # Export output
# parsedKeys=[]
# exportJobId = str(job_id)
# # r.delete(exportJobId + ':failed')
# # r.delete(exportJobId + ':completed')
# jobOutputFile = open("logs/" + exportJobId + '.csv',"a+")
# with open("./formulae/formulaeMax13HA.txt") as f:
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
#                 # print(value)
#                 sout = value['stdErr'].rstrip().replace('\n', '|').replace('\r', '|')
#                 mObj['mf'] = sout.split("  ")[0]
#                 mObj['s_totalStructuresCount'] = sout.split(" ")[-4]
#                 mObj['totalStructuresCount'] = str(value['totalStructuresCount'])
#                 mObj['oFileSize'] = str(value['oFileSize'])
#                 mObj['runtime'] = value['runtime']
#                 mObj['s_runtime'] = sout.split(" ")[-2]
#                 mObj['start'] = value['start']
#                 mObj['end'] = value['end']
#                 mObj['stdOut'] = sout
#                 mObj['stdErr'] = value['stdOut'].rstrip().replace('\n', '|').replace('\r', '|')
#                 jobOutputFile.write(",".join(list(mObj.values()))+'\n')
#                 # r.delete(key)
#                 parsedKeys.append(nkey)
#             else:
#                 print(mfd)
#         print(len(parsedKeys))
# # # delete parsed keys
# jobOutputFile.close()

# Delete all keys
# for key in r.scan_iter("*"):
#     print(r.delete(key))

# mf = []
# with open("./formulae/13HAonly.txt") as f:
#     lines = f.readlines()
#     for line in lines:
#         mf.append(line.rstrip())

# outMf = []
# with open("logs/" + exportJobId + '.csv') as f:
#     lines = f.readlines()
#     for line in lines:
#         imf = line.rstrip().split(",")[0]
#         outMf.append(imf)

# failedMF = list(set(outMf).symmetric_difference(set(mf)))

# print(len(mf) - len(outMf))
# print(len(failedMF))

# jobFailedOutputFile = open("formulae/" + exportJobId + '.txt',"a+")

# for fmf in failedMF:
#     jobFailedOutputFile.write(fmf+'\n')
