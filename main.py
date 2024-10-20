from dictionary import Dictionary 
from grammar import Grammar
from rule import Rule
import time
import random
from nltk.parse import TopDownChartParser
from nltk import CFG

d = Dictionary()
r = Rule.default()
g = Grammar(d, r)

def generate_random_sentence():
    tokens = g.generate_sentence()
    print(" ".join(tokens))

def generate_10k_sentences():
    num_sentences = 10_000
    start = time.perf_counter()
    with open("output/samples.txt", "w") as f:
        for i in range(num_sentences):
            print(f"Generating sentence {i+1}/{num_sentences}", end="\r")
            tokens = g.generate_sentence()
            sentence = " ".join(tokens)
            f.write(sentence + "\n")
    print(f"Generated {num_sentences} sentences in {time.perf_counter() - start:.2f} seconds")

def parse_input_file():
    input_file = "input/sentences.txt"
    output_file = "output/parsed-results.txt"
    grammar = CFG.fromstring(str(g))
    parser = TopDownChartParser(grammar)
    with open(input_file, "r") as f:
        sentences = f.readlines()
    with open(output_file, "w") as f:
        for line in sentences:
            tokens_posibitities = d.tokenize(line.strip())
            ans = None
            for tokens in tokens_posibitities:
                # for tree in parser.parse(tokens):
                #     f.write(str(tree) + "\n")
                trees = list(parser.parse(tokens))
                if trees:
                    ans = random.choice(trees)
                    break
            if ans:
                f.write(str(ans).replace('\n', '') + "\n")
            else:
                f.write("()\n")

generate_10k_sentences()
parse_input_file()
generate_random_sentence()
