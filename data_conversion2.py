"""
# data_conversion from vietner
# https://github.com/minhpqn/vietner/blob/ecca645e8a73292f2fa87768d8c550ebeeceaeda/vlsp2018_exp/data_conversion2.py
"""
"""Function for data conversion
"""
import unittest
import re
import os
from collections import OrderedDict
from nltk.tokenize import WordPunctTokenizer
from argparse import ArgumentParser


class Token(object):

    def __init__(self, text, start, end):
        self.text = text
        self.start = start
        self.end = end

    def __repr__(self):
        return str( (self.text, self.start, self.end) )


def remove_xml_tags(entity):
    entity = re.sub(r"<ENAMEX TYPE=\"(.+?)\">", "", entity)
    entity = re.sub(r"</ENAMEX>", "", entity)
    return entity


def tokenize(text):
    tokens = []
    # tokenizer = TreebankWordTokenizer()
    tokenizer = WordPunctTokenizer()

    syllables = tokenizer.tokenize(text)
    syllables = [ '"' if s == "``" or s == "''" else s for s in syllables ]

    _pos = 0
    for s in syllables:
        start = text.find(s, _pos)
        end = start + len(s)
        _pos = end
        syl = Token(s, start, end)
        tokens.append(syl)
    return tokens


def depth_level(astring):
    """
    E.g.,
    Tôi là sinh viên -> 0
    ĐHQG <ENAMEX>Hà Nội</ENAMEX> -> 1
    Khoa thanh nhạc <ENAMEX>Học viên âm nhạc <ENAMEX>HCM</ENAMEX></ENAMEX> -> 2
    Args:
        astring: input string with XML tags
    Returns:
        The depth level of a string
    """
    level = 0
    first = True
    first_add_child = True
    OPEN_TAG = 1
    stack = []
    i = 0
    while i < len(astring):
        # print(astring[i:], stack, level)
        if astring[i:].startswith("<ENAMEX TYPE="):
            if first:
                level += 1
                first = False
            if len(stack) > 0:
                if first_add_child:
                    level += 1
                    first_add_child = False
            stack.append(OPEN_TAG)
            i += len("<ENAMEX TYPE=")
        elif astring[i:].startswith("</ENAMEX>"):
            stack.pop()
            i += len("</ENAMEX>")
        else:
            i += 1
    return level


