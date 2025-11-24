#!/usr/bin/python
import json
from os.path import realpath,exists,expanduser,expandvars
from argparse import ArgumentParser,RawDescriptionHelpFormatter
from subprocess import Popen,PIPE
import shlex

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


def copy(tasks,execute):
    processes = []
    for task in tasks:
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
                print("Executando: %s\r" % " ".join(cmd))
                cmd = shlex.split(cmd)
                process = Popen(args=cmd,stdout=PIPE,stdin=PIPE,universal_newlines=True,text=True)
                processes.append(process)
            else:
                print("%s" % cmd)

            if(len(destinations) - 1 == i):
                print("\r")

    processes_with_error = wait_processes(processes)
    if len(processes_with_error) > 0:
        for process_with_error in processes_with_error:
            print("O Comando %s saiu com códido de erro: %d" % (process_with_error.args,process_with_error.returncode))
            print("Detalhes do erro: %s" % (process_with_error.errors))
        exit(1)

    pass


def process_tasks(tasks,execute):
    active_tasks = filter_active_tasks(tasks)
    copy(active_tasks,execute)


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
    args  = parser.parse_args()


    if(args.filename == None):
        parser.print_help()

    if(args.filename):
        config_file = open(realpath(args.filename),'r')

        tasks = get_tasks(config_file)
        execute = not args.dry_run
        process_tasks(tasks,execute)
        config_file.close()
    pass

main()
