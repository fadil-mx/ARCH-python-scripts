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
    cmd = f"rsync {source} {destination} {flags}  "
    return run_cmd(cmd)


def choose_with_fzf():
    cmd = f'ls "{SYNC}" | fzf -m'
    result = subprocess.getoutput(cmd)
    # print(result)
    if not result:
        print("❌ No file selected.")
        exit(1)
    return [os.path.join(SYNC, r) for r in result.split("\n")]


def main():
    if run_cmd("ssh an ls") != 0:
        print("SSH connection failed. Please check your SSH configuration.")
        exit(1)

    print("\n🔄 Dry run: Local → Remote")
    selected_files_local = choose_with_fzf()
    for file in selected_files_local:
        sync(file, REMOTE, dry=True)
    option = input("Do you want to proceed with this sync? (y/n): ").lower()
    if option == "y":
        for file in selected_files_local:
            sync(file, REMOTE, dry=False)
    else:
        exit(0)

    print("\n🔄 Dry run: Remote → Local")
    option = input("Do you want to sync files from remote to local? (y/n): ").lower()
    if option != "y":
        exit(0)
    selected_files_local_remote = choose_with_fzf()
    for file in selected_files_local_remote:
        sync(file, REMOTE, dry=True)
    option = input("Do you want to proceed with this sync? (y/n): ").lower()
    if option == "y":
        for file in selected_files_local_remote:
            sync(file, REMOTE, dry=False)
    else:
        exit(0)


if __name__ == "__main__":
    main()
