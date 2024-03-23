import nltk

nf ='test_tokrus.txt'
f = open(nf,"r")
sent = f.read()
words = nltk.word_tokenize(sent) 
print(words) 
print() 