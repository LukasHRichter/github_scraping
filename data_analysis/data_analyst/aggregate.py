from pymongo import MongoClient
import math
import re
from datetime import datetime

#Connecting to GitHubScraping
client = MongoClient("mongodb://root:hbX1AoLSjhdnznc@db:27017")
ghs = client["GitHubScraping"]
scraping = ghs["repos"]

agg = client['Aggregation']
agg_db = agg['data']


RE_SEC = re.compile('cwe|cve|cvss|security|secur|protection|vuln')
RE_TESTS = re.compile('test')
RE_DEP_BOTS = re.compile('dependabot|renovate')

def getRepoIds():
    return scraping.distinct('repo')

def getRepoData(repoIds):
    GET_REPO_DATA = [{"$match": {"repo": {'$in': repoIds}}}]
    results = list(scraping.aggregate(pipeline=GET_REPO_DATA))
    data = {}

    data['repos'] = []
    for repoId in repoIds:
        repoData = list(filter(lambda e: e['repo'] == repoId, results))
        data['repos'].append(aggregateRepoData(repoData))

    return data

def aggregateRepoData(repoData):
    data = {}
    combRepoData = {}
    for endpoints in repoData:
        endpoint = list(endpoints)[2]
        if endpoint == '': 
            combRepoData['data'] = list(endpoints.values())[2]
        else:
            combRepoData[endpoint] = [*combRepoData.get(endpoint, []), *list(endpoints[endpoint])]
   
    aggAmbientData(combRepoData.get('data', [''])[0], data)

    aggCodeFreq(combRepoData.get('/stats/code_frequency', [''])[0], data)

    aggCommitFreq(combRepoData.get('/stats/commit_activity', [''])[0], data)

    aggActions(combRepoData.get('/actions/workflows', [''])[0], data)

    aggContents(combRepoData.get('/contents', [''])[0], data)

    aggContributors(combRepoData.get('/contributors', [''])[0], data)

    aggPulls(combRepoData.get('/pulls', [''])[0], data)

    aggIssues(combRepoData.get('/issues', [''])[0], data)

    return data


def aggAmbientData(repoData, data):
    data['id'] = repoData['id'] #id
    data['name'] = repoData['name'] #name
    data['isFork'] = int(repoData['fork']) #isFork
    data['isArchived'] = int(repoData['archived']) #archived
    data['lang'] = repoData['language'] #languages
    data['amountForks'] = repoData['forks_count'] #forks
    data['size'] = repoData['size'] #size
    data['stars'] = repoData['stargazers_count'] #stars

def aggCodeFreq(repoData, data):
    avg = 0
    if type(repoData) is list:
        for freq in repoData:
            avg += freq[1]
            avg -= freq[2]

        avg = avg / len(repoData)

    if avg != 0:
        data['codeFreq'] = avg #avg weekly lines changed


def aggCommitFreq(repoData, data):
    avg = 0
    if type(repoData) is list:
        for freq in repoData:
            avg += freq['total']

        avg = avg / len(repoData)

    if avg != 0:
        data['commitFreq'] = avg #avg weekly commits

    
def aggActions(repoData, data):
    if type(repoData) is list:
        data['usesActions'] = int(repoData['total_count'] > 0)

    
def aggContents(repoData, data):
    tests = 0
    if type(repoData) is list:
        for content in repoData:
            if tests == 0:
                tests = int(type(RE_TESTS.match(content.get('name', ''))) != None)

    data['usesTests'] = tests


def aggContributors(repoData, data):
    amountContribtors = 0
    if type(repoData) is list:
        amountContribtors = len(repoData)
        
    data['amountContribtors'] = amountContribtors

def aggIssues(repoData, data):
    amountIssue = 0
    sec_amountIssue = 0

    avg = 0
    sec_avg = 0

    ttf = 0
    amountFixed = 0

    sec_ttf = 0
    sec_amountFixed = 0
    if type(repoData) is list:
        for issue in repoData:
            cr_date = issue['created_at']
            cl_date = issue['closed_at']
            if cr_date and cl_date:
                labels = issue.get('labels', [])
                if checkForSecLabels(labels):
                    sec_ttf += (datetime.strptime(cl_date, '%Y-%m-%dT%H:%M:%SZ') - datetime.strptime(cr_date, '%Y-%m-%dT%H:%M:%SZ')).total_seconds()
                    sec_amountFixed += 1
                    sec_amountIssue += 1

                amountIssue += 1
                amountFixed += 1
                ttf += (datetime.strptime(cl_date, '%Y-%m-%dT%H:%M:%SZ') - datetime.strptime(cr_date, '%Y-%m-%dT%H:%M:%SZ')).total_seconds()

    if amountFixed > 0:
        avg = ttf / amountFixed

    if sec_amountFixed > 0:
        sec_avg = sec_ttf / sec_amountFixed
            
    data['ttf'] = avg
    if sec_avg != 0:
        data['sec_ttf'] = sec_avg
        if avg != 0:
            data['sec_ttf/ttf'] = sec_avg / avg

    #data['amountIssues'] = amountIssue
    #data['amountSecIssues'] = sec_amountIssue

