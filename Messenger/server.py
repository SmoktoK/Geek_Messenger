import argparse
import logging
import select
import socket
import time

from common.utils import get_message, send_message
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, DEFAULT_IP_ADDRESS, MESSAGE, TEXT_MESSAGE, SENDER
from decos import log

server_loger = logging.getLogger('server')


@log
def process_client_message(message, messages_list, client):
    server_loger.debug(f'Разбор сообщения от клиента : {message}')
    # Если это сообщение о присутствии, принимаем и отвечаем, если успех
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return
    # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
    elif ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and TEXT_MESSAGE in message:
        messages_list.append((message[ACCOUNT_NAME], message[TEXT_MESSAGE]))
        return
    # Иначе отдаём Bad request
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


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
    clients = []
    messages = []
    #  Создаем парсер командной строки
    parser = create_parser()
    connect_data = parser.parse_args()

    listen_address = connect_data.address
    listen_port = connect_data.port
    server_loger.info(f'Сервер запущен {listen_address}:{listen_port}!')
    # Готовим сокет
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.5)
    # Слушаем порт
    transport.listen(MAX_CONNECTIONS)

    while True:
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            server_loger.info(f'Установлено соединение с клиентом {client_address}')
            clients.append(client)
        recv_data_lst = []
        send_data_lst = []
        err_lst = []

        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass
            # принимаем сообщения и если там есть сообщения,
            # кладём в словарь, если ошибка, исключаем клиента.
            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        process_client_message(get_message(client_with_message), messages, client_with_message)
                    except:
                        server_loger.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                        clients.remove(client_with_message)

            # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
            if messages and send_data_lst:
                message = {
                    ACTION: MESSAGE,
                    SENDER: messages[0][0],
                    TIME: time.time(),
                    TEXT_MESSAGE: messages[0][1]
                }
                del messages[0]
                for waiting_client in send_data_lst:
                    try:
                        send_message(waiting_client, message)
                    except:
                        server_loger.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                        clients.remove(waiting_client)


if __name__ == '__main__':
    main()
