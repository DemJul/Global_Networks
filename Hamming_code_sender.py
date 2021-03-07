import sender_functions as functions
import math
import socket

# Код для клиента 1

print_information = False

# Часть 1. Считывание текста с файла
print("Часть 1. Считывание текста с файла")

path_4 = "texts/My_text.txt"

# Определяем кодировку текста в файле
encoding = functions.get_encoding(path_4)
en = encoding['encoding']

if(print_information):
    print("Кодировка файла - ", en)

# Считываем текст с заданной кодировкой
file_text = functions.read_file(path_4, en) # Исходный файл

if(print_information):
    print("file =")
    print(file_text)
    print()

print("Считывание текста с файла окончено")
print()

# Часть 2. Переводим текст в список цифр в десятичной СС
print("Часть 2. Переводим текст в список цифр в десятичной СС")

file_code = list(file_text.encode(en))

if(print_information):
    print("file_text = ")
    print(file_code)
    print()

print("Перевод текста в список цифр в десятичной СС окончен")
print()

# Часть 3. Переводим текст из списка цифр в десятичной СС в список цифр в двоичной СС
print("Часть 3. Переводим текст из списка цифр в десятичной СС в список цифр в двоичной СС")
# Поиск максимального числа
max_length = 0
for i in range(len(file_code)):
    if(file_code[i] > max_length):
        max_length = file_code[i]

if(print_information):
    print("max_length = ")
    print(max_length)
    print()

# Поиск длины слова в доичном виде
word_length = math.ceil(math.log(max_length, 2))

if(print_information):
    print("word_length = ")
    print(word_length)
    print()

# Преобразование в двоичную СС
bit_mas = functions.get_bit_mas(file_code, word_length)

if(print_information):
    print("bit_mas = ")
    print(bit_mas)
    print("len(bit_mas) = ", len(bit_mas))

print("Перевод текста из списка цифр в десятичной СС в список цифр в двоичной СС окончен")
print()

# Часть 4. Применяем кодировку Хемминга
print("Часть 4. Применяем кодировку Хемминга")
# Длина слова Хемминга до вставки контрольных битов
length_hamming_word_input = 47
# Длина слова Хемминга после вставки контрольных битов
length_hamming_word_output = length_hamming_word_input + math.floor(math.log(length_hamming_word_input, 2)) + 1
#Количество ошибок
# 0 - Без ошибок
# 1 - Сообщение отправлено с внесением не более 1 ошибки
# 2 - Сообщение отправлено с внесением более 1 ошибки
count_of_errors = 2
Hamming_mas = functions.Hamming_code(bit_mas, length_hamming_word_input, count_of_errors)

if(print_information):
    print("Hamming_mas = ")
    print(Hamming_mas)
    print()

    print("Длина Hamming_mas = ")
    print(len(Hamming_mas))
    print()

print("Применение кодировки Хемминга окончено")
print()
# Часть 5. Отправляем данные на другой хост в локальной сети
print("Часть 5. Отправляем данные на другой хост в локальной сети")

# Отправляем исходный текст
sock_1 = socket.socket()
sock_1.connect(('127.0.0.1', 9090))
sock_1.send(bytes(Hamming_mas))
sock_1.close()

# Отправляем значение длины слова для кода Хемминга
sock_2 = socket.socket()
sock_2.connect(('127.0.0.1', 49100))
sock_2.send(bytes(functions.dec_bin(length_hamming_word_input)))
sock_2.close()

# Отправляем значение кодировки исходного текста
# Преобразуем данные в необходимый для отправки вид
en_code = list(en.encode('utf8'))
en_bit_mas = functions.get_bit_mas(en_code, 16)

if(print_information):
    print("en = ", en)
    print("type(en) = ", type(en))
    print("en_code = ", en_code)
    print("en_bit_mas = ", en_bit_mas)

sock_3 = socket.socket()
sock_3.connect(('127.0.0.1', 49101))
sock_3.send(bytes(en_bit_mas))
sock_3.close()

# Принимаем значение длины слова для кодировки
sock_4 = socket.socket()
sock_4.connect(('127.0.0.1', 49102))
sock_4.send(bytes(functions.dec_bin(word_length)))
sock_4.close()

print("Отправка завершена")
print()

# Часть 6. Приём ответной информации о переданном файле
print("Часть 6. Ожидаем приёма ответной информации о переданном файле")

# Принимаем информацию о количестве правильно принятых слов
sock_1 = socket.socket()
sock_1.bind(('127.0.0.1', 49110))
sock_1.listen(1)
conn_1, addr_1 = sock_1.accept()

count_of_true_words = functions.bin_dec(list(conn_1.recv(1024)))

conn_1.close()

# Принимаем информацию о количестве неправильно принятых слов
sock_2 = socket.socket()
sock_2.bind(('127.0.0.1', 49111))
sock_2.listen(1)
conn_2, addr_2 = sock_2.accept()

count_of_false_words = functions.bin_dec(list(conn_2.recv(1024)))

conn_2.close()

# Принимаем информацию о количестве исправленных слов
sock_3 = socket.socket()
sock_3.bind(('127.0.0.1', 49112))
sock_3.listen(1)
conn_3, addr_3 = sock_3.accept()

count_of_corrected_words = functions.bin_dec(list(conn_3.recv(1024)))

conn_3.close()

# Принимаем информацию о количестве неисправленных слов
sock_4 = socket.socket()
sock_4.bind(('127.0.0.1', 49113))
sock_4.listen(1)
conn_4, addr_4 = sock_4.accept()

count_of_uncorrected_words = functions.bin_dec(list(conn_4.recv(1024)))

conn_4.close()

print("Данные приянты")
print()

# Вывод на экран полученных данных
if(print_information):
    print("Количество правильно переданных слов -", count_of_true_words)
    print("Количество неправильно переданных слов -", count_of_false_words)
    print("Количество исправленных слов -", count_of_corrected_words)
    print("Количество неисправленных слов -", count_of_uncorrected_words)
else:
    file = open("texts/accepted_text_information.txt", "w")
    s = "Количество правильно переданных слов - " + str(count_of_true_words) + "\n"
    s = s + "Количество неправильно переданных слов - " + str(count_of_false_words) + "\n"
    s = s + "Количество исправленных слов - " + str(count_of_corrected_words) + "\n"
    s = s + "Количество неисправленных слов - " + str(count_of_uncorrected_words)
    file.write(s)
    file.close()