def checkForSecLabels(labels):
    for label in labels:
        name = label.get('name', '')
        if RE_SEC.match(name) is not None:
            return True
    return False

def aggPulls(repoData, data):
    amountPulls = 0
    dep_amountPulls = 0
    sec_amountPulls = 0

    avg = 0
    dep_avg = 0
    sec_avg = 0

    avg_reviewers = 0
    reviewers = 0

    ttm = 0
    amountMerged = 0

    dep_ttm = 0
    dep_amountMerged = 0

    sec_ttm = 0
    sec_amountMerged = 0

    botpull = False
    if type(repoData) is list:
        for pull in repoData:
            amountPulls += 1
            reviewers += len(pull.get('requested_reviewers', []))
            cr_date = pull['created_at']
            m_date = pull['merged_at']
            ## check for more bot (renovate, ...)
            if RE_DEP_BOTS.match(pull['user']['login']):
                botupll = True
                dep_amountPulls += 1
                sec_amountPulls += 1
                if m_date:
                    dep_ttm  += (datetime.strptime(m_date, '%Y-%m-%dT%H:%M:%SZ') - datetime.strptime(cr_date, '%Y-%m-%dT%H:%M:%SZ')).total_seconds() 
                    dep_amountMerged += 1
                    sec_ttm  += (datetime.strptime(m_date, '%Y-%m-%dT%H:%M:%SZ') - datetime.strptime(cr_date, '%Y-%m-%dT%H:%M:%SZ')).total_seconds() 
                    sec_amountMerged += 1

            check = ''
            title = pull.get('title', '')
            if type(title) != None:
                check += str(title)
                
            body = pull.get('body', '')
            if type(body) != None:
                check += str(body)

            isSec = RE_SEC.match(check)
            if isSec and not botpull:
                sec_amountPulls += 1
            if m_date:
                ttm  += (datetime.strptime(m_date, '%Y-%m-%dT%H:%M:%SZ') - datetime.strptime(cr_date, '%Y-%m-%dT%H:%M:%SZ')).total_seconds() 
                amountMerged += 1
                if isSec and not botpull:
                    sec_ttm  += (datetime.strptime(m_date, '%Y-%m-%dT%H:%M:%SZ') - datetime.strptime(cr_date, '%Y-%m-%dT%H:%M:%SZ')).total_seconds() 
                    sec_amountMerged += 1

    if amountPulls > 0:
        avg_reviewers = reviewers / amountPulls
        data['reviewers'] = avg_reviewers

    if amountMerged > 0:
        avg = ttm / amountMerged

    if dep_amountMerged > 0:
        dep_avg = dep_ttm / dep_amountMerged

    if sec_amountMerged > 0:
        sec_avg = sec_ttm / sec_amountMerged

            
    if avg != 0:
        data['ttm'] = avg
    if dep_avg != 0:
        data['dep_ttm'] = dep_avg
    if sec_avg != 0:
        data['sec_ttm'] = sec_avg
        if avg != 0:
            data['sec_ttm/ttm'] = sec_avg / avg

    if amountPulls > 0:
        data['merge_rate'] = amountMerged / amountPulls

    if dep_amountPulls > 0:
        data['dependabot'] = 1
        data['dep_merge_rate'] = dep_amountMerged / dep_amountPulls
    else:
        data['dependabot'] = 0

    if sec_amountPulls > 0:
        data['sec_merge_rate'] = sec_amountMerged / sec_amountPulls
        if data['merge_rate'] > 0:
            data['sec_merge_rate/merge_rate'] =  data['sec_merge_rate'] / data['merge_rate']


repoIds = getRepoIds()
repo_count = len(repoIds)
for i in range(0, math.ceil(repo_count/10)):
    repos = repoIds[i*10:(i+1)*10]
    data = getRepoData(repos)
    agg_db.insert_one(data)
