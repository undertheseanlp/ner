# Nhận dạng thực thể tên riêng tiếng Việt

![](https://img.shields.io/badge/version-1.1.6-blue.svg) ![](https://img.shields.io/badge/build-passing-brightgreen.svg) ![](https://img.shields.io/badge/F1-88.6%25-red.svg)

[[English](README.md)] [[Vietnamese](README.vi.md)]

Trang này chứa các thí nghiệm với bài toán nhận dạng thực thể tên riêng tiếng Việt. Đây là một phần của dự án [underthesea](https://github.com/magizbox/underthesea)

* [Demo](http://magizbox.com:9386)
* [Detail Reports](https://docs.google.com/spreadsheets/d/1OTd_bktaGpnLSy2I8GiFT2xhElRPymoDjPvqt4cAmc0/edit?usp=sharing)

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

# Hướng dẫn tự xây dựng mô hình

**Bước 1: Tạo dự án**

Cài đặt môi trường

```
# clone project
$ git clone git@github.com:magizbox/underthesea.ner.git

# create environment
$ cd underthesea.ner
$ conda create -n ner python=3.5
$ pip install -r requirements.txt
```

Chạy thử chương trình

```
$ cd ner
$ source activate ner
$ python main.py
```

**Bước 2: Chuẩn bị dữ liệu**

**Bước 3: Xây dựng mô hình**

**Bước 4: Tích hợp vào underthesea**

**Bước 5: Xây dựng demo**

Cập nhật lần cuối: Tháng 2 năm 2018
