import torch
import torch.nn as nn
import torch.nn.functional as F

from config import get_config

# Device configuration
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class CNNTextClassifier(nn.Module):
    def __init__(self, vocab_size, num_classes):
        super(CNNTextClassifier, self).__init__()
        config = get_config()
        config.kernel_sizes = [int(k) for k in config.kernel_sizes.split(',')] 
        self.config = config

        embedding_dim = vocab_size 
        channel_in = 1
        channel_out = config.channel_out 
        kernel_sizes = config.kernel_sizes

        self.embedding = nn.Embedding(vocab_size, embedding_dim) 
        self.conv1 = nn.ModuleList([nn.Conv2d(channel_in, channel_out,
                                        (k, embedding_dim)) 
                                for k in kernel_sizes])

        self.dropout = nn.Dropout(config.dropout)
        self.fc1 = nn.Linear(len(kernel_sizes) * channel_out, num_classes)

    def forward(self, x):
        h = self.embedding(x)
        h = h.unsqueeze(1) # (batch, 1, vocab_size, embedding_dim)
        h = [F.relu(conv(h)).squeeze(3) for conv in self.conv1] # [(batch, channel_out, vocab_size)] * len(kernel_sizes)
        h = [F.max_pool1d(i, i.size(2)).squeeze(2) for i in h] # [(batch, channel_out)] * len(kernel_sizes)
        h = torch.cat(h, 1) # (batch, channel_out * len(kernel_sizes) h = self.dropout(h)
        logit = self.fc1(h) # (batch, num_classes)
        return logit