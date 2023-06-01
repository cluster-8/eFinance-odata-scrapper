import logging

open('./logs/log.log', 'w+')

logging.basicConfig(level=logging.INFO, filename='./logs/log.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

# logging.debug('debug')
# logging.info('info')
# logging.warning('warning')
# logging.error('error')
# logging.critical('critical')
