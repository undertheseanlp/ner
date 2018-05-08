from underthesea import chunk
import sys
if sys.version_info >= (3, 0):
    from .model_crf import CRFNERPredictor
else:
    from model_crf import CRFNERPredictor


def ner(sentence):
    sentence = chunk(sentence)
    crf_model = CRFNERPredictor.Instance()
    result = crf_model.predict(sentence, format)
    return result

