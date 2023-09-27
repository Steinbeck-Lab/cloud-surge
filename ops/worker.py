#!/usr/bin/env python
import time
import rediswq
import os
from subprocess import Popen, PIPE
from google.cloud import storage
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import threading
import zipfile

host = "redis"
bucket_name = "steinbeck-surge-results"


def upload_blob(bucket_name, source_file_name, destination_blob_name, job):
    storage_client = storage.Client()
    # uploadStart = getTimeStamp()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    os.remove(source_file_name)
    # uploadEnd = getTimeStamp()
    # q._db.set(job + ':' + source_file_name, getJSONString({
    #   'uploadTime' : str(uploadStart - uploadEnd)
    # }))


def upload_blob_parallel(bucket_name, source_file_name, job):
    destination_blob_name = job + "/" + source_file_name
    thread = threading.Thread(
        target=upload_blob,
        args=(bucket_name, source_file_name, destination_blob_name, job),
    )
    thread.start()
    # uncomment to upload sequentially
    # thread.join()


def getTimeStamp():
    return datetime.now()


def getJobLog(runtime, oFileSize, totalStructuresCount, start, end, stdOut, stdErr):
    job = {
        "runtime": str(runtime.total_seconds()),
        "stdOut": stdOut.decode("utf-8"),
        "stdErr": stdErr.decode("utf-8"),
        "oFileSize": oFileSize,
        "start": start.strftime("%m/%d/%Y %H:%M:%S"),
        "end": end.strftime("%m/%d/%Y %H:%M:%S"),
        "totalStructuresCount": totalStructuresCount,
    }
    return getJSONString(job)


def getJSONString(job):
    return json.dumps(job)


q = rediswq.RedisWQ(name="surge_jobs", host=host, port=6379, password="")
print("Worker with sessionID: " + q.sessionID())
print("Initial queue state: empty=" + str(q.empty()))
retries = 0
while not q.empty():
    item = q.lease(lease_secs=10, block=True, timeout=2)
    if item is not None:
        itemstr = item.decode("utf-8")
        values = itemstr.split("_")
        job = values[1]
        mf = values[0]
        start = getTimeStamp()
        # Run surge with filters
        process = Popen(
            ["surge", "-P", "-T", "-B1,2,3,4,5,7,9", "-t0", "-f0", "-S", mf],
            stdout=PIPE,
            stderr=PIPE,
        )
        # Run surge with out any filters
        # process = Popen(['surge', '-S',  mf], stdout=PIPE, stderr=PIPE)
        i = 0
        smilesData = []
        totalCompressedFileSize = 0
        totalStructuresCount = 0
        currentIterCount = 0
        for line in iter(process.stdout.readline, b""):
            if currentIterCount < 10000000:
                smilesData.append(line.decode("utf-8").rstrip())
                currentIterCount += 1
            else:
                smilesData.append(line.decode("utf-8").rstrip())
                currentIterCount += 1
                ofile = mf + "_" + str(i)
                zf = zipfile.ZipFile(
                    ofile + ".zip", mode="w", compression=zipfile.ZIP_DEFLATED
                )
                zf.writestr(ofile + ".smi", "\n".join(smilesData))
                zf.close()
                totalCompressedFileSize += os.stat(ofile + ".zip").st_size
                i += 1
                smilesData = []
                totalStructuresCount += currentIterCount
                currentIterCount = 0
                upload_blob_parallel(bucket_name, ofile + ".zip", job)
        remainingSmilesLength = len(smilesData)
        if remainingSmilesLength > 0:
            totalStructuresCount += remainingSmilesLength
            ofile = mf + "_" + str(i)
            zf = zipfile.ZipFile(
                ofile + ".zip", mode="w", compression=zipfile.ZIP_DEFLATED
            )
            zf.writestr(ofile + ".smi", "\n".join(smilesData))
            zf.close()
            totalCompressedFileSize += os.stat(ofile + ".zip").st_size
            i += 1
            smilesData = []
            upload_blob_parallel(bucket_name, ofile + ".zip", job)
        filesCount = i + 1
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            end = getTimeStamp()
            q._db.set(
                job + ":" + mf,
                getJobLog(end - start, "None", "None", start, end, stdout, stderr),
            )
            q._db.lpush(job + ":" + "failed", mf)
            q.complete(item)
        else:
            end = getTimeStamp()
            q._db.set(
                job + ":" + mf,
                getJobLog(
                    end - start,
                    totalCompressedFileSize,
                    totalStructuresCount,
                    start,
                    end,
                    stdout,
                    stderr,
                ),
            )
            q._db.lpush(job + ":" + "completed", mf)
            q.complete(item)
    else:
        if retries > 10:
            break
        else:
            retries += 1
print("Queue empty, exiting")
