import datetime
import logging as log
import re
from time import sleep

import pip._vendor.requests as requests

TOKEN = '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'
CONTAINS_DOLLAR = re.compile('^\$')
# singleReq = 1, multiReq = 0
endpoints = {  
#all must be 1:
    '': 1, 
    '/license': 1, #ja
    '/community/profile': 1, #ja
    '/stats/code_frequency': 1, #ja
    '/stats/commit_activity': 1, #ja not comprehensive; sieht man für 1 Jahr zurückgehend wsl
    '/stats/contributors': 1, #ja 
    '/stats/participation': 1, #ja  
    '/stats/punch_card': 1, #ja geht eine Woche zurück
    '/languages': 1, #ja
    '/readme': 1, #ja
    '/topics': 1, #ja
    '/environments': 1, #ja
    '/projects': 1, #ja, mit vorbehalt
    '/actions/workflows': 1, #ja
    '/contents': 1, #ja
    '/labels': 0, #ja
    '/milestones': 0, #ja
    '/contributors': 0, #ja #liste von contributors mit liste von anzahl an contributions
    '/pulls': 0, #ja #funktioniert manchmal mit bad gateway #server error
    '/issues': 0, #ja
    '/branches': 0, #ja
    '/commits': 0, #ja
    '/comments': 0, #ja
    '/releases': 0, #ja  #Only the first 10000 results are available oder []???
}

def get_all_requests_from_repo(REPO_ID):
    '''
   scrape a given repositories
    @Params
    --------
    REPO_ID: int; repository id
    '''

    def get_rate_limit(time = False):
        '''
        get the remaining requests or the time till rate limit reset
        @Params
        --------
        time: bool; true if time till rate limit reset, else false
        '''
        response = requests.get(f'https://api.github.com/rate_limit', headers={'Authorization': f'Bearer {TOKEN}'}).json()
        if time:
            cTime = datetime.datetime.now().timestamp()
            rTime = response['rate']['reset']
            sTime = max(0, int(rTime - cTime)) + 60
            log.info(f'sleep for {sTime}')
            return sTime
        else:
            return response['rate']['remaining']

    def get_data(endpoint, single):
        '''
        get data for a specific endpoint
        @Params
        --------
        endpoint: str; the path of the endpoint
        single: bool; true, if the endpoint only gives a single Response, else false
        '''
        headers = {'Authorization': f'Bearer {TOKEN}'}
        params = { 'page':0, 'per_page': 100, 'state':'all' }

        ret = False
        nonlocal remaining
        exhausted = False
        while not exhausted:
            params['page'] += 1
            remaining -= 1
            if remaining <= 25:
                sleep(get_rate_limit(time=True))
                remaining = get_rate_limit()
                log.info(f'updating remaining request: {remaining}')

            if bool(single):
                exhausted = True

            response = requests.get(f'https://api.github.com/repositories/{REPO_ID}{endpoint}', headers=headers, params=params)

            if response.status_code == 200:
                resp = response.json()
                t = type(resp)

                if t == list:
                    if len(resp) == 0:
                        exhausted = True
                    else:
                        if not ret:
                            ret = []
                        ret = ret + resp

                if t == dict:
                    if len(resp) == 0:
                        exhausted = True
                    else:
                        if not ret:
                            ret = {}
                        ret = ret | resp

            else:
                exhausted = True
                log.info(f'{response.status_code} response for endpoint: {endpoint};{params}')
        
        return ret

    remaining = get_rate_limit()
    res = {}
    log.info(f'starting requests for repo {REPO_ID} with {remaining} requests left')
    for endpoint in endpoints:
        log.info(f'get endpoint {endpoint} for repo {REPO_ID}')
        res[endpoint] = get_data(endpoint=endpoint, single=endpoints[endpoint])

    return res

   
def getRepoWithStars(low, high):
    '''
    get all repos between a specific star count
    @Params
    --------
    low: int; minimum star count
    high: int; maximum star count
    '''
    res = []
    headers = {'Authorization': f'Bearer {TOKEN}'} 
    params = { 'page':1, 'per_page': 100, 'state':'all' }
    resp = requests.get(f'https://api.github.com/search/repositories?q=stars:{low}..{high}&sort=stars&order=desc', headers=headers, params=params).json()
    totalCount = resp['total_count']
    starBound = high
    log.info(f'found {totalCount} repos with {low}-{high} stars')
    log.debug(f'start fetching ids')
    for i in range(1, 11):
        log.debug(f'fetching ids {i*100 - 99}-{i*100}')
        params['page'] = i
        resp = requests.get(f'https://api.github.com/search/repositories?q=stars:{low}..{high}&sort=stars&order=desc', headers=headers, params=params).json()
        for repo in resp['items']:
            starBound = repo['stargazers_count']
            res.append(repo['id'])

    return (res, starBound)

def getMostStarredRepos(amount, minStars=100):
    '''
    get a certain amount of most starred repos
    @Params
    --------
    amount: int; amount of Repos
    minStars: int; minimum amount of stars needed
    '''
    starBound = 1000000 # More stars are not acceptable ;)
    used = requests.get(f'http://api.github.com/rate_limit', headers={'Authorization': f'Bearer {TOKEN}'}).json()['resources']['search']['used']
    while used > 0:
        log.info(f'Waiting for 10 minutes before getting repos >:(')
        sleep(600) # Sleep for 10 minutes (see: https://docs.github.com/en/rest/search)
        used = requests.get(f'http://api.github.com/rate_limit', headers={'Authorization': f'Bearer {TOKEN}'}).json()['resources']['search']['used']

    _res = []
    j = 0
    for i in range(0, round(amount/1000)):
        if j == 3:
            j = 0
            log.info(f'Waiting for 10 minutes to continue getting repos')
            sleep(600) # Sleep for 10 minutes (see: https://docs.github.com/en/rest/search)
        j += 1
        (res, starBound) = getRepoWithStars(low=minStars, high=starBound)
        _res = _res + res


    log.info(f'Acquired all repo ids')
    return _res

