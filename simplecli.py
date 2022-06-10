#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import io
import sys
import argparse

sys.path.append("simpleMDMpy-magervalp")
import SimpleMDMpy
import os
import time


# Wrap the SimpleMDMpy class to avoid sprinkling api_key everywhere.

api_key = os.getenv("API_KEY")
if not api_key:
    raise RuntimeError("API_KEY environment variable not set")

class MDM:
    Devices = SimpleMDMpy.Devices(api_key)
    Scripts = SimpleMDMpy.Scripts(api_key)
    ScriptJobs = SimpleMDMpy.ScriptJobs(api_key)


import pprint


from color import Color

ANSI_ERASE_EOL = "\x1b[K"
def ansi_line_up(num_lines):
    return f"\x1b[{num_lines}F"


### List scripts

def print_script(script, print_source=False):
    attrs = script["attributes"]
    print(f"{Color.purple('ID:')} {script['id']} {Color.purple('Name:')} '{attrs['name']}'")
    print(f"{Color.blue('Created:')} {attrs['created_at']} {Color.blue('Updated:')} {attrs['updated_at']}")
    print(f"{Color.blue('Variable Support')} {Color.green('YES') if attrs['variable_support'] else Color.red('NO')}")
    if print_source:
        print(f"{Color.blue('Source:')}")
        print(attrs["content"], end="")
        if attrs["content"][-1] != "\n":
            print("")

def list_scripts(args):
    scripts = MDM.Scripts.get_script(args.id)
    if isinstance(scripts, list):
        for i, script in enumerate(scripts):
            if i > 0:
                print(f"{Color.red('---')}")
            print_script(script, args.print_source)
    else:
        print_script(scripts, args.print_source)
    return 0


### List jobs

def color_job_status(status):
    return {
        "pending": Color.cyan(status),
        "completed-with-errors": Color.red(status),
        "completed": Color.green(status),
        "cancelled": Color.yellow(status),
    }.get(status, status)

def color_device_status(status):
    return {
        "completed": Color.green(status),
        "pending": Color.cyan(status),
        "error": Color.red(status),
        "cancelled": Color.yellow(status),
    }.get(status, status)

def print_job(job, verbose=False, print_response=False, print_source=False):
    attrs = job["attributes"]
    print(f"{Color.purple('ID:')} {job['id']} {Color.purple('Job ID:')} '{attrs['job_id']}'")
    print(f"{Color.blue('Created by:')} {attrs['created_by']} {Color.blue('at')} {attrs['created_at']}")
    print(f"{Color.blue('Updated:')} {attrs['updated_at']}")
    print(f"{Color.blue('Script:')} {attrs['script_name']}")
    print(f"{Color.blue('Pending:')} {attrs['pending_count']} {Color.blue('Success:')} {attrs['success_count']} {Color.blue('Error:')} {attrs['errored_count']}")
    if verbose or print_response:
        for device in job["relationships"]["device"]["data"]:
            try:
                name = MDM.Devices.get_device(device["id"])["attributes"]["name"]
            except:
                name = Color.red("UNKNOWN")
            print("\t".join([
                str(device['id']),
                name,
                color_device_status(device['status']),
            ]))
        if print_response:
            print(f"{Color.blue('Response:')}")
            print(device["response"], end="")
            if device["response"][-1] != "\n":
                print("")
            print(f"{Color.blue('---')}")
    if print_source:
        print(f"{Color.blue('Variable Support')} {Color.green('YES') if attrs['variable_support'] else Color.red('NO')}")
        print(f"{Color.red('--- Source:')}")
        print(attrs["content"], end="")
        if attrs["content"][-1] != "\n":
            print("")
        print(f"{Color.red('---')}")

def list_jobs(args):
    jobs = MDM.ScriptJobs.get_job(args.id)
    if isinstance(jobs, list):
        for i, job in enumerate(jobs):
            if i > 0:
                print(f"{Color.red('---')}")
            print_job(job, args.verbose, args.print_response, args.print_source)
    else:
        print_job(jobs, args.verbose, args.print_response, args.print_source)
    return 0


### Upload a script

