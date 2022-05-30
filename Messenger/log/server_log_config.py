import logging
import os
import sys

server_format = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'server.log')
# print(path)

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(server_format)
stream_handler.setLevel(logging.DEBUG)
log_file = logging.FileHandler(path, encoding='utf-8')
log_file.setFormatter(server_format)

logger = logging.getLogger('server')
logger.addHandler(stream_handler)
logger.addHandler(log_file)
logger.setLevel(logging.DEBUG)
