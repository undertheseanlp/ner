from os import listdir
from os.path import join
import re


class BratDocument:
    def __init__(self, text, annotations):
        self.text = text
        self.annotations = annotations


def muc_to_brat(muc_document):

    text = ""
    annotations = []
    muc_position = 0
    markers = []
    for match in re.finditer("<ENAMEX TYPE=\".*?\">|</ENAMEX>", muc_document):
        muc_start_tag, muc_end_tag = match.regs[0]
        tag = muc_document[muc_start_tag:muc_end_tag]
        text += muc_document[muc_position:muc_start_tag]
        # START TAG
        if tag.startswith("<ENAMEX"):
            tag_matched = re.match("<ENAMEX TYPE=\"(?P<tag>.*?)\">", tag)
            tag_name = tag_matched.group("tag")
            brat_start_tag = len(text)
            markers.append((tag_name, brat_start_tag))
        # END TAG
        else:
            tag_name, brat_start_tag = markers.pop()
            brat_end_tag = len(text)
            annotations.append((tag_name, brat_start_tag, brat_end_tag))


        muc_position = muc_end_tag
        print("String  :", tag)
        print("Matched:", match)
    brat = BratDocument(text, annotations)
    return brat


def muc_evaluation(test_files, predict_files):
    count = 0
    files = list(zip(test_files, predict_files))
    for test_file, predict_file in files[3:]:
        test_muc = open(test_file).read()
        test_brat = muc_to_brat(test_muc)
        predict_muc = open(predict_file).read()
        predict_brat = muc_to_brat(predict_muc)
        count += 1
        assert test_brat.text == predict_brat.text
    0


if __name__ == '__main__':
    test_files = []
    predict_files = []
    predict_folder = "../tmp/NER/anhv"
    test_folder = "../tmp/NER/NER-Test-Domains"
    for subfolder in listdir(test_folder):
        files = listdir(join(test_folder, subfolder))
        for file in files:
            test_files.append(join(test_folder, subfolder, file))
            predict_files.append(join(predict_folder, file))
    muc_evaluation(test_files, predict_files)
