import sys 
sys.dont_write_bytecode = True
import os
import logging as log
import scrape
from threading import Thread

ROOT_DIR = './data_handling'

if not os.path.exists(f'{ROOT_DIR}/logs'):
    os.mkdir(f'{ROOT_DIR}/logs')
open(f'{ROOT_DIR}/logs/combined.log','w').close()

def _startLogger(level):
    levels = {
        'debug': log.DEBUG,
        'info': log.INFO,
        'warn': log.WARN,
        'error': log.ERROR,
    }
    #log.basicConfig(filename=f'{ROOT_DIR}/logs/combined.log', filemode='w', format='[%(asctime)s - %(levelname)s]: %(message)s', level=levels.get(level))
    log.basicConfig(format='[%(asctime)s - %(levelname)s]: %(message)s', level=levels.get(level))

_startLogger('info')
log.debug('Start logging')


# amount of repos to be scraped in multiples of 1000
# after every 3000 repos we need to wait 10 minutes
amount = 30000
# >1000 stars -> max repos 37000
# >100 stars -> max repos 295000
minStars = 1000
# Modes:
# 'i': index RepoIds
# 's': scrape indexed Repos
# 'is': do both
mode = 's'
# offset for scraping the next x repos
offset = 7000

t = Thread(target = scrape.scrapeGithub, args =(mode, amount, minStars, offset))
t.start()
