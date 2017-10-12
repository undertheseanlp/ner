# -*- coding: utf-8 -*-
from difflib import ndiff, unified_diff, context_diff
from os import listdir, mkdir
import shutil
from os.path import dirname, join, isfile
from underthesea.util.file_io import read, write

from models.ner_1 import ner


def load_input(input_file):
    lines = read(input_file).strip().split("\n")
    if lines[0][0] == "#":
        lines = lines[1:]
    content = [line.split("\t")[0] for line in lines]
    content = u" ".join(content)
    return content

def load_output(input_file):
    lines = read(input_file).strip().split("\n")
    if lines[0][0] == "#":
        lines = lines[1:]
    text = "\n".join(lines)
    return text

def extract_sentence(content):
    return "# " + " ".join([token.split("\t")[0] for token in content.split("\n")])

if __name__ == '__main__':
    test_dir = join(dirname(__file__), "test_set")
    files = [f for f in listdir(test_dir) if isfile(join(test_dir, f))]
    model_id = "1"
    try:
        shutil.rmtree(join(test_dir, model_id))
    except:
        pass
    mkdir(join(test_dir, model_id))
    for f in files:
        input = load_input(join(test_dir, f))
        output = ner(input)
        actual = "\n".join(["\t".join(tokens) for tokens in output])
        expected = load_output(join(test_dir, f))
        if actual != expected:
            print("\n{}".format(f))
            diff = '\n'.join(ndiff(expected.splitlines(), actual.splitlines()))
            write(join(test_dir, model_id, f), "\n".join([extract_sentence(actual), actual]))
            write(join(test_dir, model_id, f + ".diff"), "\n".join([extract_sentence(actual), diff]))
