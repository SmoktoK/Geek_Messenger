
from socket import *
import select
import time
import json
import argparse
import logging
import server_log_config

serv_log = logging.getLogger('server')


# def recv_message(client, addr):
#     data = client.recv(1024)
#     serv_log.info("Сообщение %s было отправлено клиентом: %s" % (data.decode('utf-8'), str(addr)))
#     json_mess = {}
#     try:
#         json_mess = json.loads(data.decode('utf-8'))
#         serv_log.info("Сообщение: Action=%s длиной %s байт" % (str(json_mess["action"]),
#                                                                str(len(data))))
#     except json.decoder.JSONDecodeError:
#         serv_log.critical("Сообщение от клиента не распознано %s" % data.decode('utf-8'))
#     return json_mess


# def server_communicate(s: socket):
#     client, addr = s.accept()
#     serv_log.info("Получен запрос на соединение от %s" % str(addr))
#     msg_from_client = recv_message(client, addr)
#     server_response(msg_from_client, client)


def server_response(incoming_msg):
    # парсим сообщение клиента и формируем ответ сервера
    # ответ вида:
    # presense = клиент ... вошел в чат
    # msg = сообщение от клиента ...
    client_msg = {}
    try:
        client_msg = json.loads(incoming_msg)
        serv_log.info("Сообщение: Action=%s длиной %s байт" % (str(client_msg["action"]),
                                                               str(len(incoming_msg))))
    except json.decoder.JSONDecodeError:
        serv_log.critical("Сообщение от клиента не распознано %s" % incoming_msg)
    json_resp = {}
    if client_msg["action"] == 'presence':
        json_resp = {
            "response": 200,
            "time": time.time(),
            "alert": "Соединение установлено"
        }
        print("%s вошел в чат" % client_msg["user"]["account_name"])
    elif client_msg["action"] == 'msg':
        json_resp = {
            "response": 200,
            "time": time.time(),
            "alert": "Сообщение отправлено пользователю " + client_msg["to"]
        }
        print("Сообщение от %s: %s" % (client_msg["from"], client_msg["message"]))
    msg = json.dumps(json_resp)
    return msg


def read_requests(r_clients, all_clients):
    # Чтение запросов из списка клиентов
    # может быть сообщение о входе в чат (presense)
    # или текстовое сообщение всем в чате
    # на прочитанное сообщение формируем ответ и сохраняем в списке
    requests = {}      # Список запросов от клиентов  вида {сокет: запрос}
    responses = {}     # Список ответов вида {сокет: запрос}
    for sock in r_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            requests[sock] = data
            responses[sock] = server_response(data)
        except:
            print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
            all_clients.remove(sock)
    return requests, responses


def write_responses(responses, w_clients, all_clients):
    # ответ сервера клиентам, от которых были запросы
    for sock in w_clients:
        if sock in responses:
            try:
                # Подготовить и отправить ответ сервера
                resp = responses[sock].encode('utf-8')
                # рассылаем сообщения всем клиентам
                for client in all_clients:
                    client.sendall(resp)
            except:                 # Сокет недоступен, клиент отключился
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                sock.close()
                all_clients.remove(sock)


def parse_args():
    parser = argparse.ArgumentParser(description='Server App')
    parser.add_argument("-p", action="store", dest="port", type=int, default=7777,
                        help="enter port number, default is 7777")
    parser.add_argument("-a", action="store", dest="addr", type=str, default='0.0.0.0',
                        help="enter IP address, default is 0.0.0.0")
    return parser.parse_args()


def mainloop():
    #Основной цикл обработки запросов клиентов
    args = parse_args()
    port = args.port
    clients = []
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', port))
    s.listen(5)
    s.settimeout(1)  # Таймаут для операций с сокетом
    serv_log.info("Запущено прослушивание порта %s" % str(port))
    while True:
        try:
            conn, addr = s.accept()  # Проверка подключений
        except OSError as e:
            pass  # timeout вышел
        else:
            print("Получен запрос на соединение от %s" % str(addr))
            clients.append(conn)
        finally:
            # Проверить наличие событий ввода-вывода
            wait = 0
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except:
                pass  # Ничего не делать, если какой-то клиент отключился
            requests, responses = read_requests(r, clients)  # Сохраним запросы клиентов
            write_responses(responses, w, clients)  # Выполним отправку ответов клиентам


if __name__ == '__main__':
    mainloop()
