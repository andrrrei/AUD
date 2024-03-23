from collections import Counter
import pymorphy3
from nltk.corpus import stopwords

morph = pymorphy3.MorphAnalyzer()

# Function to check if a word is a service word (preposition, conjunction, particle, interjection)
def service_word(word):
    p = morph.parse(word)[0]
    if 'PREP' in p.tag or 'CONJ' in p.tag or 'PRCL' in p.tag or 'INTJ' in p.tag:
        return True
    return False

with open('text.txt', 'r', encoding='utf-8') as f:
    # Read the text from the file, convert to lowercase, remove commas, and split into words
    text = f.read().lower()
    text = text.replace(',', '')
    words = text.split()

# Count the occurrences of each word, excluding service words
word_count = Counter(word for word in words if not service_word(word))

# Find the most common word and its frequency
most_common_word, frequency = word_count.most_common(1)[0]

print(f'Most common word form: {most_common_word} (occurs {frequency} times)')
