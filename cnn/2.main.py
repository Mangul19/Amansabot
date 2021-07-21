#-*- coding: utf-8 -*-

from __future__ import print_function 
import random
import torch
import torch.backends.cudnn as cudnn
import os, sys 
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import get_config 
from train import Trainer
from dataloader import get_loader

# Device configuration
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def main(config):
    if config.save_dir is None:
        config.save_dir = 'samples' 
    os.system('mkdir {0}'.format(config.save_dir))

    config.manual_seed = random.randint(1, 10000) 
    print("Random Seed: ", config.manual_seed)

    random.seed(config.manual_seed) 
    torch.manual_seed(config.manual_seed) 
    torch.cuda.manual_seed_all(config.manual_seed)

    cudnn.benchmark = True

    print("[*] Preparing dataloader...")
    train_set, train_loader, eval_set, eval_loader, test_set, test_loader = get_loader(train_root=config.train_root,
        test_root=config.test_root,
        split_ratio=config.split_ratio,
        batch_size=config.batch_size)
        
print("Length of training set:", len(train_set)) 
print("Length of evaluating set:", len(eval_set)) 
print("Length of testing set:", len(test_set)) 
print("[*] Preparing dataloader completed!")

trainer = Trainer(config, train_set, train_loader, eval_set, eval_loader, test_set, test_loader)
if config.mode == 'train':
    trainer.train()
else:
    trainer.test()
       
if __name__ == "__main__": 
    config = get_config() 
    main(config)