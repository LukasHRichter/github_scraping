import datetime
import json
import logging as log
import pprint
import re
import os
from time import sleep

import pip._vendor.requests as requests

TOKEN = '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'
CONTAINS_DOLLAR = re.compile('^\$')
# singleReq = 1, multiReq = 0
result = {  
    'license': 1,
    # 'community/profile': 1,
    # 'stats/code_frequency': 1,
    # 'stats/commit_activity': 1,
    # 'stats/contributors': 1,
    # 'stats/participation': 1,
    # 'stats/punch_card': 1,
    # 'import/authors': 1,
    # 'import/large_files': 1,
    # 'languages': 1,
    # 'readme': 1,
    # 'releases/latest': 1,
    # 'stargazers': 0,
    # 'subscribers': 0,
    # 'deployments': 0,
    # 'assignees': 0,
    # 'issues/comments': 0,
    # 'issues/events': 0,
    # 'labels': 0,
    # 'milestones': 0,
    # 'pulls/comments': 0,
    # 'contributors': 0,
    # 'forks': 0,
    # 'tags': 0,
    # 'pulls': 0,
    # 'issues': 0,
    'branches': 0,
    'branches/$name': 0,
    # 'commits': 0,
    # 'comments': 0,
}

def get_all_requests_from_repo(REPO_ID):
    
    def get_data(endpoint, headers = {'Authorization': f'Bearer {TOKEN}'}, params = { 'page':1, 'per_page': 100, 'state':'all' }, singleReq=False):
        nonlocal reqsLeft
        reqsLeft -= 1
        if reqsLeft < 25:
            sleep(get_rate_limit_reset())
            reqsLeft = get_rate_limit()['remaining']

        _params = params.copy()
        resp = requests.get(f'http://api.github.com/repositories/{REPO_ID}/{endpoint}', headers=headers, params=_params).json()
        if bool(resp) and not singleReq:
            _params['page'] += 1
            resp += get_data(endpoint=endpoint, headers=headers, params=_params, singleReq=singleReq)
        return resp

    def get_rate_limit():
        response = requests.get(f'http://api.github.com/rate_limit', headers={'Authorization': f'Bearer {TOKEN}'})
        return response.json()['rate']

    def get_rate_limit_reset():
        currentTime = datetime.datetime.now().timestamp()
        resetTime = get_rate_limit()['reset']
        sleepTime = int(resetTime - currentTime)
        log.info(f'sleep for {sleepTime}')
        return sleepTime

    def get_all_data(endpoints, endpointName = ''):
        def get_variable_endpoints(path, var):
            parent = endpoints[path[0]]
            _path = '/'.join(path)
            res = {}
            for child in parent:
                sub = child[var[1:len(var)]]
                res[_path.replace(var, sub)] = 1
            return res

        _endpointName = endpointName
        VAR_ENDPOINT = bool(_endpointName)
        result[_endpointName] = []

        for endpoint in endpoints:
            if not VAR_ENDPOINT: _endpointName = endpoint
            if not _endpointName: 
                log.info(f'skipping empty endpoint')
                continue
            path = endpoint.split('/')
            ids = [p for p in path if re.match(CONTAINS_DOLLAR, p)]
            if len(ids) > 0:
                paths = get_variable_endpoints(path=path, var=ids[0])
                get_all_data(endpoints=paths, endpointName=_endpointName)
            
            else:

                if not os.path.exists(f'./data_handling/debug'):
                    os.mkdir(f'./data_handling/debug')
                if not os.path.exists(f'./data_handling/debug/{REPO_ID}'):
                    os.mkdir(f'./data_handling/debug/{REPO_ID}')
                temp = endpoint.replace('/', '-')
                json.dump(get_data(endpoint=endpoint, singleReq=endpoints[endpoint]), open(f'./data_handling/debug/{REPO_ID}/{temp}.json','w'),indent=4,sort_keys=True)

                if VAR_ENDPOINT: 
                    result[_endpointName].append(get_data(endpoint=endpoint, singleReq=endpoints[endpoint]))
                else:
                    if (bool(endpoint)):
                        result[_endpointName] = get_data(endpoint=endpoint, singleReq=endpoints[endpoint])
    
    reqsLeft = get_rate_limit()['remaining']
    log.info(f'starting requests for repo {REPO_ID} with {reqsLeft} requests left')
    get_all_data(result)
    #list working requests with Per_page Limit:


    # #list problem requests with per page:
    # get_request("actions/artifacts") #- (kein leeres [])
    # get_request("actions/cache/usage") #- (kein leeres [])
    # get_request("actions/runs") #- (kein leeres [])
    # get_request("actions/workflows") #- (kein leeres [])
    # get_request("events") #In order to keep the API fast for everyone, pagination is limited for this resource. Check the rel=last link relation in the Link response header to see how far back you can traverse.
    # get_request("notifications") #nf not found
    # get_request("environments") #- (kein leeres [])
    # get_request("projects")  #- (kein leeres [])
    # get_request("releases") #"Only the first 1000 results are available."
    # get_request("topics") #"names": []


    # #list working with {}
    # run_id = get_ids_with_second_param("actions/runs", "workflow_runs", "id")
    # get_request_at_end("actions/runs", run_id, "jobs")
    # get_request_at_end("actions/runs", run_id, "approvals")
    # get_request_at_end("actions/runs", run_id, "pending_deployments")
    # get_request_at_end("actions/runs", run_id, "timing")

    # branch_id = get_ids("branches", "name")
    # get_request_at_end("branches", branch_id, "protection") #nf
    # get_request_at_end("branches", branch_id, "protection/enforce_admins") #nf
    # get_request_at_end("branches", branch_id, "protection/required_pull_request_reviews") #nf
    # get_request_at_end("branches", branch_id, "protection/required_signatures") #nf
    # get_request_at_end("branches", branch_id, "protection/required_status_checks") #nf
    # get_request_at_end("branches", branch_id, "protection/required_status_checks/contexts") #nf
    # get_request_at_end("branches", branch_id, "protection/restrictions") #nf
    # get_request_at_end("branches", branch_id, "protection/restrictions/apps") #nf
    # get_request_at_end("branches", branch_id, "protection/restrictions/teams") #nf
    # get_request_at_end("branches", branch_id, "protection/restrictions/users") #nf

    # # issue_number = get_ids("issues", "number")
    # # get_request_at_end("issues", issue_number, "comments")
    # # get_request_at_end("issues", issue_number, "events")
    # # get_request_at_end("issues", issue_number, "labels")
    # # get_request_at_end("issues", issue_number, "timeline")
    # # get_request_at_end("issues", issue_number, "reactions")
    # # get_request_at_end("issues", issue_number, "reactions")
    # # issues_comments_id = get_ids("issues/comments", "id")
    # # get_request_at_end("issues/comments", issues_comments_id, "reactions")

    # # pull_number = get_ids("pulls", "number")
    # # get_request_at_end("pulls", pull_number, "commits")
    # # get_request_at_end("pulls", pull_number, "files")
    # # get_request_at_end("pulls", pull_number, "comments")
    # # get_request_at_end("pulls", pull_number, "requested_reviewers")
    # # get_request_at_end("pulls", pull_number, "reviews")
    # # pulls_comments_id = get_ids("pulls/comments", "id")
    # # get_request_at_end("pulls/comments", pulls_comments_id, "reactions")

    # deployment_id = get_ids("deployments", "id")
    # get_request_at_end("deployments", deployment_id, "statuses")

    # milestone_number = get_ids("milestones", "number")
    # get_request_at_end("milestones", milestone_number, "labels")

    # comment_id = get_ids("comments", "id")
    # get_request_at_end("comments", comment_id, "reactions")

    # release_id = get_ids("releases", "id")
    # get_request_at_end("releases", release_id, "reactions")
    # get_request_at_end("releases", release_id, "assets")

    # workflow_id = get_ids_with_second_param("actions/workflows", "workflows", "id")
    # get_request_at_end("actions/workflows", workflow_id, "runs")
    # get_request_at_end("actions/workflows", workflow_id, "timing")


    #errors/problems
    # environment_name = get_ids("environments", "name") #not sure about name #error, cause nothing in it
    # get_request_at_end("environments", environment_name, "deployment-branch-policies")


    # list requests with {} in it
    # get_request("actions/runs/{run_id}/attempts/{attempt_number}/jobs")
    # get_request("actions/runs/{run_id}/attempts/{attempt_number}")
    # get_request("actions/jobs/{job_id}")
    # get_request("check-runs/{check_run_id}")
    # get_request("check-runs/{check_run_id}/annotations")
    # get_request("check-suites/{check_suite_id}/check-runs")
    # get_request("check-suites/{check_suite_id}")
    # get_request("dependency-graph/compare/{basehead}")
    # get_request("keys/{key_id}") #nf
    # get_request("git/commits/{commit_sha}")
    # get_request("git/matching-refs/{ref}")
    # get_request("git/ref/{ref}")
    # get_request("git/trees/{tree_sha}")
    # get_request("reviews/{review_id}/comments")
    # get_request("releases/tags/{tag}")
    # get_request("releases/assets/{asset_id}")
    # get_request("contents/{path}") #?
    # get_request("hooks/{hook_id}/config")
    # get_request("hooks/{hook_id}/deliveries")


    #not found:
    # get_request("subscription") #Not Found??
    # get_request("keys") #"Not Found"
    # get_request("git/tags") #Not Found
    # get_request("import") #Not Found"
    # get_request("pages") #"Not Found"
    # get_request("pages/builds") #"Not Found"
    # get_request("pages/builds/latest") #"Not Found"
    # get_request("pages/health") #"Not Found"
    # get_request("codeowners/errors") #Not Found
    # get_request("dispatches") #Not Found
    # get_request("teams") #Not Found
    # get_request("vulnerability-alerts") #Not Found
    # get_request("autolinks") #Not Found
    # get_request("tags/protection") #Not Found
    # get_request("hooks") #Not Found



    #json.dump(data,open(json_name + 'try4.json','w'),indent=4,sort_keys=True)

    return result
    