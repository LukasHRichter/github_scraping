import logging as log

log.basicConfig(filename='combined.log', filemode='w', format='[%(asctime)s - %(levelname)s]: %(message)s', level=log.DEBUG)

log.debug('test')