import pickle
import torch
from torch import nn
from d2l import torch as d2l
import numpy as np
from torch.optim import Adam
from torch.nn import CrossEntropyLoss
from get_vocab import Vocab
from process_data import Patient


class Bertblock(nn.Module):
    def __init__(self, hidden_size, num_heads, dropout):
        super().__init__()
        self.attention = nn.MultiheadAttention(embed_dim=hidden_size, num_heads=num_heads, dropout=dropout, kdim=hidden_size, vdim=hidden_size)
        self.addnorm1 = d2l.AddNorm(hidden_size, dropout)
        self.feed = nn.Linear(hidden_size, hidden_size)
        self.addnorm2 = d2l.AddNorm(hidden_size, dropout)

    def forward(self, X):
        # X.shape: batch_size, num_steps, num_features
        X = X.permute(1, 0, 2)
        attention_output, attention_weight = self.attention(X, X, X)
        attention_output = attention_output.permute(1, 0, 2)
        Y1 = self.addnorm1(X.permute(1, 0, 2), attention_output)
        Y2 = self.feed(Y1)
        Y3 = self.addnorm2(Y1, Y2)
        return Y3


class Bert(nn.Module):
    def __init__(self, hidden_size, num_heads, dropout, num_layers, out_features):
        super().__init__()
        self.blocks = nn.Sequential()
        for i in range(num_layers):
            self.blocks.add_module("bertblock"+str(i), Bertblock(hidden_size, num_heads, dropout))
        self.linear = nn.Linear(hidden_size, out_features)


    def forward(self, X):
        vec = self.blocks(X)[:, 0, :]
        output = self.linear(vec)
        return vec, output


class Trainer:
    def __init__(self, net, loss, optimizer, lr, device, vocab, max_len=10):
        super().__init__()
        self.loss = loss
        self.lr = lr
        self.device = device
        self.net = net.to(device)
        self.optimizer = optimizer(self.net.parameters(), self.lr)
        self.max_len = max_len
        self.vocab = vocab

    def fit(self, train_iter, test_iter, max_epochs):
        patient_vecs = []
        animator = d2l.Animator(xlabel="epoch", ylabel="loss", legend=['train_loss', "test_loss", "test_acc"])
        for epoch in range(max_epochs):
            iter = 1
            metric = d2l.Accumulator(6)
            for patient_IDs, X, Y in train_iter:
                num = len(train_iter)
                X = list(X)
                X = torch.tensor([self.tokenizer(x) for x in X])
                X, Y = X.to(self.device), Y.to(self.device)
                vec, output = self.net(X)
                loss = self.loss(output, Y).mean()
                self.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(self.net.parameters(), 1)
                self.optimizer.step()
                vec = vec.cpu()
                vec = vec.detach().numpy()
                if epoch+1 == max_epochs:
                    patient_vecs.append((patient_IDs, vec))
                metric.add(1, loss.item(), 0, 0, 0, 0)
                print('| epoch %d | iter %d/%d | train loss %.4f |' % (epoch+1, iter, num, metric[1]/metric[0]))
                iter += 1

            for patient_IDs_test, X_test, Y_test in test_iter:
                with torch.no_grad():
                    patient_IDs_test = np.array(patient_IDs_test)
                    X_test = list(X_test)
                    X_test = torch.tensor([self.tokenizer(x) for x in X_test])
                    X_test, Y_test = X_test.to(self.device), Y_test.to(self.device)
                    vec, output = self.net(X_test)
                    vec = vec.cpu()
                    vec = vec.detach().numpy()
                    if epoch + 1 == max_epochs:
                        patient_vecs.append((patient_IDs_test, vec))
                    loss = self.loss(output, Y_test).mean()
                    acc = d2l.accuracy(output, Y_test)
                    metric.add(0, 0, 1, loss.item(), len(X_test), acc)
            print('| epoch %d | test loss %.4f | acc %.4f |' % (epoch+1, metric[3]/metric[2], metric[5]/metric[4]))
            animator.add(epoch+1, [metric[1]/metric[0], metric[3]/metric[2], metric[5]/metric[4]])
        torch.save(self.net.state_dict(), "./data/param.pkl")
        return patient_vecs

    def tokenizer(self, x):
        x = ['[cls]'] + x.split(",")
        n = len(x)
        if n < self.max_len:
            x = x + ['[pad]'] * (self.max_len - n)
        else:
            x = x[:self.max_len]
        return [self.vocab.get_vector(token) for token in x]


if __name__ == "__main__":
    bert = Bert(128, 16, 0, 3, 188)
    with open("./data/train_iter.pkl", "rb") as f:
        train_iter = pickle.load(f)
    with open("./data/test_iter.pkl", "rb") as f:
        test_iter = pickle.load(f)
    with open('./data/vocab.pkl', "rb") as f:
        vocab = pickle.load(f)
    loss = CrossEntropyLoss()
    optimizer = Adam
    trainer = Trainer(bert, loss, optimizer, lr=0.1, device=d2l.try_gpu(), vocab=vocab, max_len=10)
    patient_vecs = trainer.fit(train_iter, test_iter, 3)
    with open("patient_vecs.pkl", "wb") as f:
        pickle.dump(patient_vecs, f)

