# Vietnamese Named Entity Recognition ![](https://img.shields.io/badge/F1-88.6%25-red.svg)

[[English](README.md)] [[Vietnamese](README.vi.md)]

This repository contains starter code for training and evaluating machine learning models in *Vietnamese Named Entity Recognition* problem. It is a part of [underthesea](https://github.com/magizbox/underthesea) project. The code gives an end-to-end working example for reading datasets, training machine learning models, and evaluating performance of the models. It can easily be extended to train your own custom-defined models. 

## Table of contents

* [1. Installation](#1-installation)
  * [1.1 Requirements](#11-requirements)
  * [1.2 Download and Setup Environment](#12-download-and-setup-environment)
* [2. Usage](#2-usage)
  * [2.1 Using a pretrained model](#21-using-a-pretrained-model)
  * [2.2 Train a new dataset](#22-train-a-new-dataset)
  * [2.3 Sharing a model](#23-sharing-a-model)
* [3. References](#3-references)

## 1. Installation

### 1.1 Requirements

This code is writen in python. The dependencies are:

* `Operating Systems: Linux (Ubuntu, CentOS), Mac`
* `Python 3.6`
* `Anaconda`

Python Packages

* `underthesea==1.1.7`
* `languageflow==1.1.7`

### 1.2 Download and Setup Environment

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

### 2.1 Using a pretrained model


```
cd ner
$ source activate ner
$ python ner.py -fin tmp/input.txt -fout tmp/output.txt
```

### 2.2 Train a new dataset

Prepare a new dataset

Train and test

```
$ cd ner
$ source activate ner
$ python train.py
  --train data/vlsp2018/corpus/train.txt
```

### 2.3 Sharing a model

To be updated

## 3. References

To be updated

Last update: 05/2018
