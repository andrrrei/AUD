import nltk
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Function to get stems of English words with SnowballStemmer
def get_stems_en(text):
    if not text:
        return []
    
    stemmer = SnowballStemmer("english")
    words = word_tokenize(text)
    stems = [stemmer.stem(w) for w in words]
    return stems

# Function to get stems of Russian words with SnowballStemmer
def get_stems_rus(text):
    if not text:
        return []
    
    stemmer = SnowballStemmer("russian")
    words = word_tokenize(text)
    stems = [stemmer.stem(w) for w in words]
    return stems

# Function to get lemmas of words with WordNetLemmatizer
def get_lemmas(text):
    if not text:
        return []

    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text)
    lemmas = [lemmatizer.lemmatize(w) for w in words]
    return lemmas


def main():
    # Read Russian and English texts from files
    rus_text = open('idiot_rus.txt').read()
    en_text = open('idiot_en.txt').read()
    
    # Get stems of Russian and English texts
    rus_stems = get_stems_rus(rus_text)
    en_stems = get_stems_en(en_text)
    
    print("Stems Ru:", rus_stems)
    print()
    print("Stems En:", en_stems)

    print("Нормализация английского текста: ", get_lemmas(en_text))
    
    # Get stems of some Russian and English words
    rus_stems = get_stems_rus("Крючок, поиск, катушка")
    en_stems = get_stems_en("Window, building, masterpiece")
    
    print("Stems Ru:", rus_stems)
    print()
    print("Stems En:", en_stems)

if __name__ == "__main__":
    main()