def get_entities(line):
    """

    Args:
        line (string): Input sentence (single sentence) with XML tags
        E.g., Đây là lý do khiến <ENAMEX TYPE=\"PERSON\">Yoon Ah</ENAMEX> quyết định cắt mái tóc dài 'nữ thần'

    Returns:
        raw (string): raw sentence
        entities (list): list of entities (json object) (Wit.ai)
    """
    debug = False
    raw = ""
    entities = []

    regex_opentag = re.compile(r"<ENAMEX TYPE=\"(.+?)\">")
    regex_closetag = re.compile(r"</ENAMEX>")
    next_start_pos = 0
    match1 = regex_opentag.search(line, next_start_pos)
    stack = []
    if match1:
        raw += line[0:match1.start()]
        next_start_pos = match1.end()
        stack.append(match1)
    else:
        raw = line

    while len(stack) != 0:
        if debug: print("#Current stack", stack)
        match1 = stack.pop()
        if debug: print("#From next_start_pos {}: {}".format(next_start_pos, line[next_start_pos:]))
        next_closetag1 = regex_closetag.search(line, next_start_pos)
        if not next_closetag1:
            print(line)
            raise ValueError("Close tag not found")
        next_end_pos1 = next_closetag1.start()
        match2 = regex_opentag.search(line, next_start_pos, next_end_pos1)
        if match2:
            raw += line[next_start_pos:match2.start()]
            next_start_pos1 = match2.end()
            next_closetag2 = regex_closetag.search(line, next_start_pos1)
            if not next_closetag2:
                raise ValueError("Close tag not found")
            next_end_pos2 = next_closetag2.start()
            match3 = regex_opentag.search(line, next_start_pos1, next_end_pos2)
            if match3:
                level = 1
                raw += line[next_start_pos1:match3.start()]
                next_start_pos2 = match3.end()
                value = line[next_start_pos2:next_end_pos2]
                _type = match3.group(1)

                entity = OrderedDict()
                entity["type"] = _type
                entity["value"] = value
                entity["start"] = len(raw)
                entity["end"] = entity["start"] + len(value)
                entity["level"] = level
                entities.append(entity)

                if debug: print("#Entity:", value, _type, level)
                raw += value
                next_start_pos = next_closetag2.end()
                stack.append(match1)
                stack.append(match2)
            else:
                # Get entity between match2 and next_closetag2
                value = remove_xml_tags( line[match2.end():next_end_pos2] )
                _type = match2.group(1)
                # abc <ENAMEX> xyz <ENAMEX>dhg</ENAMEX> mpq</ENAMEX> r
                level = 1 + depth_level( line[match2.end():next_end_pos2] )
                if debug: print("#current: ", raw)
                raw += line[next_start_pos1:next_closetag2.start()]
                if debug: print("->", raw)
                entity = OrderedDict()
                entity["type"] = _type
                entity["value"] = value
                entity["start"] = len(raw) - len(value)
                entity["end"] = len(raw)
                entity["level"] = level
                entities.append(entity)

                if debug: print("#Entity:", value, _type, level)
                next_start_pos = next_closetag2.end()
                stack.append(match1)
                next_match2 = regex_opentag.search(line, next_start_pos)
                next_closetag3 = regex_closetag.search(line, next_start_pos)

                if next_match2:
                    if next_closetag3 and next_match2.start() < next_closetag3.start():
                        if debug: print("Next match2:", line[next_match2.start():])
                        if debug: print("#current: ", raw)
                        raw += line[next_start_pos:next_match2.start()]
                        if debug: print("->", raw)
                        next_start_pos = next_match2.end()
                        stack.append(next_match2)
        else:
            # Get entity between match1 and next_closetag1
            value = remove_xml_tags( line[match1.end():next_closetag1.start()] )
            _type = match1.group(1)
            level = 1 + depth_level( line[match1.end():next_closetag1.start()] )
            if debug: print("#current: ", raw)
            raw += line[next_start_pos:next_closetag1.start()]
            if debug: print("->", raw)
            entity = OrderedDict()
            entity["type"] = _type
            entity["value"] = value
            entity["start"] = len(raw) - len(value)
            entity["end"] = len(raw)
            entity["level"] = level
            entities.append(entity)
            if debug: print("#Entity:", value, _type, level)
            next_start_pos = next_closetag1.end()

            next_match1 = regex_opentag.search(line, next_start_pos)
            next_closetag3 = regex_closetag.search(line, next_start_pos)
            if next_match1:
                if next_closetag3 and next_match1.start() < next_closetag3.start():
                    if debug: print("#Next match1:", line[next_match1.start():])
                    if debug: print("#current: ", raw)
                    raw += line[next_start_pos:next_match1.start()]
                    if debug: print("->", raw)
                    next_start_pos = next_match1.end()
                    stack.append(next_match1)
                else:
                    continue
            else:
                if debug: print("#current: ", raw)
                if debug: print("{} {}".format(next_closetag1.end(), line[next_closetag1.end():]))
                if not re.search(r"</ENAMEX>", line[next_closetag1.end():]):
                    raw += line[next_closetag1.end():]
                    if debug: print("->", raw)

    return raw, entities


def find_syl_index(start, end, syllables):
    """Find start and end indexes of syllables
    """
    start_syl_id = None
    end_syl_id   = None
    for i, syl in enumerate(syllables):
        if syl.start == start:
            start_syl_id = i
        if syl.end == end:
            end_syl_id = i+1

        if i > 0 and syl.start >= start and syllables[i-1].end <= start:
            start_syl_id = i
        if i == 0 and syl.start > start:
            start_syl_id = i

        if i < len(syllables)-1 and syl.end < end and syllables[i+1].start > end:
            end_syl_id = i+1

        if syl.end >= end and syl.start < end:
            end_syl_id = i+1
        if i == len(syllables)-1 and syl.end <= end:
            end_syl_id = i+1

        if i > 0 and syl.start < start and syllables[i-1].end < start:
            start_syl_id = i

        if syl.start < start and syl.end >= end:
            start_syl_id = i
            end_syl_id = i + 1

        if i == 0 and len(syllables) > 0 and syl.start < start and syl.end < end:
            start_syl_id = i

    if start_syl_id == None:
        print("Cannot find start_syl_id '{}' (end={}) in '{}'".format(start, end, syllables))
    if end_syl_id == None:
        print("Cannot find end_syl_id '{}' (start={}) in '{}'".format(end, start, syllables))

    return start_syl_id, end_syl_id

