from flair.data import TaggedCorpus
from flair.data_fetcher import NLPTaskDataFetcher, NLPTask
from flair.embeddings import TokenEmbeddings, WordEmbeddings, StackedEmbeddings, MemoryEmbeddings, CharacterEmbeddings
from typing import List
import torch
import matplotlib.pyplot as plt

# 1. get the corpus
columns = {0: 'text', 1: 'ner'}
corpus: TaggedCorpus = NLPTaskDataFetcher.fetch_column_corpus("data1", columns,
                                                              train_file="train.txt",
                                                              test_file="test.txt",
                                                              dev_file="dev.txt")
print(corpus)

# 2. what tag do we want to predict?
tag_type = 'ner'

# 3. make the tag dictionary from the corpus
tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
print(tag_dictionary.idx2item)

# 4. initialize embeddings
embedding_types: List[TokenEmbeddings] = [
    CharacterEmbeddings(),
    WordEmbeddings("tmp/text19G.size300.bin")

]

embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

# 5. initialize sequence tagger
from flair.models import SequenceTagger

tagger: SequenceTagger = SequenceTagger(hidden_size=1024,
                                        embeddings=embeddings,
                                        tag_dictionary=tag_dictionary,
                                        tag_type=tag_type,
                                        use_crf=True)

# 6. initialize trainer
from flair.trainers import SequenceTaggerTrainer

trainer: SequenceTaggerTrainer = SequenceTaggerTrainer(tagger, corpus)

# 7. start training
model_path = "tmp/model2"
trainer.train(model_path,
              learning_rate=0.1,
              mini_batch_size=8,
              max_epochs=150)

# 8. plot training curves (optional)
from flair.visual.training_curves import Plotter

plotter = Plotter()
plotter.plot_training_curves(f'{model_path}/loss.tsv')
plotter.plot_weights(f'{model_path}/weights.txt')