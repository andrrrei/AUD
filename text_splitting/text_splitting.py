def split_sentences(text):
    sentences = []
    sentence = ''

    # Iterate through each character in the text
    for i in range(len(text)):
        sentence += text[i]
        
        # Check if the current character is a sentence-ending punctuation mark
        if text[i] in '.?!':
            if (i == len(text) - 1) or (text[i:i+3] == '...') or \
                    (text[i + 1] == ' ' and text[i + 2].isupper()):
                sentences.append(sentence.strip())
                sentence = ''
   
    return sentences

with open('test_rus.txt') as f:
    text = f.read()

sentences = split_sentences(text)

# Print each sentence with its index
for i, sentence in enumerate(sentences):
    print(f"{i + 1}. {sentence}")
