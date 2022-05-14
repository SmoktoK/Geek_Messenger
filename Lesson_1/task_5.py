# Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать
# результаты из байтового в строковый тип на кириллице.
import subprocess
import chardet

args1 = ['ping', 'yandex.ru']
args2 = ['ping', 'youtube.com']

ya_ping = subprocess.Popen(args1, stdout=subprocess.PIPE)
you_ping = subprocess.Popen(args2, stdout=subprocess.PIPE)

for i in ya_ping.stdout:
    result_ya = chardet.detect(i)
    i = i.decode(result_ya['encoding']).encode()
    print(i.decode())

for l in you_ping.stdout:
    result_you = chardet.detect(l)
    l = l.decode(result_you['encoding']).encode()
    print(l.decode())





