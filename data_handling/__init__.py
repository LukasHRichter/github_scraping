import sys 
sys.dont_write_bytecode = True
import os
import logging as log
import api
import scrape
from threading import Thread

ROOT_DIR = './data_handndling'

if not os.path.exists(f'./data_handling/logs'):
    os.mkdir(f'./data_handling/logs')
open(f'./data_handling/logs/combined.log','w').close()

def _startLogger(level):
    levels = {
        'debug': log.DEBUG,
        'info': log.INFO,
        'warn': log.WARN,
        'error': log.ERROR,
    }
    log.basicConfig(filename=f'./data_handling/logs/combined.log', filemode='w', format='[%(asctime)s - %(levelname)s]: %(message)s', level=levels.get(level))

_startLogger('debug')


#example scrape usage
amount = 1
offset = 0
t = Thread(target = scrape.scrapeGithub, args =(amount, offset))
t.start()

#example API usage
#api.getMetadata(100, 'abc', 'def')
