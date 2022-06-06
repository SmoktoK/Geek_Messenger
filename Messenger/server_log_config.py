
import logging
import logging.handlers
import sys
import os

# В директории проекта создать каталог log, в него пишем лог сервера
curr_dir = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(curr_dir, 'log')
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
logging_file = os.path.join(log_dir, 'server.log')
print("Логирование настроено в %s" % logging_file)

# Создать регистратор верхнего уровня с именем 'server'
serv_log = logging.getLogger('server')
# Формат сообщений <дата-время> <уровень_важности> <имя_модуля> <сообщение>
_format = logging.Formatter("%(asctime)s %(levelname)-10s %(module)s: %(message)s")

# # Создать обработчик, который выводит сообщения с уровнем
# # CRITICAL в поток stderr
crit_hand = logging.StreamHandler(sys.stderr)
crit_hand.setLevel(logging.CRITICAL)
crit_hand.setFormatter(_format)

# Создать обработчик, который выводит сообщения в файл
# ротация лога каждые 5 минут для проверки
applog_hand = logging.handlers.TimedRotatingFileHandler(logging_file, when='D', interval=1, encoding='utf-8',
                                                        backupCount=10)
applog_hand.setFormatter(_format)
applog_hand.setLevel(logging.DEBUG)

# Добавить несколько обработчиков в регистратор 'server'
serv_log.addHandler(applog_hand)
serv_log.addHandler(crit_hand)
serv_log.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # Создаем потоковый обработчик логирования (по умолчанию sys.stderr):
    console = logging.StreamHandler(sys.stderr)
    console.setLevel(logging.DEBUG)
    console.setFormatter(_format)
    serv_log.addHandler(console)
    serv_log.info('Тестовый запуск логирования')
    serv_log.critical('critical!')
    serv_log.error('error!')
    serv_log.warning('warning!')
    serv_log.info('info!')
    serv_log.debug('debug!')
