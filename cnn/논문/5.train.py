import torch
import torch.nn as nn
import torch.optim as optim
from model import CNNTextClassifier 
import time, os
import numpy as np

# Device configuration
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class Trainer(object):
    def __init__(self, config, train_set, train_loader, eval_set, eval_loader, test_set,
            test_loader):
        self.config = config
        self.train_set= train_set 
        self.train_loader = train_loader 
        self.test_set = test_set 
        self.test_loader = test_loader 
        self.eval_set = eval_set 
        self.eval_loader = eval_loader

        self.mode = config.mode

        self.idx2group = { 0 : 'ELEC', 1 : 'FALL', 2 : 'COLA', 3 : 'CRAS', 4 : 'SPLA'}

        self.lr = config.lr
        self.num_epochs = config.num_epochs

        self.log_interval = config.log_interval 
        self.eval_interval = config.eval_interval 
        self.save_dir = config.save_dir

        if len(self.config.kernel_sizes) == 1: 
            self.channels = "single"
        else:
            self.channels = "multi"

        self.build_net() 
    
    def build_net(self):
        model = CNNTextClassifier(len(self.train_set.word2idx)+1, 5) # class의 개수 
        
        if self.config.training_model is not None:
            model.load_state_dict(torch.load(self.config.training_model))

        if self.mode == 'test': 
            model.load_state_dict(torch.load(os.path.join(self.save_dir, 'best_acc.pth'),
            lambda storage, loc: storage))

        self.model = model.to(device) 
        print("[*] Prepare model completed!")

    def train(self):
        criterion = nn.CrossEntropyLoss()
        parameters = filter(lambda p: p.requires_grad, self.model.parameters()) 
        optimizer = optim.Adam(parameters, lr=self.lr)
        
        steps = 0
        best_acc = 0.

        print("\nLearning started!") 
        start_time = time.time()
        for epoch in range(self.num_epochs):
            for step, (feature, target) in enumerate(self.train_loader): 
                self.model.train()
                step_batch = feature.size(0)
                feature = feature.to(device).long()
                target = target.to(device).long()
                
                logits = self.model(feature)
                loss = criterion(logits, target)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                steps += 1

                if steps % self.log_interval == 0:
                    predicted = torch.max(logits, 1)[1].view(target.size()) 
                    corrects = (predicted.data == target.data).sum() 
                    accuracy = 100.0 * (float(corrects) / step_batch)

                    end_time = time.time()
                    print("[%d/%d] [%d/%d] time:%.3f loss:%.3f accuracy:%.3f" % (epoch + 1, self.num_epochs, step + 1, len(self.train_loader), end_time - start_time, loss.item(), accuracy))

                if steps % self.eval_interval == 0: 
                    acc = self.eval()
                    if acc > best_acc:
                        best_acc = acc
                        torch.save(self.model.state_dict(), os.path.join(self.save_dir, 'best_acc.pth')) # save model
                        print("Save model completed!")
         
            print("Learning finished!")
            torch.save(self.model.state_dict(), os.path.join(self.save_dir, 'final.pht')) # save model
            print("Save model completed!")

    def eval(self):
        self.model.eval()

        avg_acc = 0.
        avg_loss = 0.

        criterion = nn.CrossEntropyLoss()

        for feature, target in self.eval_loader: 
            step_batch = feature.size(0)

        feature = feature.to(device).long()
        target = target.to(device).long()

        logits = self.model(feature) 
        loss = criterion(logits, target)

        predicted = torch.max(logits, 1)[1].view(target.size()) 
        corrects = (predicted.data == target.data).sum() 
        accuracy = 100.0 * (float(corrects) / step_batch)

        avg_loss += loss.item() / len(self.train_loader) 
        avg_acc += accuracy / len(self.train_loader)

        print("Evaluation- loss: %.3f accuracy: %.3f"% (avg_loss, avg_acc)) 
        return avg_acc

    def test(self):
        self.model.eval()
        for idx, feature in enumerate(self.test_loader):
            feature = feature.to(device).long()

            logits = self.model(feature)
            predicted = torch.max(logits, 1)[1] 
            predicted = self.idx2group[predicted.item()]

            print("Document ID: {}\tPredicted class: {}".format(idx+1, predicted))
