from torch.utils import data
from torch.utils.data import DataLoader


class Indexer:
    def __init__(self):
        self.w2i = {}

    def fit_transfrom(self, tokens):
        indices = []
        for token in tokens:
            if token in self.w2i:
                index = self.w2i[token]
            else:
                index = len(self.w2i)
                self.w2i[token] = index
            indices.append(index)
        return indices


class VLSP2016Dataset(data.Dataset):
    def __init__(self, train_data_path, w2i=None):
        f = open(train_data_path, 'r')
        lines = f.read().split("\n\n")
        lines = lines[:10]
        token_indexer = Indexer()
        label_indexer = Indexer()
        self.data = []
        for sentence in lines:
            items = sentence.split("\n")
            tokens = [item.split("\t")[0] for item in items]
            tokens = token_indexer.fit_transfrom(tokens)
            labels = [item.split("\t")[-1] for item in items]
            labels = label_indexer.fit_transfrom(labels)
            self.data.append((tokens, labels))

    def __getitem__(self, index):
        tokens, labels = self.data[index]
        return tokens, labels

    def __len__(self):
        return len(self.data)


if __name__ == '__main__':
    vlsp2016_dataset = VLSP2016Dataset("data/train.txt")
    print(0)
    dataloader = DataLoader(vlsp2016_dataset, batch_size=4, shuffle=True, num_workers=4)
    for i, data in enumerate(dataloader):
        tokens, labels = data
        print(i)
        print(tokens)
        print(labels)
