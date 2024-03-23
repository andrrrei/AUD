from nltk.tokenize import regexp_tokenize

s = "Good"
d = "He bought muffins in 12 september 2023. They are out of date."

print(regexp_tokenize(s, '\s', gaps=True))  # Splitting by whitespace into words
print(regexp_tokenize(s, '[,\.\?!"]\s*', gaps=True))  # Splitting into sentences
print(regexp_tokenize(s, '[A-Z]\w+', gaps=False))  # Extracting words starting with capital letters
