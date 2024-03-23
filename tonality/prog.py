from pymorphy3 import MorphAnalyzer # необходим для морфологического анализа, 
# конкретно участвует в процессе приведения словоупотеблений к леммам

from nltk.corpus import stopwords # используем список стоп-слов, чтобы очистить текст от них, то есть от слов,
# которые не влияют на тонатльность, но портят статистику частоты лемм

from nltk.tokenize import word_tokenize # для парсинга текста на слова

from nltk.probability import FreqDist # для вычисления статистических данных

import pandas as pd # для работы с тональным словарем

import re # для использования регулярных выражений при удалении числительных из текста

from collections import defaultdict # для более удобной работы 


# получение лемм из списка слов с исключением числительных
def get_lemmas(words):
    pm3 = MorphAnalyzer()
    parsings = [pm3.parse(w)[0] for w in words]
    lemmas = [p.normal_form for p in parsings if p.tag.POS != 'NUMR']
    return lemmas


# запись в файл filename списка слов lst
def write_to_file(filename, lst):
    f = open(filename, 'w')
    for el in lst:
        print(el, file = f)
    f.close()


# функция, где происходит подготовка текста к анализу: токенизация, очищение от знаков препинаний, лемматизация, очистка от стоп-слов
def text_preparing(filename, num = 0):

    # переменные для вычисления статистических характеристик: общее кол-во слов в тексте и кол-во лемм
    all_words = 0
    all_lemmas = 0

    # токенизация и удаление чисел
    f = open(filename, 'r')
    text = f.read()
    f.close()
    text = text.lower() # приводим текст к нижнему регистру
    numbers_pattern = r'\b\d+\b' # регулярное выражение для выделения чисел
    text = re.sub(numbers_pattern, '', text) # удаление чисел
    text = text.replace('.\\xa0—', ' ')
    word_tokens = word_tokenize(text) # токенизация
    
    # очистка текста от знаков препинания
    punkt = ['!', ',', '.', '...', '?', ':', '(', ')', ';', '—', '»', '«', '–', '-', '"', "'", '`', '``', "''", '..'] 
    words = []
    for w in word_tokens: 
        if w not in punkt: 
            words.append(w)
    
    # определение некот. статистических характеристик, лемматизация
    all_words = len(words) # получение кол-ва словоупотреблений
    lemmas = get_lemmas(words) # лемматизация и исключение числительных
    all_lemmas = len(set(lemmas)) # получение кол-ва уникальных лемм
    
    # очищение текста от стоп-слов
    stop_words = stopwords.words('russian')
    stop_words.extend(['всё', 'это', 'весь', 'ваш', 'свой', 'который', 'ещё', 'ах', 'её', '№', '*', 'какой-то'])
    stop_words.extend(['мгу', 'вмк', 'пми', 'фиит']) # исключаю из рассмотрения слова, характерные для прикладной задачи
    set_stop = set(stop_words)
    filtered_lemmas = []
    for w in lemmas: 
        if w not in set_stop: 
            filtered_lemmas.append(w) 

    # для более симпатичного вывода        
    if num != 0:
        print(f'Проанализирован отзыв {num}')

    # функция возвращает общее кол-во слов, лемм и очищенный лемматизированный текст
    return all_words, all_lemmas, filtered_lemmas


def print_dict(d):
    
    # исключаю из рассмотрения слова, которые бесполезны конкретно в данной задаче и уже не повлияют на тональность
    neut_words = ['учиться', 'курс', 'хороший', 'очень', 'вуз', 'семестр', 'просто', 'год', 'первый', 'второй', 'неделя', 'сюда'] 
    for i in neut_words:
        if i in d.keys():
            d[i] = 0
    d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse = True)} # сортировка словаря
    keys = list(d.keys())[:5]
    for key in keys:
        print(key, d[key])
    print()



# ______ main ______ #


# Решение поставленной задачи
print()
print('Сначала приведу решение программы, соответствующее поставленному заданию,\nна примере мучительных и карательных рассуждений Раскольникова\nиз произведения Ф. М. Достоевского "Преступление и наказание"', end = '\n\n')

# 1) Морфологический анализ текста, очищение текста
#name = 'examples/crime_and_punishment.txt'
name = 'test1.txt'
all_words, all_lemmas, words = text_preparing(name)

# 2) Вычисление общестатистических характеристик: общее число словоупотреблений, число уникальных лемм и самые популярные леммы
print(f'Общее число словоупотреблений: {all_words}', end = '\n\n')
print(f'Число уникальных лемм: {all_lemmas}', end = '\n\n')
print("15 наиболее популярных лемм в тексте (с исключением стоп-слов):")
fdist = FreqDist(words) # использую класс FreqDist для подсчет а
for elem in fdist.most_common(15):
    print(elem[0], elem[1])
print()

# 3) Определение тональной окрашенности текста
df = pd.read_csv('kartaslovsent.csv', delimiter = ';') # загрузка словаря kartaslov
df = df.set_index(df['term'])
df = df.drop(columns = ['term'])
df = df[df['tag'] != 'NEUT'] # выделение из словаря нужного подмножества
rate = 0
cnt = 0
for el in words:
    if el in set(df.index):
        rate +=  df.at[el, 'value']
        cnt += 1
        
res = rate / cnt
print(f'Численное значение тональной окрашенности текста: {round(res, 3)}')
if res <= 0.2:
    print('Текст имеет негативную окраску')
elif res >= 0.45: 
    print('Текст имеет положительную окраску')
else:
    print('Текст имеет нейтральную окраску')
print(end = '\n\n')


# Решение прикладной задачи
print('Далее решение прикладной задачи', end = '\n\n')
dict_neg = defaultdict(int)
dict_pos = defaultdict(int)
cnt_all = 12
cnt_pos = 0
cnt_neg = 0
for i in range(cnt_all):
    name = 'reviews/review' + str(i + 1) + '.txt'

    # Морфологический анализ текста, очищение текста
    all_words, all_lemmas, words = text_preparing(name, i + 1)

    # Определение тональной окрашенности текста
    rate = 0
    cnt = 0
    for el in words:
        if el in set(df.index):
            rate +=  df.at[el, 'value']
            cnt += 1

    res = rate / cnt
    if res <= 0.2:
        tonality = 'NGTV'
        dict = dict_neg
        cnt_neg += 1
    elif res >= 0.45: 
        tonality = 'PSTV'
        dict = dict_pos
        cnt_pos += 1
    else:
        tonality = 'NEUT'
        continue

    # Вычисление общестатистических характеристик: общее число словоупотреблений, число уникальных лемм и самые популярные леммы
    fdist = FreqDist(words)
    for elem in fdist.most_common(10):
        dict[elem[0]] += elem[1]

print()
print(f'Количество проанализированных отзывов: {cnt_all}')
print(f'Из них позитивных: {cnt_pos}')
print(f'Негативных: {cnt_neg}')
print(f'Нейтральных: {cnt_all - cnt_neg - cnt_pos}', end = '\n\n')
print('Самые популярные леммы в позитивных отзывах и количество их употреблений:')
print_dict(dict_pos)
print('Самые популярные леммы в негативных отзывах:')
print_dict(dict_neg)

