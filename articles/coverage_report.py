#!/usr/bin/env python
import os
import re
from confluence.client import Confluence
import json
import gitlab

creds = open(f"{os.environ['HOME']}/.confluence").read().rstrip().split(":")
code_coverage_page_id = 894861314
code_coverage_space_key = "DEVO"

token_file = open(f"{os.environ['HOME']}.gitlab.token")
gitlab_token = token_file.read().rstrip()
gl = gitlab.Gitlab("https://gitlab.com", private_token=gitlab_token)

c_client = Confluence('https://renovo.atlassian.net/wiki', (creds[0], creds[1]))
current_content = c_client.get_content_by_id(code_coverage_page_id, ['body.view', 'version.number'])

coverage_body = '<div class="table-wrap">' \
                '<table data-layout="default" class="confluenceTable">' \
                '<tbody>' \
                '<tr>' \
                '<th class="confluenceTh"><p><strong>project</strong></p></th>' \
                '<th class="confluenceTh"><p><strong>coverage</strong></p></th>' \
                '<th class="confluenceTh"><p /></th>' \
                '</tr>'

projects = [{
    'name': "data-services-management",
    'gitlab_id': "11622030"
}]

for project in projects:

    gl_project = gl.projects.get(project["gitlab_id"])
    jobs = gl_project.jobs.list()

    last_coverage_job_id = False

    for job in jobs:
        print(f"{job.id} - {job.name}")
        if job.name == "coverage":
            last_coverage_job_id = job.id
            break

    print(f"LastJobId: {last_coverage_job_id}")

    job_log = gl_project.jobs.get(last_coverage_job_id).trace()
    # print(job_log)
    for line in job_log.decode("utf-8").split("\n"):
        if re.match(r'^TOTAL', line):
            parts = line.split()
            print(parts)
            coverage_pct = parts[-1]

    coverage_body += '<tr>' \
                     f"<td class='confluenceTd'><p>{project['name']}</p></td>" \
                     f"<td class='confluenceTd'><p>{coverage_pct}</p></td>" \
                     f"<td class='confluenceTd'><p>-</p></td>" \
                     '</tr>'

coverage_body += '</tbody></table></div>'

c_client.update_content(
    content_id=current_content.id,
    new_content=coverage_body,
    new_version=current_content.version.number + 1,
    content_type=current_content.type,
    new_title=current_content.title)

