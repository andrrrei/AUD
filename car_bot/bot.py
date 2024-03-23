from nltk.tokenize import word_tokenize
import pymorphy3
import random
from nltk.corpus import stopwords

# Importing stop words
stop_words = set(stopwords.words('russian'))


# Function to load car features from a file
def load_car_features(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        features = {}
        current_category = None
        for line in file:
            line = line.strip()
            if line:
                if ':' not in line:
                    current_category = line
                else:
                    key, value = line.split(': ')
                    if current_category not in features:
                        features[current_category] = {}
                    features[current_category][key] = value
    return features


# Function to preprocess a sentence
def preprocess(sentence):
    tokens = word_tokenize(sentence, language='russian')
    tokens = [token for token in tokens if token.lower() not in stop_words and token.isalnum()]
    morph = pymorphy3.MorphAnalyzer()
    lemmatized_tokens = [morph.parse(token)[0].normal_form for token in tokens]
    return lemmatized_tokens


# Function to extract bigrams from tokens
def extract_bigrams(tokens):
    bigrams = [(tokens[i], tokens[i+1]) for i in range(len(tokens)-1)]
    return bigrams


# Function to preprocess a sentence and extract bigrams
def preprocess_bigram(sentence):
    tokens = word_tokenize(sentence, language='russian')
    tokens = [token for token in tokens if token.lower() not in stop_words and token.isalnum()]
    morph = pymorphy3.MorphAnalyzer()
    lemmatized_tokens = [morph.parse(token)[0].normal_form for token in tokens]
    return extract_bigrams(lemmatized_tokens)


# Function to calculate Jaccard similarity between two sets
def calculate_jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1) + len(set2) - intersection
    similarity = intersection / union if union != 0 else 0
    return similarity


# Function to extract features based on a question
def extract_features(question, car_features):
    extracted_features = []
    question_bigrams = set(preprocess(question))
    best_match = None
    best_similarity = 0.0

    for category, attributes in car_features.items():
        for key, value in attributes.items():
            key_bigrams = set(preprocess(key))
            similarity = calculate_jaccard_similarity(question_bigrams, key_bigrams)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = attributes, key

    if best_match is not None:
        attributes, key = best_match
        extracted_features.append(f"-> {key}: {attributes[key]}\n")
    return extracted_features


# Function to generate response to a question
def answer_question(question, car_features):
    extracted_features = extract_features(question, car_features)

    intro = [
        "Вот что я могу рассказать об этом",
        "Позвольте мне поделиться информацией по этому вопросу",
        "Давайте обсудим, что я знаю на этот счет",
        "Если вы интересуетесь этим вопросом, вот что у меня есть для Вас"
    ]

    apologises = [
        "Прошу прощения, но я не в состоянии найти ответ на ваш запрос",
        "К сожалению, я не способен предоставить информацию по вашему вопросу",
        "Извините, но я не обладаю данными, связанных с вашим запросом",
        "Прошу прощения, но я не располагаю необходимой информацией для ответа на ваш вопрос",
        "Извините, не могу найти информацию по вашему вопросу"
    ]

    if extracted_features:
        response = f"\n{random.choice(intro)} \n{''.join(extracted_features)}"
        return response
    else:
        return random.choice(apologises)


# Main function to interact with the user
def main():
    file_path = 'features.txt'
    car_features = load_car_features(file_path)

    print("\nЗдравствуйте! Меня зовут Степа, и я могу рассказать о всех характеристиках Porcshe 911 GT3 RS 2022. Задавайте вопросы или скажите 'выход' для завершения.")
    
    while True:
        user_input = input("\nВаш вопрос: ")
        if user_input.lower() == 'выход':
            print('До новых встреч!')
            break
        response = answer_question(user_input, car_features)
        print(response)


if __name__ == "__main__":
    main()

