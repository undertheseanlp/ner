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
        for sentence in lines:
            items = sentence.split("\n")
            tokens = [item.split("\t")[0] for item in items]
            tokens = token_indexer.fit_transfrom(tokens)
            label = [item.split("\t")[-1] for item in items]
            print(0)
        if w2i is None:
            self.w2i = {}

    def __getitem__(self, index):
        sentence = self.lines[index]
        items = sentence.split("\n")
        tokens = []
        labels = []
        for item in items:
            tokens.append(item.split("\t")[0])
            labels.append(item.split("\t")[-1])
        return tokens, labels

    def __len__(self):
        return len(self.lines)


if __name__ == '__main__':
    vlsp2016_dataset = VLSP2016Dataset("data/train.txt")
    print(0)
    dataloader = DataLoader(vlsp2016_dataset, batch_size=4, shuffle=True, num_workers=4)
    for i, data in enumerate(dataloader):
        tokens, labels = data
        print(i)
        print(tokens)
        print(labels)
