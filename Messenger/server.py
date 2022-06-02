import argparse
import json
import logging
import socket
import traceback
from log import server_log_config

from common.utils import get_message, send_message
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, DEFAULT_IP_ADDRESS

server_loger = logging.getLogger('server')


def log(func_to_log):
    def log_saver(*args, **kwargs):
        ret = func_to_log(*args, **kwargs)
        server_loger.debug(f'Вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}. '
                           f'из модуля {func_to_log.__module__}. Вызов из'
                           f' функции {traceback.format_stack()[0].strip().split()[-1]}.')
        return ret
    return log_saver

@log
def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT)
    parser.add_argument('-a', '--address', default=DEFAULT_IP_ADDRESS)
    return parser

@log
def process_client_message(message):
    server_loger.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message and message[USER][
        ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    #  Создаем парсер командной строки
    parser = create_parser()
    connect_data = parser.parse_args()

    listen_address = connect_data.address
    listen_port = connect_data.port
    server_loger.info(f'Сервер запущен {listen_address}:{listen_port}!')
    # Готовим сокет
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    # Слушаем порт
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        server_loger.info(f'Установлено соединение с клиентом {client_address}')
        try:
            message_from_client = get_message(client)
            server_loger.debug(f'Получено сообщение от клиента: {message_from_client}')
            # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
            response = process_client_message(message_from_client)
            server_loger.debug(f'Клиенту отправлен ответ: {response}')
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            server_loger.error(f'Принято некорректное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
