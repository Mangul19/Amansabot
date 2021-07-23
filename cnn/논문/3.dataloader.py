from torch.utils.data import DataLoader, Dataset
from konlpy.tag import Hannanum
tagger = Hannanum()

import numpy as np
import pandas as pd
from sklearn.utils import shuffle

class GlobalDataset(Dataset):
    def __init__(self, train_root, test_root, MAX_LENGTH, split_ratio):
        entire_set = pd.read_csv(train_root, header=None, encoding='UTF8') 
        entire_set = entire_set.drop(columns=0).dropna()
        entire_set = shuffle(entire_set)

        # train-eval split
        split_row = int(len(entire_set) * (1.-split_ratio)) 
        self.train_set = entire_set.values[:split_row, :] 
        self.eval_set = entire_set.values[split_row:, :]

        test_set = pd.read_csv(test_root, header=None, encoding='UTF8').drop(columns=[0]).dropna()
        self.test_set = test_set.values

        self.group2idx = {'ELEC': 0, 'FALL': 1, 'COLA': 2, 'CRAS': 3, 'SPLA' : 4} 
        self.MAX_LENGTH = MAX_LENGTH
        
        self.train_x = []
        self.train_y = []
        self.eval_x = []
        self.eval_y = []
        self.test_x = []

        self.build_word2idx()

    def build_word2idx(self):
    # global word-to-index vocabulary for training, evaluating, testing self.word2idx = {}
    
    # for training set, build word vocabulary for item in self.train_set:
        sentence = item[0]
        group = item[1]

        # remove useless space
        sentence = sentence.lstrip().rstrip() 
        if len(sentence) > 5:
            tokenized = tagger.nouns(sentence) 
            for token in tokenized:
                if token not in self.word2idx: 
                    self.word2idx[token] = len(self.word2idx)
            tokenized = [self.word2idx[w] for w in tokenized]
            padding = [0 for i in range(self.MAX_LENGTH - len(tokenized))] tokenized.extend(padding)
            self.train_x.append(tokenized) 
            self.train_y.append(self.group2idx[group])

        # for evaluating set, add word vocabulary for item in self.eval_set:
        sentence = item[0]
        group = item[1]

        # remove useless space
        sentence = sentence.lstrip().rstrip() 
        if len(sentence) > 5:
            tokenized = tagger.nouns(sentence) 
            for token in tokenized:
                if token not in self.word2idx: 
                    self.word2idx[token] = len(self.word2idx)
            tokenized = [self.word2idx[w] for w in tokenized]
            padding = [0 for i in range(self.MAX_LENGTH - len(tokenized))] tokenized.extend(padding)
            self.eval_x.append(tokenized) 
            self.eval_y.append(self.group2idx[group])

        # for testing set, add word vocabulary 
        for item in self.test_set:
            sentence = item[0]

            # remove useless space
            sentence = sentence.lstrip().rstrip() 
            if len(sentence) > 5:
                tokenized = tagger.nouns(sentence) 
                for token in tokenized:
                    if token not in self.word2idx: 
                        self.word2idx[token] = len(self.word2idx)

                tokenized = [self.word2idx[w] for w in tokenized]
                padding = [0 for i in range(self.MAX_LENGTH - len(tokenized))] 
                tokenized.extend(padding)
                self.test_x.append(tokenized)

        self.train_x = np.asarray(self.train_x) 
        self.train_y = np.asarray(self.train_y) 
        self.eval_x = np.asarray(self.eval_x) 
        self.eval_y = np.asarray(self.eval_y) 
        self.test_x = np.asarray(self.test_x)
    
    def __len__(self):
       return len(self.train_x)

    def __getitem__(self, idx):
        return self.train_x[idx], self.train_y[idx]

class EvalDataset(Dataset):
    def __init__(self, global_dataset):
        self.global_dataset = global_dataset 
        self.eval_x = self.global_dataset.eval_x 
        self.eval_y = self.global_dataset.eval_y

    def __len__(self):
        return len(self.eval_x)

    def __getitem__(self, idx):
        return self.eval_x[idx], self.eval_y[idx]

class TestDataset(Dataset):
    def __init__(self, global_dataset):
        self.global_dataset = global_dataset 
        self.test_x = self.global_dataset.test_x

    def __len__(self):
       return len(self.test_x)

    def __getitem__(self, idx): 
        return self.test_x[idx]

def get_loader(train_root, test_root, split_ratio, batch_size):
    train_set = GlobalDataset(train_root, test_root, 500, split_ratio) 
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True) 
    eval_set = EvalDataset(train_set)
    eval_loader = DataLoader(eval_set, batch_size=batch_size, shuffle=False) 
    test_set = TestDataset(train_set)
    test_loader = DataLoader(test_set, batch_size=1, shuffle=False)
    return train_set, train_loader, eval_set, eval_loader, test_set, test_loader