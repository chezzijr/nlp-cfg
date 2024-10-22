from __future__ import annotations
import pickle
import yaml
import random
from dataclasses import dataclass

DICTIONARY_PATH = "./data/data.yaml"
DICTIONARY_PICKLE_PATH = "./data/dict_obj.pkl"

@dataclass
class WordDefinition:
    definition: str
    examples: list[str]
    tag: str

@dataclass
class Word:
    word: str
    definitions: list[WordDefinition]

class Dictionary:
    def __init__(self):
        self.d = load_dictionary_from_pickle()
        # số chữ nhiều nhất trong một từ
        self.max_word_length = max(len(w.split()) for w in self.d.keys())

    def exists(self, word: str):
        return word in self.d

    def word(self, word: str) -> Word:
        w = self.d[word]
        defs = []
        for ds in w:
            for d in ds["defs"]:
                defs.append(WordDefinition(d["def"], d["examples"], ds["tag"]))
        return Word(word, defs)

    def words(self) -> list[str]:
        return self.d.keys()

    def words_of_tag(self, tag: str):
        return [w for w in self.words() if self.word(w).definitions[0].tag == tag]

    def random_of_tag(self, tag: str):
        return self.word(random.choice(self.words_of_tag(tag)))

    # from nonterminal to list of words
    def rules(self):
        d = {}
        for w in self.words():
            for defn in self.word(w).definitions:
                if defn.tag not in d:
                    d[defn.tag] = []
                d[defn.tag].append(w)
        return d

    def tokenize(self, text: str) -> list[list[str]]:
        set_of_words = set(w for w in self.words() if w in text)
        def recursion(curr: list[str], rem: list[str], ans: list[list[str]]):
            if not rem:
                ans.append(curr)
                return
            for i in range(1, len(rem) + 1):
                if i > self.max_word_length:
                    break
                word = " ".join(rem[:i])
                if word in set_of_words:
                    recursion(curr + [word], rem[i:], ans)

        ans = []
        recursion([], text.split(), ans)
        return ans


def load_dictionary_from_pickle():
    with open(DICTIONARY_PICKLE_PATH, "rb") as f:
        d = pickle.load(f)
    return d

def save_dictionary_as_pickle(d):
    with open(DICTIONARY_PICKLE_PATH, "ab") as f:
        pickle.dump(d, f)


if __name__ == "__main__":
    with open(DICTIONARY_PATH, "r") as f:
        d = yaml.safe_load(f)
    save_dictionary_as_pickle(d)
