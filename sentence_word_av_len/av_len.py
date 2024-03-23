import nltk

# Sentence Tokenization function
def my_sent_tokenize(filename):
    with open(filename, 'r') as f:
        text = f.read()
    text = text.replace('ё', 'е').replace('Ё', 'Е').replace('»', '').replace('«', '').replace('...', 'λ.')
    # Tokenize sentences using NLTK
    sentences = nltk.sent_tokenize(text, language='russian')

    size = len(sentences)
    i = 0
    while i < size - 1:
        if not (sentences[i + 1][0].strip().isalpha() and sentences[i + 1][0].strip().isupper()):
            sentences[i] = sentences[i].rstrip() + ' ' + sentences[i + 1].lstrip()
            sentences.pop(i + 1)
            size -= 1
        else:
            i += 1

    for i in range(len(sentences)):
        sentences[i] = sentences[i].replace('λ.', '...')
    
    return sentences


# Function to count Russian words
def russian_words(word_len, count, lst):
    correct_symbols = 'йцукенгшщзхъфывапролджэячсмитьбю-.'
    
    for i in lst:
        check = True
        # Check if word contains only valid symbols
        for c in i:
            if c not in correct_symbols:
                check = False
                break
        if check:
            word_len += len(i) - i.count('.')
            count += 1
    return word_len, count


# Word Tokenization function
def my_word_tokenize(text):
    punctuation = ',./;[]:?><!@#$%^&*()_-'
    # Remove punctuation
    for c in punctuation:
        text = text.replace(c, '')
    lst = nltk.word_tokenize(text.lower())
    return lst


sentences = my_sent_tokenize('ex.txt')
with open('output.txt', 'w') as f:
    sent_len = 0
    word_len = 0
    count = 0
    # Process each sentence
    for i, sentence in enumerate(sentences):
        words = my_word_tokenize(sentence)
        word_len, count = russian_words(word_len, count, words)
        # Write sentence and its length to output file
        print(f'{i + 1}. {sentence} Длина: {len(words)}', file=f)
        sent_len += len(words)

    # Calculate and write average sentence and word lengths to output file
    print(file=f)
    print('Средняя длина предложения: ', '{:.3f}'.format(sent_len / len(sentences)), file=f)
    print('Средняя длина русского слова: ', '{:.3f}'.format(word_len / count), file=f)
