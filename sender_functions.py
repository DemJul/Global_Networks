import math
from chardet.universaldetector import UniversalDetector
import copy
import random

# Длина слова в коде Хемминга - 47

# Вспомогательные методы
#ord(символ) - символ в его код в ascii
#chr(число) - код ascii в символ
#print(int('1101', base=2)) - перевод из двоичной сс и десятичную

# Считывание текста из файла с заданной кодировкой
def read_file(path, encoding):
    text = ""
    with open(path, "r", encoding = encoding) as f:
        for line in f.readlines():
            text += line
    return text

# Определение кодировки заданного файла
def get_encoding(path):
    detector = UniversalDetector()
    with open(path, 'rb') as fh:
        for line in fh:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    if (detector.result == None):
        print("Неизвестная кодиковка. Невозможно открыть прочитать текст")
        exit()
    return detector.result

# Кодировка из значения ascii в массив с двоичным кодом
def get_bit_mas(code, word_length):
    bit_mas = []
    for i in range(len(code)):
        s = bin(code[i])
        s = s[2:] # Удаляем первые символы '0b' из двоичной кодировки
        while(len(s) != word_length): # Добавляем 0, если слово короче заданной длины
            s = '0' + s
        for j in range(len(s)):
            bit_mas.append(int(s[j]))
    return bit_mas

# Реализация кода Хемминга
def Hamming_code(bit_mas, length_hamming_word_input, count_of_errors):
    Hamming_mas = [] # Список с готовым кодом

    count_of_iterations = math.ceil(len(bit_mas) / length_hamming_word_input)

    # Считываем одно слово
    for k in range(count_of_iterations):
        try:
            value_word = bit_mas[0:length_hamming_word_input]
            bit_mas = bit_mas[length_hamming_word_input:]
        except:
            value_word = bit_mas
            bit_mas = []

        # Вставка контрольных битов (по умолчанию принимают 0)
        counter = 0
        value = 0
        while(value < len(value_word)):
            value_word.insert(value, 0)
            counter = counter + 1
            value = (2 ** counter) - 1

        # Установка значений контрольных битов
        counter = 0
        value = 2 ** counter
        while(value - 1 < len(value_word)):
            i = value - 1
            count_of_one = 0
            while(i < len(value_word)):
                for j in range(value):
                    if(value_word[i] == 1):
                        count_of_one = count_of_one + 1
                    i = i + 1
                    if(i >= len(value_word)):
                        break
                i = i + value
            value_word[value - 1] = count_of_one % 2
            counter = counter + 1
            value = 2 ** counter

        # Генерация и вставка заданного количества ошибок
        if(count_of_errors != -1):
            for i in range(count_of_errors):
                number = math.floor(len(value_word) * random.random())
                if(value_word[number] == 0):
                    value_word[number] = 1
                elif(value_word[number] == 1):
                    value_word[number] = 0

        # Добавление текущего слова в готовый список
        for i in range(len(value_word)):
            Hamming_mas.append(value_word[i])

    return Hamming_mas

# Перевод из десятичной сс в двоичную (число -> список)
def dec_bin(number):
    number_copy = copy.deepcopy(number)
    l = []
    while(number_copy != 0):
        l.append(number_copy % 2)
        number_copy = math.floor(number_copy / 2)
    l.reverse()
    return l

# Перевод из двоичной сс в десятичную (список -> число)
def bin_dec(l):
    l_copy = copy.deepcopy(l)
    number = 0
    for i in range(len(l_copy)):
        number = number + (l_copy[i] * (2 ** (len(l_copy) - i - 1)))
    return number