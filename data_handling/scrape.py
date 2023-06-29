import sys 
sys.dont_write_bytecode = True
import logging as log
import data_formatter as format
import data_store as store
import github_access as access

def scrapeGithub(mode = 's', amount = 3000, minStars = 1000, offset = 0):
    '''
    scrape a given amount of repositories
    @Params
    --------
    mode: str; accepts "s" for scraping, "i" for indexing, "is" for both
    amount: int; number of repositories to scrape
    minStars: int; minimum amount of stars
    offset: int; skip the first <offset> repositories
    '''

    log.info(f'script is in "{mode}"-mode')

    if mode.find('i') != -1:
        log.info(f'get {amount} repository ids with the most stars')
        ids = access.getRepoWithMostStars(amount=amount, minStars=minStars)

        log.info(f'storing {amount} repository ids with the most stars')
        store.storeRepoIds(ids=ids, amount=amount)

    if mode.find('s') != -1:
        log.info(f'get {amount} repository ids with the most stars')
        ids = store.getRepoIds(amount=amount)

        log.info(f'get metadata for {amount} projects:')
        for id in ids[offset:]:
            log.info(f'[{id}] - getData')
            data = access.getData(id=id)
            log.info(f'[{id}] - formatData')
            data = format.formatData(data=data)
            log.info(f'[{id}] - storeData')
            store.storeRepoData(repo=id, data=data)
