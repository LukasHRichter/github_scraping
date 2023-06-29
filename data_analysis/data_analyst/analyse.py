from pymongo import MongoClient
import pandas

#Connecting to GitHubScraping
client = MongoClient("mongodb://root:hbX1AoLSjhdnznc@db:27017")
agg = client['Aggregation']
agg_db = agg['data']


def getAggData():
    data = []
    for repos in agg_db.find():
        data.extend(list(repos['repos']))

    return data


def getAutomation():
    data = getAggData()
    df = pandas.DataFrame(data).drop(['name', 'lang','id', 'isFork', 'usesTests', 'isArchived', 'stars', 'codeFreq', 'dependabot', 'amountForks', 'size', 'ttf', 'sec_ttf', 'sec_merge_rate', 'merge_rate', 'sec_ttf/ttf','sec_merge_rate/merge_rate', 'sec_ttm/ttm' ,'commitFreq', 'amountContribtors', 'reviewers', 'dep_ttm', 'dep_merge_rate'], axis=1).groupby(['usesActions']).mean()
    return df

def getCorr():
    data = getAggData()
    cols = {'amountForks': 'amtForks', 'amountContribtors': 'amtContributors', 'merge_rate': 'mr', 'dep_merge_rate': 'dep_mr', 'sec_merge_rate': 'sec_mr', 'sec_merge_rate/merge_rate': 'sec_mr/mr'}
    df = pandas.DataFrame(data).drop(['id','isFork', 'usesTests', 'isArchived', 'amountForks', 'size', 'ttm', 'sec_ttm', 'sec_merge_rate', 'merge_rate', 'sec_ttf/ttf','sec_merge_rate/merge_rate', 'sec_ttm/ttm' ,'commitFreq', 'amountContribtors', 'reviewers', 'dep_ttm', 'dep_merge_rate'], axis=1).rename(columns=cols)
    return df

def getDep():
    data = getAggData()
    df = pandas.DataFrame(data).drop(['name', 'lang','id', 'isFork', 'usesTests', 'isArchived', 'stars', 'codeFreq', 'usesActions', 'amountForks', 'size', 'ttf', 'sec_ttf', 'sec_merge_rate', 'merge_rate', 'sec_ttf/ttf','sec_merge_rate/merge_rate', 'sec_ttm/ttm' ,'commitFreq', 'amountContribtors', 'reviewers', 'dep_ttm', 'dep_merge_rate'], axis=1).groupby(['dependabot']).mean()
    return df

def getReviewer():
    data = getAggData()
    df = pandas.DataFrame(data).drop(['name', 'lang','id', 'isFork', 'usesTests', 'isArchived', 'stars', 'codeFreq', 'usesActions', 'amountForks', 'dep_ttm', 'size', 'sec_ttf', 'ttf', 'sec_merge_rate', 'merge_rate', 'sec_ttf/ttf','sec_merge_rate/merge_rate', 'sec_ttm' ,'commitFreq', 'amountContribtors', 'dependabot', 'sec_ttm/ttm', 'dep_merge_rate'], axis=1)
    groups = []
    for i in range(1,8):
        groups.append(df.loc[(df['reviewers'] >= i*0.5) & (df['reviewers'] < i*0.5+1)]['sec_ttm'])
    return groups
