# Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.

var_1 = 'attribute'
var_2 = 'класс'
var_3 = 'функция'
var_4 = 'type'

var_list = [var_1, var_2, var_3, var_4]

for i in var_list:
    try:
        print(bytes(i, 'ascii'))
    except UnicodeEncodeError:
        print(f'Ошибка! Слово \"{i}\" невозможно записать в байтовом типе')
