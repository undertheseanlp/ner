import json
from os.path import join
from pprint import pprint

from sklearn.metrics import confusion_matrix
from underthesea.util.file_io import read

def convert_cm_to_log(cm, labels, line=5):
    cm = cm.tolist()
    # cm = [" ".join([("%-" + str(line) + "s") % labels[index]] + map(lambda i: ("%" + str(line) + "d") % i, row)) for index, row in enumerate(cm)]
    cm_ = []
    for index, row in enumerate(cm):
        content = " ".join([("%-" + str(line) + "s") % labels[index]] + map(lambda i: ("%" + str(line) + "d") % i, row))
        cm_.append(content)
    title = " " * (line + 1) + " ".join(map(lambda i: ("%" + str(line) + "s") % i, labels))
    cm.insert(0, title)
    return cm
# results = json.loads(read(join("logs", "20171006_153955", "result.json")))
results = json.loads(read(join("logs", "20171006_161437", "result.json")))
print(0)
actual = results["actual"]
expected = results["expected"]
labels = list(set(expected).union(set(actual)))
cm = confusion_matrix(expected, actual, labels)
cm = convert_cm_to_log(cm, labels)
pprint(cm, indent=2)