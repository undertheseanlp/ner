from os.path import dirname, join
from underthesea_flow.flow import Flow
from underthesea_flow.model import Model
from underthesea_flow.model.crf import CRF
from underthesea_flow.reader.tagged_corpus import TaggedCorpus
from underthesea_flow.transformer.tagged import TaggedTransformer
from underthesea_flow.validation.validation import TrainTestSplitValidation

from preprocess import vlsp2016

if __name__ == '__main__':
    # =========================================================================#
    # Start an experiment with flow
    # =========================================================================#
    flow = Flow()

    # =========================================================================#
    #                               Data
    # =========================================================================#

    # for evaluation
    file = join(dirname(__file__), "corpus", "vlsp2016", "train.txt")
    # file = join(dirname(__file__), "corpus", "sample_vlsp_2016", "train.txt")
    sentences = vlsp2016.load_data(file)

    # for saving model
    # corpus_folder = join(dirname(__file__), "corpus", "vlsp_chunk")
    # train = join(corpus_folder, "train.txt")
    # dev = join(corpus_folder, "dev.txt")
    # test = join(corpus_folder, "test.txt")
    # sentences = load_data(train) + load_data(dev) + load_data(test)

    flow.data(sentences=sentences)

    # =========================================================================#
    #                                Transformer
    # =========================================================================#
    template = [
        "T[0].lower", "T[-1].lower", "T[1].lower",
        "T[0].istitle", "T[-1].istitle", "T[1].istitle",
        "T[-2]", "T[-1]", "T[0]", "T[1]", "T[2]",  # word unigram
        "T[-2,-1]", "T[-1,0]", "T[0,1]", "T[1,2]",  # word bigram
        "T[-2][1]", "T[-1][1]", "T[0][1]", "T[1][1]", "T[2][1]",  # pos unigram,
        "T[-2,-1][1]", "T[-1,0][1]", "T[0,1][1]", "T[1,2][1]", # pos bigram
    ]
    transformer = TaggedTransformer(template)

    flow.transform(transformer)

    # =========================================================================#
    #                               Models
    # =========================================================================#
    crf_params = {
        'c1': 1.0,  # coefficient for L1 penalty
        'c2': 1e-3,  # coefficient for L2 penalty
        'max_iterations': 1000,  #
        # include transitions that are possible, but not observed
        'feature.possible_transitions': True
    }
    flow.add_model(Model(CRF(params=crf_params), "CRF"))

    # =========================================================================#
    #                              Evaluation
    # =========================================================================#
    flow.add_score('f1_chunk')
    flow.add_score('accuracy_chunk')

    flow.set_validation(TrainTestSplitValidation(test_size=0.1))

    flow.train()

    # flow.save_model("CRF", filename="crf")
