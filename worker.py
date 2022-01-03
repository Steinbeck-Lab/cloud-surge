#!/usr/bin/env python
import time
import rediswq
import os
from subprocess import Popen, PIPE
from google.cloud import storage
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

host="redis"
bucket_name = 'steinbeck-surge-results'

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    os.remove(source_file_name)
    # print(
    #     "File {} uploaded to {}.".format(
    #         source_file_name, destination_blob_name
    #     )
    # )

q = rediswq.RedisWQ(name="surge_jobs", host=host, port=6379, password='')
# print("Worker with sessionID: " +  q.sessionID())
# print("Initial queue state: empty=" + str(q.empty()))
while not q.empty():
  item = q.lease(lease_secs=10, block=True, timeout=2) 
  if item is not None:
    itemstr = item.decode("utf-8")
    values =  itemstr.split("_")
    job = values[1]
    mf = values[0]
    q._db.set(job + ':' + mf + ':' + 'start', str(datetime.now()))
    process = Popen(['surge', '-o'+mf+".smiles.gz", '-z', '-S',  mf], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    q._db.set(job + ':' + mf + ':' + 'stdout', stdout)
    q._db.set(job + ':' + mf + ':' + 'stderr', stderr)
    if process.returncode != 0: 
        q._db.lpush(job + ':' + 'failed', mf)
        q.complete(item)
    else:
        q._db.set(job + ':' + mf + ':' + 'end', str(datetime.now()))
        q._db.lpush(job + ':' + 'completed', mf)
        upload_blob(bucket_name, mf+".smiles.gz", job + "/" + mf+".smiles.gz" )
        q.complete(item)