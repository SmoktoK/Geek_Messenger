import argparse
import json
import logging
import socket
import time
import traceback
from log import client_log_config

from common.utils import get_message, send_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT

client_logger = logging.getLogger('client')


def log(func_to_log):
    def log_saver(*args, **kwargs):
        ret = func_to_log(*args, **kwargs)
        client_logger.debug(f'Вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}. '
                            f'из модуля {func_to_log.__module__}. Вызов из'
                            f' функции {traceback.format_stack()[0].strip().split()[-1]}.')
        return ret
    return log_saver

@log
def create_parser():
    parser = argparse.ArgumentParser()
    #  Ключи для парсера командной строки
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT)
    parser.add_argument('-a', '--address', default=DEFAULT_IP_ADDRESS)
    return parser

@log
def create_presence(account_name='Guest'):  # отправка присутствия клиента
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    client_logger.debug(f'{PRESENCE} сообщение сформировано для {account_name}')
    return out

@log
def process_ans(message):  # ответ сервера
    client_logger.debug(f'Сообщение от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


def main():
    #  активация парсера аргументов командной строки
    parser = create_parser()
    connect_data = parser.parse_args()
    server_address = connect_data.address
    server_port = connect_data.port
    client_logger.info(f'Попытка подключения к серверу {server_address}:{server_port}')

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        transport.connect((server_address, server_port))
        message_to_server = create_presence()
        send_message(transport, message_to_server)
        client_logger.info(f'Подключение к серверу {server_address}:{server_port} прошло успешно.')
    except ConnectionRefusedError:
        client_logger.critical(f' Не удалось подключиться к серверу {server_address}:{server_port}')
    try:
        answer = process_ans(get_message(transport))
        client_logger.info(f'Ответ от сервера принят: {answer}')
    except (ValueError, json.JSONDecodeError):
        client_logger.error(f'Сообщение не декодировано.')


if __name__ == '__main__':
    main()
