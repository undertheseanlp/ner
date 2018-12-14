def convert_sentence(sentence):
    words = sentence.split("\n")
    words_ = []
    for word in words:
        tokens = word.split("\t")
        syllables, tag = tokens[0].split(), tokens[3]
        if not tag.startswith("B-"):
            for syllable in syllables:
                word = " ".join([syllable, tag])
                words_.append(word)
        else:
            for i, syllable in enumerate(syllables):
                if i == 0:
                    word = " ".join([syllable, tag])
                    words_.append(word)
                else:
                    tag = tag.replace("B-", "I-")
                    word = " ".join([syllable, tag])
                    words_.append(word)
    sentence_ = "\n".join(words_)
    return sentence_


def check_sentence(sentence):
    words = sentence.split("\n")
    for word in words:
        tokens = word.split("\t")
        if len(tokens) != 4:
            print("Sentence error ")
            print(sentence)
            return False
    return True


def convert_dataset(inpath, outpath):
    content = open(inpath).read()
    sentences = content.split("\n\n")
    sentences = [convert_sentence(s) for s in sentences if check_sentence(s)]
    content_ = "\n\n".join(sentences)
    f = open(outpath, "w")
    f.write(content_)
    print(f"Output file is saved in {outpath}")


convert_dataset("data/train.txt", "data1/train.txt")
convert_dataset("data/dev.txt", "data1/dev.txt")
convert_dataset("data/test.txt", "data1/test.txt")
