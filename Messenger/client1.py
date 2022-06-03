import argparse
import json
import logging
import socket
import sys
import time
from decos import log
from log import client_log_config

from common.utils import get_message, send_message
from common.variables import *

client_logger = logging.getLogger('client')


# def log(func_to_log):
#     def log_saver(*args, **kwargs):
#         ret = func_to_log(*args, **kwargs)
#         client_logger.debug(f'Вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}. '
#                             f'из модуля {func_to_log.__module__}. Вызов из'
#                             f' функции {traceback.format_stack()[0].strip().split()[-1]}.')
#         return ret
#     return log_saver

@log
def create_parser():
    parser = argparse.ArgumentParser()
    #  Ключи для парсера командной строки
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT)
    parser.add_argument('-a', '--address', default=DEFAULT_IP_ADDRESS)
    parser.add_argument('-m', '--mode', default=DEF_MODE)
    return parser

@log
def mess_from_server(message):
    if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and TEXT_MESSAGE in message:
        print(f'получено сообщение от пользователя: {message[SENDER]}:\n {message[TEXT_MESSAGE]}')
        client_logger.info(f'получено сообщение от пользователя: {message[SENDER]}:\n {message[TEXT_MESSAGE]}')
    else:
        client_logger.error(f'Получено некорректное сообщение {message} ')

@log
def create_mess(sock, account_name='Guest'):
    message = input(f'Input message, or \'quite\' for exit!')
    if message == 'quite':
        sock.close()
        client_logger.info('User send stop ')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        TEXT_MESSAGE: message
    }
    client_logger.debug(f'Сформировано сообщение: {message_dict}')
    return message_dict

@log
def create_presence(account_name='Guest'):
    # отправка сообщения
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
    client_mode = connect_data.mode
    if client_mode not in ('listen', 'send'):
        client_logger.critical(f'Указан недопустимы режим работы клиента {client_mode}, '
                               f'Необходимо указать: listen или send')
        sys.exit(1)
    else:
        print(f'Запущен клиент с режимом работы: {client_mode}')
    client_logger.info(f'Попытка подключения к серверу {server_address}:{server_port}')

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        transport.connect((server_address, server_port))
        message_to_server = create_presence()
        send_message(transport, message_to_server)
        client_logger.info(f'Подключение к серверу {server_address}:{server_port} прошло успешно.')
        print('Подключение прошло успешно!')
    except ConnectionRefusedError:
        client_logger.critical(f' Не удалось подключиться к серверу {server_address}:{server_port}')
    except (ValueError, json.JSONDecodeError):
        client_logger.error(f'Сообщение не декодировано.')
    else:
        answer = process_ans(get_message(transport))
        client_logger.info(f'Ответ от сервера принят: {answer}')
        if client_mode == 'send':
            print('Режим работы- отправка сообщений')
        else:
            print('Режим работы- прием сообщений')

        while True:
            if client_mode == 'send':
                try:
                    send_message(transport, create_mess(transport))
                except (ConnectionRefusedError, ConnectionError, ConnectionAbortedError):
                    client_logger.error(f'Соединение с {server_address} потеряно.')
                    sys.exit(1)

            if client_mode == 'listen':
                try:
                    mess_from_server(get_message(transport))
                except (ConnectionRefusedError, ConnectionError, ConnectionAbortedError):
                    client_logger.error(f'Соединение с {server_address} потеряно.')
                    sys.exit(1)



if __name__ == '__main__':
    main()
