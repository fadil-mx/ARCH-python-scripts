#!/usr/bin/env python3
import os
import subprocess

SYNC = os.path.expanduser("~/Sync")
REMOTE = "an:/sdcard/Sync/"


def run_cmd(cmd):
    return subprocess.call(
        cmd,
        shell=True,
    )


def sync(source, destination, dry=True):
    if dry:
        flags = "-puavn "
    else:
        flags = "-puav "
    cmd = f"rsync {source} {destination} {flags}"
    return run_cmd(cmd)


def main():
    if run_cmd("ssh an ls") != 0:
        print("SSH connection failed. Please check your SSH configuration.")
        exit(1)

    print("\n🔄 Dry run: Local → Remote")
    sync(SYNC + "/", REMOTE, dry=True)
    option = input("Do you want to proceed with this sync? (y/n): ").lower()
    if option == "y":
        sync(SYNC + "/", REMOTE, dry=False)
    else:
        exit(0)

    print("\n🔄 Dry run: Remote → Local")
    sync(REMOTE, SYNC + "/", dry=True)
    option = input("Do you want to proceed with this sync? (y/n): ").lower()
    if option == "y":
        sync(REMOTE, SYNC + "/", dry=False)
    else:
        exit(0)


if __name__ == "__main__":
    main()
