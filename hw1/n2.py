def split_sentences(text):
    sentences = []
    sentence = ''

    for i in range(len(text)):
        sentence += text[i]
        if text[i] in '.?!':
            if (i == len(text) - 1) or (text[i] + text[i + 1] + text[i + 2] == '...') or (text[i + 1] == ' ' and text[i + 2].isupper()):
                sentences.append(sentence.strip())
                sentence = ''
   
    return sentences

f = open('test_rus.txt')
text = f.read()
sentences = split_sentences(text)
for i in range(len(sentences)):
    print(i + 1, '. ', sentences[i], sep = '')


# Программа будет работать правильно не для каждого текста. Например, если в тексте есть инициалы, 
# они будут разделяться на предложения

