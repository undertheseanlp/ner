# Vietnamese Named Entity Recognition ![](https://img.shields.io/badge/F1-88.6%25-red.svg)

[[English](README.md)] [[Vietnamese](README.vi.md)]

This repository contains experiments in **Vietnamese Named Entity Recognition** problem. It is a part of [underthesea](https://github.com/magizbox/underthesea) project.

## Tables of contents

# [1. Installation](#1.-installation)
  # [Requirements](#requirements)
  # [Download and Setup Environement](#download-and-setup-environment)
* [2. Usage](#2.-usage)
  * [Using a pretrained model](#using-a-pretrained-model)
  * [Train a new dataset](#train-a-new-dataset)
  * [Sharing a model](#sharing-a-model)
* [3. References](#3.-references)

## 1. Installation

### Requirements

* `Operating Systems: Linux (Ubuntu, CentOS), Mac`
* `Python 3.5+`
* `conda 4+`

Python Packages

* `underthesea==1.1.7`
* `languageflow==1.1.7`

### Download and Setup Environment

Clone project using git

```
$ git clone https://github.com/undertheseanlp/ner.git
```

Create environment and install requirements

```
$ cd ner
$ conda create -n uts.ner python=3.5
$ pip install -r requirements.txt
```

## 2. Usage

### Using a pretrained model

```
cd ner
$ source activate ner
$ python ner.py -fin tmp/input.txt -fout tmp/output.txt
```

### Train a new dataset

Prepare a new dataset

Train and test

```
$ cd ner
$ source activate ner
$ python train.py
  --train data/vlsp2018/corpus/train.txt
```

### Sharing a model

To be updated

## 3. References

To be updated

Last update: 05/2018