count = 0

def xml2tokens(xml_tagged_sent):
    global count
    """Convert XML-based tagged sentence into CoNLL format based on syllables
    Args:
        xml_tagged_sent (string): Input sentence (single sentence) with XML tags

    Returns:
        tokens (list): list of tuples (tk, level1_tag, level2_tag)
          level1_tag is entity tag (BIO scheme) at the level 1
          level2_tag is entity tag at the level 2 (nested entity)
    """
    raw, entities = get_entities(xml_tagged_sent)
    if re.search(r"ENAMEX", raw):
        print(xml_tagged_sent)
        print(raw)
        count += 1
    # assert not re.search(r"<ENAMEX", raw), raw

    tokens = tokenize(raw)
    level1_syl_tags = ["O" for i in range(len(tokens))]
    level2_syl_tags = ["O" for i in range(len(tokens))]
    level3_syl_tags = ["O" for i in range(len(tokens))]

    flag = False
    for entity in entities:
        value = entity["value"]
        start = entity["start"]
        end = entity["end"]
        entity_type = entity["type"]
        start_syl_id, end_syl_id = find_syl_index(start, end, tokens)
        if start_syl_id != None and end_syl_id != None:
            if entity["level"] == 1:
                level1_syl_tags[start_syl_id] = "B-" + entity_type
                for i in range(start_syl_id + 1, end_syl_id):
                    level1_syl_tags[i] = "I-" + entity_type
            elif entity["level"] == 2:
                level2_syl_tags[start_syl_id] = "B-" + entity_type
                for i in range(start_syl_id + 1, end_syl_id):
                    level2_syl_tags[i] = "I-" + entity_type
            else:
                level3_syl_tags[start_syl_id] = "B-" + entity_type
                for i in range(start_syl_id + 1, end_syl_id):
                    level3_syl_tags[i] = "I-" + entity_type
        else:
            print("{},{},\"{}\" in '{}' ({})".format(start,end,value,raw,xml_tagged_sent))
            flag = True
    res = list(zip([ tk.text for tk in tokens], level1_syl_tags, level2_syl_tags, level3_syl_tags))
    return res, flag


