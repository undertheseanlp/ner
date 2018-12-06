from torch.utils import data
from torch.utils.data import DataLoader


class VLSP2016Dataset(data.Dataset):
    def __init__(self, train_data_path):
        f = open(train_data_path, 'r')
        lines = f.read().split("\n\n")
        self.lines = lines

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

