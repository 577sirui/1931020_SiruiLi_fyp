sentiment_words = []

with open("new_corpus05.txt", "r", encoding="utf-8") as f:
    words05 = [line.strip() for line in f]

for x in words05:
    sentiment_words.append(x)
print("05 finished")

with open("new_corpus11.txt", "r", encoding="utf-8") as f:
    words11 = [line.strip() for line in f]

for x in words11:
    sentiment_words.append(x)
print("11 finished")

with open("new_corpus12.txt", "r", encoding="utf-8") as f:
    words12 = [line.strip() for line in f]

for x in words12:
    sentiment_words.append(x)
print("12 finished")

#sentiment_set = set(sentiment_words)

with open('new_corpus.txt','w') as f:
    for word in sentiment_words:
        f.write(word + "\n")