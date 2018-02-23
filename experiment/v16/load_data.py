from languageflow.reader.tagged_corpus import TaggedCorpus


def load_data(file):
    tagged_corpus = TaggedCorpus()
    tagged_corpus.load(file)
    sentences = tagged_corpus.sentences
    return sentences


