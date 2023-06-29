import sys 
sys.dont_write_bytecode = True
import logging as log
import data_formatter as format
import data_store as store
import github_access as access

def scrapeGithub(amount, offset):
    ids = access.getMostForkedProjects(amount, offset)
    #https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc
    #https://github.com/search?l=Python&q=stars%3A%3E1&s=stars&type=Repositories
    ids = [12888993, 81598961, 32689863, 5483330, 145553672, 162998479, 154747577, 91573538, 57222302, 237791077]

    log.debug(f'Get metadata for {len(ids)} projects:')
    for id in ids:
        log.debug(f'[{id}] - getData')
        data = access.getData(id=id)
        log.debug(f'[{id}] - formatData')
        data = format.formatData(data=data)
        log.debug(f'[{id}] - storeData')
        store.storeData(repo=id, data=data)
