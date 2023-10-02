import redis
import uuid
import argparse
import json

parser = argparse.ArgumentParser(
    description="Load tasks to Cloud Surge  \
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
    help="Delete pending tasks",
)
parser.add_argument(
    "--export",
    default=False,
    action=argparse.BooleanOptionalAction,
    help="Export session stats",
)
parser.add_argument(
    "--stats",
    default=True,
    action=argparse.BooleanOptionalAction,
    help="Display all tasks statistics",
)
parser.add_argument("--session", type=str, help="Display the tasks statistics")
args = parser.parse_args()
r = redis.Redis(host="127.0.0.1", port=6379, password="")


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i: i + n]


if args.mfs:
    if args.export:
        if args.session:
            parsedKeys = []
            exportSessionId = str(args.session)
            sessionOutputFile = open("logs/" + exportSessionId + ".csv", "a+")
            with args.mfs as input_file:
                lines = input_file.readlines()
                nkey = exportSessionId
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
                            sessionOutputFile.write(",".join(list(mObj.values())) + "\n")
                            # r.delete(key)
                            parsedKeys.append(nkey)
                        else:
                            print(mfd)
                    # print(len(parsedKeys))
                sessionOutputFile.close()
                for key in r.scan_iter("*"):
                    r.delete(key)
                mf = []
                for line in lines:
                    mf.append(line.rstrip())
                outMf = []
                with open("logs/" + exportSessionId + ".csv") as f:
                    lines = f.readlines()
                    for line in lines:
                        imf = line.rstrip().split(",")[0]
                        outMf.append(imf)
                failedMF = list(set(outMf).symmetric_difference(set(mf)))
                tasksFailedOutputFile = open("logs/failed-" + exportSessionId + ".txt", "a+")
                for fmf in failedMF:
                    tasksFailedOutputFile.write(fmf + "\n")
    else:
        session_id = uuid.uuid4()
        print("Loading tasks from input: %s" % args.mfs.name)
        print("Tasks Session ID: %s" % session_id)
        mf = []
        with args.mfs as input_file:
            lines = input_file.readlines()
            for line in lines:
                mf.append(line.rstrip() + "_" + str(session_id))
        totalTasks = len(mf)
        r.lpush("surge_tasks", *mf)

if args.delete:
    r.delete("surge_tasks")

if args.session:
    sessionId = args.session
    print("Session id:" + str(sessionId))
    pendingTasks = r.lrange("surge_tasks", 0, -1)
    pendingTasksCount = len(pendingTasks)
    print("Pending mfs:" + str(pendingTasksCount))
    completedTasks = r.lrange(sessionId + ":completed", 0, -1)
    completedTasksCount = len(completedTasks)
    print("Completed mfs:" + str(completedTasksCount))
    failedTasks = r.lrange(sessionId + ":failed", 0, -1)
    failedTasksCount = len(failedTasks)
    print("Failed mfs:" + str(failedTasksCount))
    processingTasksCount = completedTasksCount + failedTasksCount
    +pendingTasksCount
    print("Lease / processing mfs:" + str(processingTasksCount))
else:
    if args.stats:
        pendingTasks = r.lrange("surge_tasks", 0, -1)
        pendingTasksCount = len(pendingTasks)
        print("Pending Tasks Count: %s" % pendingTasksCount)
        processingTasks = r.lrange("surge_tasks:processing", 0, -1)
        processingTasksCount = len(processingTasks)
        print("Processing Tasks Count: " + str(processingTasksCount))
