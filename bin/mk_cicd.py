#!/usr/bin/env python

import yaml
import pprint
from jinja2 import Template
import subprocess

pp = pprint.PrettyPrinter(indent=4)

base_file = open("etc/gitlab-ci.yml")
base_yaml = yaml.safe_load(base_file.read())

app_file = open("etc/gitlab-app.yml")
tpl = Template(app_file.read())

def get_apps():
    return ["operations", "eks", "application"]


# Get list of workspaces from terraform call.
def get_workspaces(app_name):
    return ["production", "demo"]
    cmd = "cd aws/environments/{}; terraform workspace list".format(app_name)
    out = subprocess.getoutput(cmd)
    workspaces = []
    for line in out.split():
        if line == "*":
            continue
        workspaces.append(line.rstrip())
    return workspaces


for app_name in get_apps():
    workspaces = get_workspaces(app_name)

    for workspace_name in workspaces:
        cicd_app = yaml.safe_load(tpl.render(app_name=app_name, workspace_name=workspace_name))
        base_yaml.update(cicd_app)

cicd_file = open(".gitlab-ci.yml", "w")
yaml.dump(base_yaml, cicd_file)

print("Updated cicd config")
