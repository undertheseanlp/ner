def extract_tags(line):
    texts = [text.split("\t") for text in line]
    tokens = [text[0] for text in texts]
    tags = [text[-1] for text in texts]
    return tokens, tags

f = open("data/train.txt")
lines = f.read().split("\n\n")
lines = [line.split("\n") for line in lines][:10]
training_data = [extract_tags(line) for line in lines]

f = open("data/test.txt")
lines = f.read().split("\n\n")
lines = [line.split("\n") for line in lines][:3]
test_data = [extract_tags(line) for line in lines]