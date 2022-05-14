# Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
# Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
import chardet

with open('test_file.txt', 'rb') as file:
    res = file.read()
    result = chardet.detect(res)
    out = res.decode(result['encoding']).encode('utf-8')
    print(out.decode('utf-8'))




