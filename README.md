# Named Entity Recognition Experiments

This repository contains experiments in Vietnamese NER problems. It is a part of [underthesea](https://github.com/magizbox/underthesea) project.

## Corpus Summary

Corpus is in [UniversalDependencies format](https://github.com/UniversalDependencies/UD_Vietnamese).

```
Sentences     : 14861
Unique words  : 18123
Top words     : ,, ., ", của, là, một, và, có, được, người, không, đã, những, cho, ..., ở, :, trong, đến, “
POS Tags (36) : A, Ab, B-NP, C, CH, Cb, Cc, E, FW, Fw, I, I-NP, L, M, N, NNP, NNPY, NPP, Nb, Nc, Ne, Ni, Ns, Nu, Ny, O, P, Pp, R, T, V, Vb, Vy, X, Z, p
Chunking Tags (14) : B-AP, B-EP, B-IP, B-MP, B-NP, B-NPb, B-PP, B-VP, B-VPb, I-AP, I-NP, I-RP, I-VP, O
NER Tags (9) :B-LOC, B-MISC, B-ORG, B-PER, I-LOC, I-MISC, I-ORG, I-PER, O
```

## Reports

![](https://img.shields.io/badge/f1-88.6%25-red.svg)

* [Detail Reports](https://docs.google.com/spreadsheets/d/1OTd_bktaGpnLSy2I8GiFT2xhElRPymoDjPvqt4cAmc0/edit?usp=sharing)

## Usage

**Setup Environment**

```
# clone project
$ git clone git@github.com:magizbox/underthesea.ner.git

# create environment
$ cd underthesea.ner
$ conda create -n underthesea.ner python=3.4
$ pip install -r requirement.txt
```

**Run experiment**

```
$ source activate underthesea.ner
$ cd underthesea.ner
$ python main.py
```

## Related Works

* [Vietnamese Named Entity Recognition Tools](https://github.com/magizbox/underthesea/wiki/Vietnamese-NLP-Tools#named-entity-recognition)
* [Vietnamese Named Entity Recognition Publications](https://github.com/magizbox/underthesea/wiki/Vietnamese-NLP-Publications#named-entity-recognition)
* [Vietnamese Named Entity Recognition State of The Art](https://github.com/magizbox/underthesea/wiki/Vietnamese-NLP-SOTA#named-entity-recognition)
* [Vietnamese Named Entity Recognition Service](https://github.com/magizbox/underthesea/wiki/Vietnamese-NLP-Services#named-entity-recognition)

Last update: October 2017
