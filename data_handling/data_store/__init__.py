import logging as log
import pymongo
import pymongo.errors
import itertools


#Database connection
URI="mongodb://root:root@db:27017"

client = pymongo.MongoClient(URI)
print("Connection Successful")

db = client["GitHubScraping"]
collection = db["repos"]

def storeData(repo, data, parent = ''):
    # parent may be necessary for dicts with multiple nesting levels
    keys = [key for key in data]
    for key in keys:
        if type(key) == dict: 
            ins = key 
            key = key[str('id')]
        else: ins = data[key]
        try:
            # you can only insert dicts, hence we create a slice of our current dict
            collection.insert_one({'repo': repo, 'parent': parent, key: ins})
        except pymongo.errors.DocumentTooLarge:
            storeData(repo=repo, data=data[key], parent=key)

    return True


def getData(id, param):
    log.debug('getData')
    return {'id': id, 'param': param}
    


