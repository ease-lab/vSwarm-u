#!/usr/bin/env python3
import os
import re
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("dir", type = str, help = "Results directory")
    return parser.parse_args()


def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))



args = parse_arguments()
subdirs = [s for s in os.listdir(args.dir) if os.path.isdir(args.dir + s)]
subdirs.sort()


rerun_cmds = [(True, "cd /users/dschall/vSwarm-u/benchmarks/wkdir")]
results = []


for subdir in subdirs[:]:
    filename = "{}/{}/gem5.log".format(args.dir,subdir)
    cmd = ""
    success = False

    if os.path.exists(filename):
        with open(filename) as f:
            # print(filename, "\n")
            start_tick = 0
            for line in f:
                if line[:14] == "command line: ":
                    cmd = line[14:].strip()
                # if "'fwait'" in line:
                #     print("{} stopped with 'fwait'".format(subdir))
                if "simulation done" in line:
                    success = True
                    break

            if success:
                print(f"{subdir} \033[92m succeed\033[00m")
            else:
                print(f"{subdir} \033[91m fail\033[00m")
            rerun_cmds += [(success, f"{cmd} > {filename} 2>&1 &")]
    # write the gRPC packet tick.


total = len(rerun_cmds) -1
with open("rerun.sh", "w") as f:
    for success,cmd in rerun_cmds:
        comment = "# " if success else ""
        f.write(f"{comment} sudo {cmd} \n")

