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

# save the run details to redis
# input file, start time

# r.delete('surge_jobs')

mf = []
with open("./formulae/formulaeMax5HA.txt") as f:
    lines = f.readlines()
    for line in lines:
        # print(line.rstrip())
        mf.append(line.rstrip() + "_" + str(job_id))

# r.lpush('surge_jobs', *mf)
print(r.lrange('surge_jobs', 0, 10))