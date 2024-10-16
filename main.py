from dictionary import Dictionary 
from grammar import Grammar
from rule import Rule
import nltk


if __name__ == "__main__":
    d = Dictionary()
    r = Rule.default()
    g = Grammar(d, r)
    tokens = g.generate_sentence()
    sentence = " ".join(tokens)
    print("Random Sentence:", sentence)
    cfg = nltk.CFG.fromstring(str(g))
    parser = nltk.ChartParser(cfg)
    for t in parser.parse(tokens):
        print(t)
