from models import CRFTrainer

features = []
corpus = []

trainer = CRFTrainer(features, corpus)

trainer.train('resources/taggers.bin')
