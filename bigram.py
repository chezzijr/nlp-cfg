from __future__ import annotations
from math import log, exp
from dictionary import Dictionary
from collections import defaultdict
from os.path import exists
import random as rd
import pickle

def zero():
    return 0.0

def empty_dict():
    return defaultdict(zero)

class BigramModel:
    def __init__(self, d: Dictionary, path: str):
        self.d = d
        self.word_prob: defaultdict[str, float] = empty_dict()
        self.word_conditional_prob: defaultdict[str, defaultdict[str, float]] = defaultdict(empty_dict)
        self.gather_word_prob()

        with open(path, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, d: Dictionary, path: str = "models/bigram.pkl") -> BigramModel:
        if exists(path):
            with open(path, "rb") as f:
                return pickle.load(f)
        return cls(d, path)

    def get_examples(self, example: str) -> list[str]:
        list_examples = example.split("~")
        list_examples = list(map(lambda x: x if '\"' not in x else x.split('\"')[1], list_examples))
        return list_examples

    def gather_word_prob(self):
        def word_cnt_str(word: str):
            word_cnt = 0
            tokens_posibilities = self.d.tokenize(word)
            for posibility in tokens_posibilities:
                for i, token in enumerate(posibility):
                    word_cnt += 1
                    self.word_prob[token] += 1
                    if i > 0:
                        self.word_conditional_prob[posibility[i - 1]][token] += 1
            return word_cnt

        word_cnt = 0
        for word in self.d.words():
            w = self.d.word(word)
            for definition in w.definitions:
                defi = definition.definition
                word_cnt += word_cnt_str(defi)

                for examples in definition.examples:
                    if examples == "":
                        continue

                    for example in self.get_examples(examples):
                        word_cnt += word_cnt_str(example)
                
        for token in self.word_prob:
            self.word_prob[token] = log(self.word_prob[token] / word_cnt)

        for token in self.word_conditional_prob:
            total = sum(self.word_conditional_prob[token].values())
            for next_token in self.word_conditional_prob[token]:
                self.word_conditional_prob[token][next_token] = log(self.word_conditional_prob[token][next_token] / total)

    def generate_word(self, tag: str, prev_word: str | None = None):
        selected_dict_prob = self.word_prob if prev_word is None else self.word_conditional_prob[prev_word]
        list_of_words = sorted(selected_dict_prob.items(), key=lambda x: x[1], reverse=True)
        list_of_words = list(filter(lambda x: tag in [d.tag for d in self.d.word(x[0]).definitions], list_of_words))
        if not list_of_words:
            return self.d.random_of_tag(tag).word
        
        softmax_prob = [exp(x[1]) for x in list_of_words]
        total_prob = sum(softmax_prob)
        softmax_prob = [x / total_prob for x in softmax_prob]
        return rd.choices(list_of_words, weights=softmax_prob)[0][0]
