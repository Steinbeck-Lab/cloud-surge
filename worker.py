#!/usr/bin/env python
import time
import rediswq
import os
from subprocess import Popen, PIPE
from google.cloud import storage
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json

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

def getTimeStamp():
    return str(datetime.now())

def getJobLog(start, end, stdOut, stdErr, uploadStart, uploadEnd, oFileSize):
    job = {
        'start': start,
        'end': end,
        'stdOut': stdOut.decode("utf-8"),
        'stdErr': stdErr.decode("utf-8"),
        'uploadStart': uploadStart,
        'uploadEnd': uploadEnd,
        'oFileSize': oFileSize
    }
    return getJSONString(job)

def getJSONString(job):
    return json.dumps(job)

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
    start = getTimeStamp()
    ofile = mf+".smiles.gz"
    process = Popen(['surge', '-o'+ofile, '-z', '-S',  mf], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0: 
        end =  getTimeStamp()
        q._db.set(job + ':' + mf, getJobLog(start, end, stdout, stderr, 'None', 'None', 'None'))
        q._db.lpush(job + ':' + 'failed', mf)
        q.complete(item)
    else:
        end =  getTimeStamp()
        oFileSize = os.stat(ofile).st_size
        uploadStart =  getTimeStamp()
        upload_blob(bucket_name, ofile, job + "/" + ofile )
        uploadEnd =  getTimeStamp()
        q._db.set(job + ':' + mf, getJobLog(start, end, stdout, stderr, uploadStart, uploadEnd, oFileSize))
        q._db.lpush(job + ':' + 'completed', mf)
        q.complete(item)