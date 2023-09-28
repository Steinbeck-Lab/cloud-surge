import redis
import uuid
import argparse
import json

parser = argparse.ArgumentParser(
    description="Load jobs to Cloud Surge  \
     Redis Queue"
)
parser.add_argument(
    "--mfs",
    type=argparse.FileType("r", encoding="UTF-8"),
    help="Molecular Formulae list file",
)
parser.add_argument(
    "--delete",
    default=False,
    action=argparse.BooleanOptionalAction,
    help="Delete pending jobs",
)
parser.add_argument(
    "--export",
    default=False,
    action=argparse.BooleanOptionalAction,
    help="Export job stats",
)
parser.add_argument(
    "--stats",
    default=True,
    action=argparse.BooleanOptionalAction,
    help="Display all jobs statistics",
)
parser.add_argument("--job", type=str, help="Display the Job Statistics")
args = parser.parse_args()
r = redis.Redis(host="127.0.0.1", port=6379, password="")


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


if args.mfs:
    if args.export:
        if args.job:
            parsedKeys = []
            exportJobId = str(args.job)
            jobOutputFile = open("logs/" + exportJobId + ".csv", "a+")
            with args.mfs as input_file:
                lines = input_file.readlines()
                nkey = exportJobId
                for mfs in chunks(lines, 500):
                    smfs = []
                    for mf in mfs:
                        if mf not in parsedKeys:
                            smfs.append(nkey + ":" + mf.rstrip())
                    mfdata = r.mget(smfs)
                    for mfd in mfdata:
                        mObj = {}
                        if mfd:
                            value = json.loads(mfd.decode("utf-8"))
                            sout = (
                                value["stdErr"]
                                .rstrip()
                                .replace("\n", "|")
                                .replace("\r", "|")
                            )
                            mObj["mf"] = sout.split("  ")[0]
                            mObj["s_totalStructuresCount"] = sout.split(" ")[-4]
                            mObj["totalStructuresCount"] = str(
                                value["totalStructuresCount"]
                            )
                            mObj["oFileSize"] = str(value["oFileSize"])
                            mObj["runtime"] = value["runtime"]
                            mObj["s_runtime"] = sout.split(" ")[-2]
                            mObj["start"] = value["start"]
                            mObj["end"] = value["end"]
                            mObj["stdOut"] = sout
                            mObj["stdErr"] = (
                                value["stdOut"]
                                .rstrip()
                                .replace("\n", "|")
                                .replace("\r", "|")
                            )
                            jobOutputFile.write(",".join(list(mObj.values())) + "\n")
                            # r.delete(key)
                            parsedKeys.append(nkey)
                        else:
                            print(mfd)
                    # print(len(parsedKeys))
                jobOutputFile.close()
                for key in r.scan_iter("*"):
                    r.delete(key)
                mf = []
                with args.mfs as input_file:
                    lines = input_file.readlines()
                    for line in lines:
                        mf.append(line.rstrip())
                outMf = []
                with open("logs/" + exportJobId + ".csv") as f:
                    lines = f.readlines()
                    for line in lines:
                        imf = line.rstrip().split(",")[0]
                        outMf.append(imf)
                failedMF = list(set(outMf).symmetric_difference(set(mf)))
                jobFailedOutputFile = open("logs/failed-" + exportJobId + ".txt", "a+")
                for fmf in failedMF:
                    jobFailedOutputFile.write(fmf + "\n")
    else:
        job_id = uuid.uuid4()
        print("Loading jobs from input: %s" % args.mfs.name)
        print("Jobs Session ID: %s" % job_id)
        mf = []
        with args.mfs as input_file:
            lines = input_file.readlines()
            for line in lines:
                mf.append(line.rstrip() + "_" + str(job_id))
        totalJobs = len(mf)
        r.lpush("surge_jobs", *mf)

if args.delete:
    r.delete("surge_jobs")

if args.job:
    jobId = args.job
    print("Job id:" + str(jobId))
    pendingJobs = r.lrange("surge_jobs", 0, -1)
    pendingJobsCount = len(pendingJobs)
    print("Pending mfs:" + str(pendingJobsCount))
    completedJobs = r.lrange(jobId + ":completed", 0, -1)
    completedJobsCount = len(completedJobs)
    print("Completed mfs:" + str(completedJobsCount))
    failedJobs = r.lrange(jobId + ":failed", 0, -1)
    failedJobsCount = len(failedJobs)
    print("Failed mfs:" + str(failedJobsCount))
    processingJobsCount = completedJobsCount + failedJobsCount
    +pendingJobsCount
    print("Lease / processing mfs:" + str(processingJobsCount))
else:
    if args.stats:
        pendingJobs = r.lrange("surge_jobs", 0, -1)
        pendingJobsCount = len(pendingJobs)
        print("Pending Jobs Count: %s" % pendingJobsCount)
        processingJobs = r.lrange("surge_jobs:processing", 0, -1)
        processingJobsCount = len(processingJobs)
        print("Processing Jobs Count: " + str(processingJobsCount))
