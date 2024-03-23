import nltk
nf ='test_tokrus.txt'
f = open(nf,"r")
sentences = nltk.sent_tokenize(f.read()  , language="russian")
i = 1
for sentence in sentences: 
    print(i, '  ',sentence)
    i += 1
