import logging
import os
import sys

client_format = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'client.log')
# print(path)

stream_hand = logging.StreamHandler(sys.stderr)
stream_hand.setFormatter(client_format)
stream_hand.setLevel(logging.DEBUG)
log_file = logging.FileHandler(path, encoding='utf-8')
log_file.setFormatter(client_format)

logger = logging.getLogger('client')
logger.addHandler(stream_hand)
logger.addHandler(log_file)
logger.setLevel(logging.DEBUG)
#
# if __name__ == '__main__':
    # logger.critical('Critical error!')
    # logger.error('Error!')
    # logger.info('Info message')
    # logger.debug('Debug info')
