from os.path import dirname
from underthesea.corpus import PlainTextCorpus, join, mkdir
import re
# from pipelines.data_preparation.corpus import TaggedCorpus, TaggedWord, TaggedSentence, TaggedDocument
import random

raw_folder = join(dirname(dirname(dirname(__file__))), "data", "raw", "version 2")
ud_file = join(dirname(dirname(dirname(__file__))), "data", "ud", "vi_ud_no_comment.conllu")
dev_file = join(dirname(dirname(dirname(__file__))), "data", "ud", "dev.conllu")
test_file = join(dirname(dirname(dirname(__file__))), "data", "ud", "test.conllu")
# sample_ud_file = join("sample", "sample_vi_ud.conllu")
# ud_file = sample_ud_file


def extract_tokens(text):
    matched = re.match("(.*)/(.*)", text, re.UNICODE)
    return [matched.group(1), matched.group(2)]


if __name__ == '__main__':
    corpus = PlainTextCorpus()
    corpus.load(raw_folder)
    tagged_corpus = TaggedCorpus()
    tagged_documents = []
    documents = corpus.documents
    # documents = random.sample(documents, 10)
    for document in documents:
        sentences = []
        for sentence in document.sentences:
            tagged_tokens = sentence.split()
            tagged_words = [extract_tokens(token) for token in tagged_tokens]
            tagged_words = [TaggedWord(tagged_word[0].replace("_", " "), tagged_word[1]) for tagged_word in
                            tagged_words]
            sentence = TaggedSentence(tagged_words)
            if len(sentence.words) > 0:
                sentences.append(sentence)
        tagged_document = TaggedDocument(sentences)
        tagged_document.id = document.id
        tagged_documents.append(tagged_document)
    tagged_corpus.documents = tagged_documents
    n = int(0.8 * len(tagged_documents))
    tagged_corpus.documents = tagged_documents[:n]
    tagged_corpus.save(dev_file, comment=False)
    tagged_corpus.documents = tagged_documents[n:]
    tagged_corpus.save(test_file, comment=False)
