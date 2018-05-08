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
    position = 0
    markers = []
    index = re.search("<ENAMEX", muc_document)
    for match in re.finditer("<ENAMEX TYPE=\".*?\">|</ENAMEX>", muc_document):
        start_tag, end_tag = match.regs[0]
        tag = muc_document[start_tag:end_tag]
        # START TAG
        if tag.startswith("<ENAMEX"):
            tag_matched = re.match("<ENAMEX TYPE=\"(?P<tag>.*?)\">", tag)
            tag_name = tag_matched.group("tag")
            markers.append((tag_name, start_tag))
        # END TAG
        else:
            tag_name, start_position = markers.pop()
            end_position = start_position + len(tag_name)
            print(0)

        text += muc_document[position:start_tag]
        position = end_tag
        print("String  :", tag)
        print("Matched:", match)
    brat = BratDocument(text, annotations)
    return brat


def muc_evaluation(test_files, predict_files):
    # for test_file, predict_file in zip(test_files, predict_files):
    #     test_muc = open(test_file).read()
    #     brat_document = muc_to_brat(test_muc)
    test_file, predict_file = list(zip(test_files, predict_files))[0]
    test_muc = open(test_file).read()
    test_brat = muc_to_brat(test_muc)
    predict_muc = open(predict_file).read()
    predict_brat = muc_to_brat(predict_muc)


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
