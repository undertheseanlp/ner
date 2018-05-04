import os
from os.path import join
import re
from underthesea.word_sent.regex_tokenize import tokenize


def sentence_segmenter(text):
    text = tokenize(text)
    # 'Con mèo kêu gâu gâu . Con chó kêu meo meo .'

    sentences = re.split(r" \. ?", text)
    sentences = [s for s in sentences if s != ""]
    return sentences


def extract_sentences(file):
    content = open(file, "r").read()
    sentences = []
    sentences_ = content.split("\n")
    sentences_ = [s for s in sentences_ if s != ""]
    for s in sentences_:
        sentences += sentence_segmenter(s)
    return sentences

files = []
train_folder = "./raw/VLSP2018-NER-train-Jan14"
folders = os.listdir(train_folder)
for folder in folders:
    files_ = os.listdir(join(train_folder, folder))
    files_ = [join(train_folder, folder, file) for file in files_]
    files += files_
sentences = []
print("There are", len(files), "documents.")
for file in files:
    sentences += extract_sentences(file)
content = "\n".join(sentences)
with open("./corpus/train.txt", "w") as f:
    f.write(content)
print("There are", len(sentences), "sentences.")
