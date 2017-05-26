from os.path import dirname, join

import pycrfsuite
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from underscore import _

from model_building.features.feature import word2features
from model_building.model_profiling import ModelProfiling
from model_building.transformer import Transformer


def parse_sentence(sentence):
    tokens = sentence.split("\n")
    tokens = [t.split() for t in tokens]
    return tokens


def sent2features(sentence, template):
    return [word2features(sentence, i, template) for i in range(len(sentence))]


def sent2label(sentence):
    return [t[-1] for t in sentence]


def convert_cm_to_log(cm, labels, line=5):
    cm = cm.tolist()
    cm = [" ".join([("%-" + str(line) + "s") % labels[index]] + map(lambda i: ("%" + str(line) + "d") % i, row)) for index, row in enumerate(cm)]
    title = " " * (line + 1) + " ".join(map(lambda i: ("%" + str(line) + "s") % i, labels))
    cm.insert(0, title)
    return cm


def load_train_sents():
    filepath = join(dirname(dirname(__file__)), "data", "vi-chunk.train")
    content = open(filepath, "r").read()
    sentences = content.split("\n\n")
    sentences = [parse_sentence(s) for s in sentences]
    return sentences


if __name__ == '__main__':
    sents = load_train_sents()
    transformer = Transformer()
    template = [
        "T[0].lower", "T[-1].lower", "T[1].lower",
        "T[0].istitle", "T[-1].istitle", "T[1].istitle",
        "T[-2]", "T[-1]", "T[0]", "T[1]", "T[2]",  # unigram
        "T[-2,-1]", "T[-1,0]", "T[0,1]", "T[1,2]",  # bigram
        "T[-1][1]", "T[-2][1]", "T[-3][1]",  # dynamic feature
        "T[-3,-2][1]", "T[-2,-1][1]",
        "T[-3,-1][1]"
    ]
    X = [sent2features(s, template) for s in sents]
    y = [sent2label(s) for s in sents]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=10)
    trainer = pycrfsuite.Trainer(verbose=True)
    for xseq, yseq in zip(X_train, y_train):
        trainer.append(xseq, yseq)
    model_params = {
        "name": "CRF",
        "params": {
            'c1': 1.0,  # coefficient for L1 penalty
            'c2': 1e-3,  # coefficient for L2 penalty
            'max_iterations': 1000,  #
            # include transitions that are possible, but not observed
            'feature.possible_transitions': True
        }
    }
    trainer.set_params(model_params["params"])

    profile = ModelProfiling()
    profile.add("data", {"train": len(X_train), "test": len(X_test)})
    profile.add("model", model_params)
    profile.add("template", template)

    model_name = "chunking-crf-model"
    profile.start_train()
    trainer.train(model_name)
    profile.end_train()

    model = pycrfsuite.Tagger()
    model.open(model_name)

    y_test = _.flatten(y_test)
    y_pred = [model.tag(x) for x in X_test]
    y_pred = _.flatten(y_pred)
    labels = list(set(y_test).union(set(y_pred)))

    cm = confusion_matrix(y_test, y_pred, labels)
    cm = convert_cm_to_log(cm, labels)
    score = {
        "accuracy": accuracy_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred, average='weighted'),
        "precision": precision_score(y_test, y_pred, average='weighted'),
        "f1": f1_score(y_test, y_pred, average='weighted')
    }
    profile.add("score", score)
    profile.add("confusion matrix", cm)

    profile.save()
    profile.show()
