# Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
# Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.

with open('test_file.txt') as file:
    print(f'Кодировка файла: {file.encoding}')
    file.close()

with open('test_file.txt', encoding='utf-8') as file:
    print(file.read())
    file.close()



