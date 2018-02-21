# Nhận dạng thực thể tên riêng tiếng Việt

![](https://img.shields.io/badge/version-1.1.6-blue.svg) ![](https://img.shields.io/badge/build-passing-brightgreen.svg) ![](https://img.shields.io/badge/F1-88.6%25-red.svg)

[[English](README.md)] [[Vietnamese](README.vi.md)]

Trang này chứa các thí nghiệm với bài toán nhận dạng thực thể tên riêng tiếng Việt. Đây là một phần của dự án [underthesea](https://github.com/magizbox/underthesea)

## Kết quả

![](https://img.shields.io/badge/F1-86.6-red.svg)

## Hướng dẫn tự xây dựng mô hình

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
