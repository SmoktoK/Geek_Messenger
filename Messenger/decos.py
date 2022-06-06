import sys
import logging
import server_log_config
import client_log_config
import traceback

if sys.argv[0].find('client') == -1:
    loger = logging.getLogger('server')
else:
    loger = logging.getLogger('client')


def log(func_to_log):
    def log_saver(*args, **kwargs):
        ret = func_to_log(*args, **kwargs)
        loger.debug(f'Вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}. '
                    f'из модуля {func_to_log.__module__}. Вызов из'
                    f' функции {traceback.format_stack()[0].strip().split()[-1]}.')
        return ret

    return log_saver
