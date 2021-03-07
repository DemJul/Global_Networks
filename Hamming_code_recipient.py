import recipient_functions as functions
import socket

# Код для клиента 2

print_information = False

# Часть 1. Работа с сокетами (приём данных)

print("Ожидаем приёма текста")

# Принимаем исходный текст
Hamming_mas = []

sock_1 = socket.socket()
sock_1.bind(('127.0.0.1', 9090))
sock_1.listen(1)
conn_1, addr_1 = sock_1.accept()

while True:
    data = list(conn_1.recv(1024))
    for i in range(len(data)):
        Hamming_mas.append(data[i])
    if not data:
        break

conn_1.close()

# Принимаем значение длины слова для кода Хемминга
sock_2 = socket.socket()
sock_2.bind(('127.0.0.1', 49100))
sock_2.listen(1)
conn_2, addr_2 = sock_2.accept()

length_hamming_word_input = functions.bin_dec(list(conn_2.recv(1024)))

conn_2.close()

# Принимаем значение кодировки исходного текста
sock_3 = socket.socket()
sock_3.bind(('127.0.0.1', 49101))
sock_3.listen(1)
conn_3, adrr_3 = sock_3.accept()

encoding = functions.get_ascii_code((conn_3.recv(1024)), 16)
encoding = functions.get_text(encoding, 16, 'utf8')

conn_3.close()

# Принимаем значение длины слова для кодировки
sock_4 = socket.socket()
sock_4.bind(('127.0.0.1', 49102))
sock_4.listen(1)
conn_4, adrr_4 = sock_4.accept()

word_length = functions.bin_dec(list(conn_4.recv(1024)))

print("Данные приняты")
print()
# Часть 2. Выводим полученные данные на экран
if(print_information):
    print("Часть 2. Выводим полученные данные на экран")
    print()

    print("Hamming_mas = ")
    print(Hamming_mas)
    print()

    print("Длина Hamming_mas = ")
    print(len(Hamming_mas))
    print()

    print("length_hamming_word_input = ", length_hamming_word_input)

    print("encoding = ", encoding)
    print("type(encoding) = ", type(encoding))

    print("word_length = ", word_length)
    print()

# Часть 3. Проверка и расшифровка текста
print("Часть 3. Проверка и расшифровка текста")
# Обнаруживаем ошибки и исправляем, если они есть
bit_mas_new, count_of_true_words, count_of_false_words, count_of_corrected_words, count_of_uncorrected_words = functions.Repeat_Hamming_code(Hamming_mas, length_hamming_word_input)

# Переводим текст в список цифр в десятичной СС
file_code_2 = functions.get_ascii_code(bit_mas_new, word_length)

if(print_information):
    print("file_code_2 = ")
    print(file_code_2)
    print()

max = 0
for i in range(len(file_code_2)):
    if(file_code_2[i] > max):
        max = file_code_2[i]

if(print_information):
    print("max = ", max)
    print()

# Декодируем исходное сообщение
try:
    text = bytes(file_code_2)
    text = text.decode(encoding)
except UnicodeDecodeError:
    print("Из-за проблем с кодировкой расшифровать сообщение, в котором хотя бы в одном слове более двух ошибок, невозможно.")
    print("Мне очень жаль.")
    count_of_true_words = 0
    count_of_false_words = 0
    count_of_corrected_words = 0
    count_of_uncorrected_words = 0
    text = ""

if(print_information):
    print("text = ")
    print(text)
    print()
else:
    file = open("texts/accepted text.txt", "w", encoding = encoding)
    file.write(text)
    file.close()

print("Проверка и расшифровка текста окончена")
print()
# Часть 4. Отправка информации о принятом файле
print("Часть 4. Отправка информации о принятом файле")
# Отправляем информацию о количестве правильно принятых слов
sock_1 = socket.socket()
sock_1.connect(('127.0.0.1', 49110))
sock_1.send(bytes(functions.dec_bin(count_of_true_words)))
sock_1.close()

# Отправляем информацию о количестве неправильно принятых слов
sock_2 = socket.socket()
sock_2.connect(('127.0.0.1', 49111))
sock_2.send(bytes(functions.dec_bin(count_of_false_words)))
sock_2.close()

# Отправляем информацию о количестве исправленных слов
sock_3 = socket.socket()
sock_3.connect(('127.0.0.1', 49112))
sock_3.send(bytes(functions.dec_bin(count_of_corrected_words)))
sock_3.close()

# Отправляем информацию о количестве неисправленных слов
sock_4 = socket.socket()
sock_4.connect(('127.0.0.1', 49113))
sock_4.send(bytes(functions.dec_bin(count_of_uncorrected_words)))
sock_4.close()

print("Отправка завершена")