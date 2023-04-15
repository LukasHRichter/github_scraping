import logging as log
import pymongo
import pymongo.errors


#Database connection
URI="mongodb://root:hbX1AoLSjhdnznc@db:27017"

client = pymongo.MongoClient(URI)
print("Connection Successful")

db = client["GitHubScraping"]
collection = db["repos"]

def insertData(_repo, _data, _endpoint):
    '''
    insert data into the db for a single endpoint
    @Params
    --------
    _repo: int; repo id
    _data: dict; the data too save
    _endpoint: str; the endpoint path
    '''
    try:
        collection.insert_one({'repo': _repo, str(_endpoint): [_data]})
    except pymongo.errors.DocumentTooLarge:
        half = len(_data)//2
        _data1, _data2 = _data[:half], _data[half:]
        insertData(_repo=_repo, _data=_data1, _endpoint=_endpoint)
        insertData(_repo=_repo, _data=_data2, _endpoint=_endpoint)

def storeRepoData(repo, data):
    '''
    insert data into the db for all endpoint
    @Params
    --------
    repo: int; repo id
    data: dict; the data too save
    '''

    endpoints = [key for key in data]
    for endpoint in endpoints:
        if bool(collection.find_one({endpoint: {'$exists': 'true' }, 'repo': repo})):
            continue

        _data = data[endpoint]
        insertData(_repo=repo, _data=_data, _endpoint=endpoint)
        
def storeRepoIds(ids, amount, offset):
    '''
    insert repo ids into the db
    @Params
    --------
    ids: dict; the ids to save 
    amount: int; save a specific amount of ids
    offset: int; save the ids from a specifc offset on
    '''
    db_id = f'repoIds_{amount}_{offset}'
    if not collection.find_one({db_id: {'$exists': 'true' }}):
        log.info(f'no repository ids for {db_id} found, inserting')
        collection.insert_one({db_id: ids})
    else:
        log.info(f'repository ids for {db_id} found, skip inserting')

def getRepoIds(amount, offset):
    '''
    get a specific amount of repo ids from a specific offset on
    @Params
    --------
    amount: int; load a specific amount of ids
    offset: int; load the ids from a specifc offset on
    '''
    db_id = f'repoIds_{amount}_{offset}'
    content = collection.find_one({db_id: {'$exists': 'true' }})
    if bool(content):
        return content[db_id]
    else:
        log.error(f'no repositories ids for scraping found')

