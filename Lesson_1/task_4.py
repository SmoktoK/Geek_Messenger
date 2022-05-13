# Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое
# и выполнить обратное преобразование (используя методы encode и decode).

var_1 = 'разработка'
var_2 = 'администрирование'
var_3 = 'protocol'
var_4 = 'standard'

var_list = [var_1, var_2, var_3, var_4]

for i in var_list:
    byte_var = i.encode()
    print(byte_var)
    str_var = byte_var.decode()
    print(str_var)


