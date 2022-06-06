from socket import *
from threading import Thread
import time
import argparse
import json
import logging
import inspect
import client_log_config

cli_log = logging.getLogger('client')

enable_tracing = False


def log(func):
    # print("decorator working")
    if enable_tracing:
        def callf(*args, **kwargs):
            cli_log.info("Функция %s: вызвана из функции  %s" % (func.__name__, inspect.stack()[1][3]))
            r = func(*args, **kwargs)
            cli_log.info("%s вернула %s" % (func.__name__, r))
            return r

        return callf
    else:
        return func


@log
def parse_message(str1):  # разобрать сообщение сервера;
    try:
        serv_message = json.loads(str1)
        if serv_message["response"] in (100, 101, 102, 200, 201, 202):
            cli_log.info("Сообщение доставлено на сервер, код возврата %s, %s " % (
                str(serv_message["response"]), serv_message["alert"]))
            return serv_message
    except json.decoder.JSONDecodeError:
        cli_log.critical("Сообщение от сервера не распознано: %s ", str1)
        return {
            "response": 400,
            "time": time.time(),
            "alert": "Сообщение от сервера не распознано"
        }


@log
def presence(username, status):  # сформировать presence-сообщение;
    return {
        "action": "presence",
        "time": time.time(),
        "type": "status",
        "user": {
            "account_name": username,
            "status": status
        }
    }


@log
def message_to_user(from_user, to_user, msg):  # сформировать сообщение;
    # to_user = ""
    # while (len(to_user) == 0) or (len(to_user) > 25):
    #     to_user = input("Кому отправить сообщение:")
    #     if (len(to_user) == 0) or (len(to_user) > 25):
    #         print("имя пользователя/название чата должно содержать от 1 до 25 символов")
    # msg = ""
    # while (len(msg) == 0) or (len(msg) > 500):
    #     msg = input("Введите сообщение:")
    #     if (len(msg) == 0) or (len(msg) > 500):
    #         print("сообщение должно содержать максимум 500 символов")
    return {
        "action": "msg",
        "time": time.time(),
        "to": to_user,
        "from": from_user,
        "encoding": "utf-8",
        "message": msg
    }


def message_chat(from_user, msg):  # сформировать сообщение;
    return {
        "action": "msg",
        "time": time.time(),
        "to": "ALL",  # вообще-то здесь указывается room name,
        # пока упрощенный чат в котором участвуют все подключенные
        "from": from_user,
        "encoding": "utf-8",
        "message": msg
    }


def join_chat(from_user, room_name):  # Присоединиться к чату
    return {
        "action": "join",
        "time": time.time(),
        "from": from_user,
        "room": room_name
    }


def leave_chat(from_user, room_name):  # Покинуть чат
    return {
        "action": "leave",
        "time": time.time(),
        "from": from_user,
        "room": room_name
    }


def read_server_messages(sock):
    while True:  # дальше в цикле получаем сообщения
        data = sock.recv(1024).decode('utf-8')
        server_resp = {}
        server_resp = parse_message(data)
        print(server_resp["alert"])


def client_loop(host, port):  # отправляет сообщения в чат
    # и читает из него в отдельном потоке
    with socket(AF_INET, SOCK_STREAM) as sock:  # Создать сокет TCP
        cli_log.info("Попытка соединения с %s по порту %s" % (host, port))
        # sock.connect(ADDRESS)   # Соединиться с сервером
        try:
            sock.connect((host, port))
        except ConnectionRefusedError:
            cli_log.critical("Сервер %s недоступен по порту %s" % (host, port))
            return
        except OSError as err:
            cli_log.critical("OS error: {0}".format(err))
            return
        else:
            cli_log.info("Подключен к %s по порту %s" % (host, port))
        username = input('Имя пользователя: ')
        msg = json.dumps(presence(username, "Yep, I am here!"))
        sock.send(msg.encode('utf-8'))  # Отправить сообщение presense
        print("presense message sent")
        data = sock.recv(1024).decode('utf-8')  # Получить ответ на него
        server_resp = parse_message(data)
        print(server_resp["alert"])
        # запускаем поток вычитывания серверных сообщений
        receiver = read_server_messages(sock)
        th_sender = Thread(target=receiver)
        th_sender.daemon = True
        th_sender.start()

        while True:  # дальше в цикле отправляем сообщения
            msg = input('Ваше сообщение: ')
            if msg == 'exit':
                break
            msg = json.dumps(message_chat(username, msg))
            sock.send(msg.encode('utf-8'))  # Отправить!


# получить и обработать параметры командной строки
def parse_args():
    parser = argparse.ArgumentParser(description='Client App')
    parser.add_argument("-a", action="store", dest="addr", type=str, default='localhost',
                        help="enter IP address, default is localhost")
    parser.add_argument("-p", action="store", dest="port", type=int, default=7777,
                        help="enter port number, default is 7777")
    # parser.add_argument("-t", action="store", dest="trace", type=str, default='false',
    #                    help="enter 'true' to enable tracing, default is 'false'")
    return parser.parse_args()


def main():
    # print("main working")
    cli_log.debug('Старт приложения')
    args = parse_args()
    port = args.port
    host = args.addr
    # enable_tracing = args.trace
    print("Connecting to %s:%s" % (host, port))
    client_loop(host, port)


# Entry point
if __name__ == '__main__':
    main()
