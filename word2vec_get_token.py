import torch
from torch import nn
from d2l import torch as d2l
import pandas as pd
import matplotlib.pyplot as plt
import random
import math


def subsample(sentences, vocab):
    """Subsample high-frequency words.

    Defined in :numref:`sec_word2vec_data`"""
    # Exclude unknown tokens '<unk>'
    sentences = [[token for token in line if vocab[token] != vocab.unk]
                 for line in sentences]
    counter = d2l.count_corpus(sentences)
    num_tokens = sum(counter.values())

    # Return True if `token` is kept during subsampling
    def keep(token):
        return(random.uniform(0, 1) <
               math.sqrt(1e-3 / counter[token] * num_tokens))

    return ([[token for token in line if keep(token)] for line in sentences],
            counter)


def load_answer(sentences: list, max_window_size=2, num_noise_words=2):
    vocab = d2l.Vocab(sentences, min_freq=2)  # 获得vocab
    subsampled, counter = subsample(sentences, vocab)  # 下采样删除某些高频词
    # d2l.show_list_len_pair_hist(['origin', 'subsampled'], '# tokens per sentence', 'count', sentences, subsampled)
    # plt.show()
    subsampled = list(filter(None, subsampled))
    corpus = [vocab[line] for line in subsampled]  # 获取corpus
    # 获取中心词和上下文
    all_centers, all_contexts = d2l.get_centers_and_contexts(corpus, max_window_size=max_window_size)
    print("all_centers number", len(all_centers))
    print("all_contexts", len(all_contexts))
    # 负采样
    all_negatives = d2l.get_negatives(all_contexts, vocab, counter, num_noise_words)
    print(len(all_negatives))


liushui = pd.read_excel('liushui.xlsx', nrows=10000)
sentences = liushui['seg']
sentences = [sentence.split(',') for sentence in sentences]
load_answer(sentences)