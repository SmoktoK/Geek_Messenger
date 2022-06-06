# Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
# (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.

var_1 = b'class'
var_2 = b'function'
var_3 = b'method'

var_list = [var_1, var_2, var_3]

for i in var_list:
    print(f'{i}, Type:{type(i)}, Len:{len(i)}')