def create_script(args):
    try:
        with open(args.path, "rt", encoding="utf-8") as f:
            script_content = f.read()
    except Exception as e:
        print(f"Unable to read script: {e}", file=stderr)
        return os.EX_NOINPUT
    script = MDM.Scripts.create_script(args.name, args.variable_support, script_content)
    print_script(script)
    return 0


### Run a script on devices

def parse_device_list(arg):
    if not arg:
        return None
    ids = []
    for item in arg.split(","):
        try:
            ids.append(int(item))
        except ValueError:
            result = MDM.Devices.get_device(search=item)
            if len(result) == 1:
                ids.append(result[0]["id"])
            elif len(result) > 1:
                raise RuntimeError(f"Multiple devices found for '{item}'")
            else:
                raise RuntimeError(f"Unknown device '{item}'")
    return ids

def parse_id_list(arg):
    if not arg:
        return None
    ids = []
    for item in arg.split(","):
        try:
            ids.append(int(item))
        except ValueError:
            raise RuntimeError(f"Unknown id '{item}'")
    return ids

def create_job(args):
    if not any([args.devices, args.groups, args.assignment_groups]):
        print(f"Must provide either devices, groups, or assignment groups", file=stderr)
        return os.EX_USAGE
    device_ids = parse_device_list(args.devices)
    group_ids = parse_id_list(args.groups)
    assignment_group_ids = parse_id_list(args.assignment_groups)
    job = MDM.ScriptJobs.create_job(args.script_id, device_ids, group_ids, assignment_group_ids)
    if not args.wait:
        print_job(job)
    else:
        wait_job(job["id"])
    return 0


### Wait for job to finish

def wait_job(args):
    # If called from run -w args will just be the job id
    if isinstance(args, int):
        job_id = args
    else:
        job_id = int(args.id)
    while True:
        job = MDM.ScriptJobs.get_job(job_id)
        print_job(job)
        if job["attributes"]["status"] == "pending":
            time.sleep(5)
            for _ in range(5):
                print(f"{ansi_line_up(1)}{ANSI_ERASE_EOL}", end="")
            continue
        return 0


def main(argv):
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="command")

    p_listjobs = sp.add_parser("listjobs", aliases=["lj"], help="List jobs")
    p_listjobs.add_argument("--verbose", "-v", action="store_true")
    p_listjobs.add_argument("--print-response", "-r", action="store_true")
    p_listjobs.add_argument("--print-source", "-p", action="store_true")
    p_listjobs.add_argument("id", default="all", nargs="?")
    p_listjobs.set_defaults(func=list_jobs)
    
    p_listscripts = sp.add_parser("listscripts", aliases=["ls"], help="List scripts")
    p_listscripts.add_argument("--print-source", "-p", action="store_true")
    p_listscripts.add_argument("id", default="all", nargs="?")
    p_listscripts.set_defaults(func=list_scripts)
    
    p_upload = sp.add_parser("upload", help="Upload a script")
    p_upload.add_argument("name", help="The name of the script")
    p_upload.add_argument("--variable-support", "-v", action="store_true", help="Enable variable support")
    p_upload.add_argument("path", help="Path to a script to upload")
    p_upload.set_defaults(func=create_script)
    
    p_run = sp.add_parser("run", help="Run a script on devices")
    p_run.add_argument("--wait", "-w", action="store_true", help="Wait for job to finish")
    p_run.add_argument("script_id", type=int, help="Script ID")
    p_run.add_argument("--devices", "-d", help="Comma separated list of devices")
    p_run.add_argument("--groups", "-g", help="Comma separated list of groups")
    p_run.add_argument("--assignment-groups", "-a", help="Comma separated list of assignment groups")
    p_run.set_defaults(func=create_job)
    
    p_wait = sp.add_parser("wait", help="Wait for job to finish")
    p_wait.add_argument("id", help="ID")
    p_wait.set_defaults(func=wait_job)
    
    try:
        args = p.parse_args(argv[1:])
        return args.func(args) or 0
    except SimpleMDMpy.SimpleMDM.ApiError as e:
        print(f"Api call failed: {e}", file=sys.stderr)
        return os.EX_UNAVAILABLE
    except RuntimeError as e:
        print(f"{e}", file=sys.stderr)
        return os.EX_SOFTWARE

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

