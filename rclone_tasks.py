#!/usr/bin/python
import json
from os.path import realpath,exists,expanduser,expandvars
from argparse import ArgumentParser,RawDescriptionHelpFormatter
from subprocess import Popen,PIPE,TimeoutExpired
from time import sleep
import shlex
from tkinter.constants import FALSE

def get_tasks(config_file):
    return json.load(config_file)
    pass

def get_path(source):
    is_cloud_provider = ":" in source
    if(not is_cloud_provider):
        source = expanduser(source)
        source = expandvars(source)
    return source
    pass

def filter_active_tasks(tasks):
    active_tasks = []
    for task in tasks:
        has_enabled  = "enabled" in task
        enabled      = has_enabled and task['enabled'] == True
        if enabled:
            active_tasks.append(task)
    return active_tasks


def process_tasks(tasks,execute,max_spawn_processes):
    commands    = []
    processes   = []
    active_tasks = filter_active_tasks(tasks)
    for task in active_tasks:
        source       = get_path(task['source'])
        destinations = task['destination']
        command      = task['command']

        for i in range(0,len(destinations)):
            args         = []
            destination = get_path(destinations[i])
            args.append(source)
            args.append(destination)
            if 'args' in task:
                args = args + task['args']

            if exists(source):
                source = realpath(source)

            binary = ['/usr/bin/rclone']
            cmd = []
            cmd = binary + [command] + args
            cmd = " ".join(cmd)
            if execute:
                print("Running: %s\r" % cmd)
                cmd = shlex.split(cmd)
                commands.append({"args":cmd})
            else:
                print("%s" % cmd)

            if(len(destinations) - 1 == i):
                print("\r")

    for command in commands:
        process = Popen(args=command['args'],stdout=PIPE,stdin=PIPE,stderr=PIPE,universal_newlines=True,text=True)
        processes.append(process)
        while True:
            process_running = 0
            process_ended   = 0
            process_queued  = 0
            for process in processes:
                try:
                    stdout,stderr = process.communicate(timeout=1)
                    process_ended += 1
                except TimeoutExpired:
                    process_running += 1

            if process_running > max_spawn_processes:
                continue

            process_queued = len(commands) - (process_running + process_ended)

            print("Running: %d, Ended: %s, Queued: %s\r" % (process_running,process_ended,process_queued))
            break
    processes_with_error = wait_processes(processes)
    if len(processes_with_error) > 0:
        for process_with_error in processes_with_error:
            process_stdout,process_stderr = process_with_error.communicate()
            print("""
                Command:  %s
                Exit:     %s
                Stdout:   %s
                Stderr:   %s
                ------------
                """ %
                (" ".join(process_with_error.args),
                    process_with_error.returncode,
                    process_stdout,
                    process_stderr
                )
            )

    pass


def wait_processes(processes):
    processes_with_error = []
    for process in processes:
        exit_code = process.wait()
        if exit_code != 0:
            processes_with_error.append(process)

    return processes_with_error

def main():
    parser = ArgumentParser(prog='rclone_tasks',
        formatter_class=RawDescriptionHelpFormatter,
        description='Program to sync multiple folder at once')
    parser.add_argument('-f','--filename',help="file with definition files to sync")
    parser.add_argument('-n','--dry-run',help="print command instead of execute them",action="store_true")
    parser.add_argument('-p','--processes',help='max concurrent running processes',default=4,type=int)
    args  = parser.parse_args()


    if(args.filename == None):
        parser.print_help()

    if(args.filename):
        config_file = open(realpath(args.filename),'r')

        tasks = get_tasks(config_file)
        execute = not args.dry_run
        process_tasks(tasks,execute,args.processes)
        config_file.close()
    pass

main()
