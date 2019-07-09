# Nhận dạng thực thể tên riêng tiếng Việt

![](https://img.shields.io/badge/made%20with-%E2%9D%A4-red.svg)
![](https://img.shields.io/badge/opensource-vietnamese-blue.svg)
![](https://img.shields.io/badge/build-passing-green.svg)

Dự án nghiên cứu về bài toán *nhận dạng thực thể tên riêng tiếng Việt*, được phát triển bởi nhóm nghiên cứu xử lý ngôn ngữ tự nhiên tiếng Việt - [underthesea](https://github.com/undertheseanlp). Chứa mã nguồn các thử nghiệm cho việc xử lý dữ liệu, huấn luyện và đánh giá mô hình, cũng như cho phép dễ dàng tùy chỉnh mô hình đối với những tập dữ liệu mới.

**Nhóm tác giả** 

* Vũ Anh ([anhv.ict91@gmail.com](anhv.ict91@gmail.com))
* Bùi Nhật Anh ([buinhatanh1208@gmail.com](buinhatanh1208@gmail.com))

**Tham gia đóng góp**

 Mọi ý kiến đóng góp hoặc yêu cầu trợ giúp xin gửi vào mục [Issues](../../issues) của dự án. Các thảo luận được khuyến khích **sử dụng tiếng Việt** để dễ dàng trong quá trình trao đổi. 
 
Nếu bạn có kinh nghiệm trong bài toán này, muốn tham gia vào nhóm phát triển với vai trò là [Developer](https://github.com/undertheseanlp/underthesea/wiki/H%C6%B0%E1%BB%9Bng-d%E1%BA%ABn-%C4%91%C3%B3ng-g%C3%B3p#developercontributor), xin hãy đọc kỹ [Hướng dẫn tham gia đóng góp](https://github.com/undertheseanlp/underthesea/wiki/H%C6%B0%E1%BB%9Bng-d%E1%BA%ABn-%C4%91%C3%B3ng-g%C3%B3p#developercontributor).

## Mục lục

* [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
* [Thiết lập môi trường](#thiết-lập-môi-trường)
* [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng)
  * [Sử dụng mô hình đã huấn luyện](#sử-dụng-mô-hình-đã-huấn-luyện)
  * [Huấn luyện mô hình](#huấn-luyện-mô-hình) 
* [Kết quả thử nghiệm](#kết-quả-thử-nghiệm)
* [Trích dẫn](#trích-dẫn)
* [Bản quyền](#bản-quyền)

## Yêu cầu hệ thống 

* `Hệ điều hành: Linux (Ubuntu, CentOS), Mac`
* `Python 3.6+`
* `conda 4+`

## Thiết lập môi trường

Tải project bằng cách sử dụng lệnh `git clone`

```
$ git clone https://github.com/undertheseanlp/ner.git
```

Tạo môi trường mới và cài đặt các gói liên quan

```
$ cd classification
$ conda create -n ner python=3.6
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

## Kết quả thử nghiệm

Dữ liệu VLSP 2016: mức từ (không dùng nhãn gold POS, Chunk)

<table>
  <tr>
    <th>Mô hình</th>
    <th>F1 (%)</th>
    <th>Thời gian train</th>
  </tr>
  <tr>
     <td>BiLSTM-CRF (20 epoch)</td>
     <td><b>66.39</b></td>
     <td>3.46 giờ</td>
  </tr>
</table>

Dữ liệu VLSP 2016: mức syllable

<table>
  <tr>
    <th>Mô hình</th>
    <th>F1 (%)</th>
    <th>Thời gian train</th>
  </tr>
  <tr>
     <td>flair (WordEmbedding(word_dim=300) + CharacterEmbedding, SequenceTagger(<code>hidden_size=1024</code>), learning_rate=0.1, mini_batch_size=8)</td>
     <td><b>86.68</b></td>
     <td></td>
  </tr>
   <tr>
     <td>flair (WordEmbedding(word_dim=300,<code>corpus=19GB</code>) + CharacterEmbedding, SequenceTagger(hidden_size=1024), learning_rate=0.1, mini_batch_size=8)</td>
     <td>86.46</td>
     <td></td>
  </tr>
   <tr>
     <td>flair (WordEmbedding(word_dim=300) + <code>CharacterEmbedding</code>, learning_rate=0.1, mini_batch_size=8)</td>
     <td>84.74</td>
     <td></td>
  </tr>
   <tr>
     <td>flair (WordEmbedding(<code>word_dim=300</code>), learning_rate=0.1, mini_batch_size=8)</td>
     <td>84.37</td>
     <td>2 giờ 15 phút</td>
  </tr>
   <tr>
     <td>flair (<code>WordEmbedding(word_dim=100)</code>, learning_rate=0.1, mini_batch_size=8)</td>
     <td>82.30</td>
     <td>3 giờ 13 phút</td>
  </tr>
  <tr>
     <td>flair (<code>Character Embeddings</code>, learning_rate=0.1, mini_batch_size=16)</td>
     <td>67.45</td>
     <td>5 giờ 34 phút</td>
  </tr>
</table>

