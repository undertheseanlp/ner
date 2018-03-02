from os.path import dirname, join

import os
from languageflow.flow import Flow
from languageflow.model import Model
from languageflow.model.crf import CRF
from languageflow.transformer.tagged import TaggedTransformer
from languageflow.validation.validation import TrainTestSplitValidation

from load_data import load_data

from utils.scorer import iob_score

if __name__ == '__main__':
    # =========================================================================#
    # Start an experiment with flow
    # =========================================================================#
    flow = Flow()
    flow.log_folder = join(dirname(__file__), "logs")

    # =========================================================================#
    #                               Data
    # =========================================================================#

    # for saving model
    sentences = []
    for f in ["train.txt", "dev.txt", "test.txt"]:
        file = join(dirname(dirname(dirname(__file__))), "data", "vlsp2016", "corpus", f)
        sentences.append(load_data(file))
    train_sentences = sentences[0] + sentences[1]
    test_sentences = sentences[2]
    train_sentences = train_sentences

    # flow.data(sentences=sentences)

    # =========================================================================#
    #                                Transformer
    # =========================================================================#
    template = [
        "T[-2].lower", "T[-1].lower", "T[0].lower", "T[1].lower", "T[2].lower",
        "T[0].istitle", "T[-1].istitle", "T[1].istitle", "T[-2].istitle", "T[2].istitle",
        # word unigram and bigram
        "T[-2]", "T[-1]", "T[0]", "T[1]", "T[2]",
        "T[-2,-1]", "T[-1,0]", "T[0,1]", "T[1,2]",
        # pos unigram and bigram
        "T[-2][1]", "T[-1][1]", "T[0][1]", "T[1][1]", "T[2][1]",
        "T[-2,-1][1]", "T[-1,0][1]", "T[0,1][1]", "T[1,2][1]",
        # ner
        "T[-3][3]", "T[-2][3]", "T[-1][3]",
    ]
    transformer = TaggedTransformer(template)

    # flow.transform(transformer)
    X_train, y_train = transformer.transform(train_sentences)
    X_test, y_test = transformer.transform(test_sentences)


    # =========================================================================#
    #                               Models
    # =========================================================================#
    parameters = {
        'c1': 1.0,  # coefficient for L1 penalty
        'c2': 1e-3,  # coefficient for L2 penalty
        'max_iterations': 1000,  #
        # include transitions that are possible, but not observed
        'feature.possible_transitions': True
    }
    filename = join(dirname(__file__), 'model', 'crf.model')
    estimator = CRF(params=parameters, filename=filename)
    estimator.fit(X_train, y_train)


    # =========================================================================#
    #                              Evaluation
    # =========================================================================#
    y_pred = estimator.predict(X_test)
    f1_score = iob_score(y_test, y_pred)
    print(f1_score)
