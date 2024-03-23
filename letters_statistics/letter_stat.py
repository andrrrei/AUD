import matplotlib.pyplot as plt
import seaborn as sns

def count_symbols(filename):

    with open(filename, 'r') as f:
        s = f.read()  
    s = s.lower()  
    s = s.replace('ё', 'е')  
    
    # Initialize a dictionary to count letter occurrences
    d = dict.fromkeys([chr(c) for c in range(ord('а'), ord('я') + 1)], 0)

    for letter in s:
        if letter.isalpha(): 
            d[letter] += 1
    
    d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}
    
    k = 1
    for letter, count in d.items():
        print(f'{k}) {letter} - {count}')
        k += 1

    # Plot a bar chart showing letter frequencies
    plt.bar(d.keys(), d.values(), alpha=0.5, color='orange')
    plt.xlabel('letters', fontsize=10)
    plt.ylabel('frequency', fontsize=10)
    plt.show()

    # Select top 10 letters and group others
    d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}
    count = 10
    keys_ = list(d.keys())[:count]
    values_ = list(d.values())[:count]
    d1 = dict(zip(keys_, values_))
    d1['другие'] = sum(list(d.values())[count:])
    
    # Plot a pie chart showing the most popular letters
    plt.pie(d1.values(), labels=d1.keys(), autopct='%.0f%%', labeldistance=1.1, 
            colors=sns.color_palette('tab20c'), shadow=True)
    plt.title(label="Наиболее популярные буквы", fontdict={"fontsize": 16}, pad=20)
    plt.axis('equal')
    plt.show()

count_symbols('task1.txt')