class TestDataConversion(unittest.TestCase):

    def test_3level_real(self):
        sent = '<ENAMEX TYPE="ORGANIZATION">NDĐT</ENAMEX> – Nhân kỷ niệm 63 năm Ngày Giải phóng Thủ đô (10-10-1954 – 10-10-2017), <ENAMEX TYPE="ORGANIZATION">Khoa Thanh nhạc - <ENAMEX TYPE="ORGANIZATION">Học viện Âm nhạc Quốc gia <ENAMEX TYPE="LOCATION">Việt Nam</ENAMEX></ENAMEX></ENAMEX> tổ chức chương trình nghệ thuật đặc biệt “<ENAMEX TYPE="MISCELLANEOUS">Sóng đàn Hà Nội</ENAMEX>”.'
        print(sent)
        raw, entities = get_entities(sent)
        self.assertFalse(re.search(r"<ENAMEX", raw), raw)
        self.assertFalse(re.search(r"</ENAMEX>", raw), raw)
        print(raw)
        print(entities)
        tokens, flag = xml2tokens(sent)
        print(tokens)

    def test_2level_real(self):
        sent = '<ENAMEX TYPE="ORGANIZATION">Ngân hàng Thương mại Cổ phần Phát triển Nhà <ENAMEX TYPE="LOCATION">TP.HCM</ENAMEX> ABC</ENAMEX> <ENAMEX TYPE="LOCATION">Vĩnh Long</ENAMEX>'
        print(sent)
        raw, entities = get_entities(sent)
        self.assertFalse(re.search(r"<ENAMEX", raw), raw)
        self.assertFalse(re.search(r"</ENAMEX>", raw), raw)
        print(raw)
        print(entities)
        tokens, flag = xml2tokens(sent)
        print(tokens)

    def test_3level_nested(self):
        sent = 'w0 <ENAMEX TYPE="A">w1 <ENAMEX TYPE="B">w2 <ENAMEX TYPE="C">w3</ENAMEX> w4</ENAMEX> w5 <ENAMEX TYPE="D">w6</ENAMEX> w7 w8</ENAMEX> w9'
        sent = '<ENAMEX TYPE="A">w1</ENAMEX> w2 <ENAMEX TYPE="B">w3 <ENAMEX TYPE="C">w4 <ENAMEX TYPE="D">w5</ENAMEX> w6 <ENAMEX TYPE="E">w7</ENAMEX></ENAMEX></ENAMEX> "<ENAMEX TYPE="F">w8</ENAMEX>".'
        print(sent)
        raw, entities = get_entities(sent)
        print(raw)
        print()
        for e in entities:
            print(e)

    def test_2level_nested(self):

        # sent = 'w0 <ENAMEX TYPE="A">w1 <ENAMEX TYPE="B">w2</ENAMEX> w3 <ENAMEX TYPE="C">w4</ENAMEX> w5</ENAMEX>'
        sent = 'w0 <ENAMEX TYPE="A">w1 <ENAMEX TYPE="B">w2</ENAMEX> <ENAMEX TYPE="C">w3</ENAMEX></ENAMEX>'
        print(sent)
        raw, entities = get_entities(sent)
        print(raw)
        for e in entities:
            print(e)

    def test_depth_level(self):
        self.assertEqual(0, depth_level("w1 w2 w3"))
        self.assertEqual(1, depth_level('w0 w1 <ENAMEX TYPE="B">w2</ENAMEX>'))
        self.assertEqual(1, depth_level('w0 w1 <ENAMEX TYPE="B">w2</ENAMEX> <ENAMEX TYPE="B">w2</ENAMEX>'))
        self.assertEqual(2, depth_level('w3 <ENAMEX TYPE="C">w4 <ENAMEX TYPE="D">w5</ENAMEX> w6 <ENAMEX TYPE="E">w7</ENAMEX></ENAMEX>'))


    def test_xml2tokens(self):
        raw = '<ENAMEX TYPE="ORGANIZATION">Ngân hàng Thương mại Cổ phần Phát triển Nhà <ENAMEX TYPE="LOCATION">TP.HCM</ENAMEX> ABC</ENAMEX> <ENAMEX TYPE="LOCATION">Vĩnh Long</ENAMEX>'
        tokens, _ = xml2tokens(raw)
        self.assertTupleEqual( ("Ngân", "O", "B-ORGANIZATION"), tokens[0] )
        print(tokens)
        raw = "Đây là lý do khiến <ENAMEX TYPE=\"PERSON\">Yoon Ah</ENAMEX> quyết định cắt mái tóc dài 'nữ thần'"
        tokens, _ = xml2tokens(raw)
        self.assertTupleEqual( ("Yoon", "B-PERSON", "O"), tokens[5] )

    def test_get_entities(self):
        sent = "Đây là lý do khiến"
        raw, entities = get_entities(sent)
        self.assertEqual("Đây là lý do khiến", raw)
        self.assertTrue(len(entities) == 0)
        sent = "Đây là lý do khiến <ENAMEX TYPE=\"PERSON\">Yoon Ah</ENAMEX> quyết định cắt mái tóc dài 'nữ thần'"
        raw, entities = get_entities(sent)
        self.assertEqual("Đây là lý do khiến Yoon Ah quyết định cắt mái tóc dài 'nữ thần'", raw)
        self.assertTrue(len(entities) == 1)
        entity0 = entities[0]
        print(raw)
        print(entity0)
        self.assertEqual("Yoon Ah", entity0["value"])
        self.assertEqual("PERSON", entity0["type"])
        self.assertEqual(19, entity0["start"])
        self.assertEqual(26, entity0["end"])

        sent = 'Ngoại trưởng <ENAMEX TYPE="LOCATION">Mỹ</ENAMEX> <ENAMEX TYPE="PERSON">Rex Tillerson</ENAMEX> kêu gọi cộng đồng quốc tế ngăn chặn các nước sở hữu vũ khí hạt nhân.'
        raw, entities = get_entities(sent)
        self.assertEqual('Ngoại trưởng Mỹ Rex Tillerson kêu gọi cộng đồng quốc tế ngăn chặn các nước sở hữu vũ khí hạt nhân.',raw)
        entity0 = entities[0]
        print(raw)
        print(entity0)

        sent = '<ENAMEX TYPE="ORGANIZATION">Ngân hàng Thương mại Cổ phần Phát triển Nhà <ENAMEX TYPE="LOCATION">TP.HCM</ENAMEX> ABC</ENAMEX> <ENAMEX TYPE="LOCATION">Vĩnh Long</ENAMEX>'
        raw, entities = get_entities(sent)
        self.assertEqual('Ngân hàng Thương mại Cổ phần Phát triển Nhà TP.HCM ABC Vĩnh Long', raw)
        entity0 = entities[0]
        entity1 = entities[1]
        print(raw)
        print(entity0)
        print(entity1)
        self.assertEqual(raw[entity0["start"]:entity0["end"]], entity0["value"])
        self.assertEqual(raw[entity1["start"]:entity1["end"]], entity1["value"])

    def test_cannot_find_sylid(self):
        sent = "Xôn xao tin '<ENAMEX TYPE=\"PERSON\">Đông Phương Bất Bại</ENAMEX>' <ENAMEX TYPE=\"PERSON\">Trần Kiều Ân</ENAMEX> sắp cưới đàn em"
        raw, entities = get_entities(sent)
        self.assertTrue(len(entities) > 0)
        print(raw)
        print(entities)
        tokens, flag = xml2tokens(sent)
        print(tokens)

        sent = "<ENAMEX TYPE=\"ORGANIZATION\">Da LAB</ENAMEX> - Cuộc đời tuyệt đẹp khi 'có đúng có sai'"
        raw, entities = get_entities(sent)
        print(raw)
        print(entities)
        tokens, flag = xml2tokens(sent)
        print(tokens)

        sent = '\'<ENAMEX TYPE="PERSON">Cavani</ENAMEX> và <ENAMEX TYPE="PERSON">Neymar</ENAMEX> tranh nhau đá penalty nhưng im lặng khi... tính tiền ăn\''
        raw, entities = get_entities(sent)
        print(raw)
        print(entities)
        tokens, flag = xml2tokens(sent)
        print(tokens)

        sent = "'<ENAMEX TYPE=\"LOCATION\">Biển chết</ENAMEX> <ENAMEX TYPE=\"LOCATION\">Trung Quốc</ENAMEX>' hóa nửa hồng, nửa xanh"
        raw, entities = get_entities(sent)
        print(raw)
        print(entities)
        tokens, flag = xml2tokens(sent)
        print(tokens)

        sent = "Trong phần lớn thời gian hiệp hai luôn có 3-4 cái bóng áo xanh vây áp <ENAMEX TYPE=\"PERSON\">\"Ronaldo xứ Nghệ\"</ENAMEX>."
        raw, entities = get_entities(sent)
        print(raw)
        print(entities)
        tokens, flag = xml2tokens(sent)
        print(tokens)
        print()

    def test_tokenize(self):
        tokens = tokenize("Ngân hàng Thương mại Cổ phần Phát triển Nhà TP. HCM")
        print([ tk.text for tk in tokens ])

        tokens = tokenize("Xôn xao tin 'Đông Phương Bất Bại' Trần Kiều Ân sắp cưới đàn em")
        print(tokens)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("data_dir", help = "Path to data directory")
    parser.add_argument("output", help = "Path to output file")
    args = parser.parse_args()

    subdirs = [ d for d in os.listdir(args.data_dir) if os.path.isdir(os.path.join(args.data_dir,d)) ]
    fo = open(args.output, "w", encoding="utf-8")
    for d in subdirs:
        dd = os.path.join(args.data_dir, d)
        files = [ f for f in os.listdir(dd) if os.path.isfile(os.path.join(dd,f)) ]
        for filename in files:
            ff = os.path.join(dd, filename)
            with open(ff, "r") as f:
                for line in f:
                    line = line.strip()
                    line = line.strip(u"\ufeff")
                    line = line.strip(u"\u200b\u200b\u200b\u200b\u200b\u200b\u200b")
                    if line == "":
                        continue
                    tokens, flag = xml2tokens(line)
                    if flag:
                        print("File: {}".format(ff))
                        print()
                    for tp in tokens:
                        fo.write("{}\n".format(" ".join(tp)))
                    fo.write("\n")
    fo.close()

# Run
# python data_conversion2  tmp/vlsp2018/VLSP2018-NER-train-Jan14 tmp/train.txt
# python data_conversion2  tmp/vlsp2018/VLSP2018-NER-dev tmp/dev.txt
# python data_conversion2 tmp/vlsp2018/VLSP2018-NER-Test-Domains tmp/test.txt
