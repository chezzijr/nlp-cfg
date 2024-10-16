from dictionary import Dictionary
import random
from rule import Rule
from bigram import BigramModel

def flatten(container: list | tuple):
    for i in container:
        if isinstance(i, (list, tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i 


class Grammar:
    def __init__(self, lexicals: Dictionary, rules: Rule):
        self.rules = rules
        self.lexicals = lexicals

    def nonterminals(self):
        return set(self.rules.keys())

    def to_dict(self):
        grammar = self.rules.copy()
        for word in self.lexicals.words():
            w = self.lexicals.word(word)
            for d in w.definitions:
                if d.tag not in grammar:
                    grammar[d.tag] = []
                grammar[d.tag].append(word)
        return grammar

    def __str__(self):
        s = ""
        g = self.to_dict()
        for k, v in g.items():
            s += f"{k} -> "
            v = map(lambda x: " ".join(x) if isinstance(x, list) else f"\'{x}\'", v)
            s += " | ".join(v)
            s += "\n"
        return s


    def leaves(self):
        # exclude nonterminals like "NP", "VP", "PP"
        return set(flatten(list(self.rules.values()))) - self.nonterminals()

    def generate(self, symbols: list[str], depth: int):
        for _ in range(depth):
            symbols = list(flatten([random.choice(self.rules.get(symbol, [symbol])) for symbol in symbols]))

        # clean up NP, VP, PP
        symbols = list(flatten([self.rules.recursively_search_for_leaves(symbol) for symbol in symbols]))

        return symbols

    def generate_sentence(self, depth: int = 3):
        """
        depth: int, the depth of the tree, used to prevent infinite recursion
        if there are nonleave nodes, proceed to clean up
        """
        bigram = BigramModel.load(self.lexicals)
        structure = self.generate(["S"], depth)
        print(structure)
        sentence = []
        for i, tag in enumerate(structure):
            print(tag, sentence[-1] if i > 0 else None)
            word = bigram.generate_word(tag, sentence[-1] if i > 0 else None)
            sentence.append(word)

        return sentence
