import redis
import uuid

r = redis.Redis(
    host='127.0.0.1',
    port=6379,
    password='')

job_id = uuid.uuid4()

mf = []
with open("./resources/formulae/14.txt") as f:
    lines = f.readlines()
    for line in lines:
        mf.append(line.rstrip() + "_" + str(job_id))

totalJobs = len(mf)
r.lpush('surge_jobs', *mf)