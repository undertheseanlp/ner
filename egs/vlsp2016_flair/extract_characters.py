from collections import Counter

from flair.data import Dictionary

# Flair Characters
chars = Dictionary.load('common-chars')
flair_characters = sorted([b.decode("utf-8") for b in chars.idx2item])
content = "\n".join(flair_characters)
f = open("characters_flair.txt", "w")
f.write(content)

# Corpus Characters
files = [
    "data1/train.txt",
    "data1/dev.txt",
    "data1/test.txt"
]

characters = Counter()
for file in files:
    for line in open(file):
        if line.strip():
            c = Counter(line.strip().split()[0])
            characters += c
corpus_characters = sorted([c for c, n in characters.most_common()])
content = "\n".join(corpus_characters)
f = open("characters_corpus.txt", "w")
f.write(content)

# Merge characters
characters = sorted(set(corpus_characters).union(set(flair_characters)))
content = "\n".join(characters)
f = open("characters_merged.txt", "w")
f.write(content)

