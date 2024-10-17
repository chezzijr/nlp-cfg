from dictionary import Dictionary 
from grammar import Grammar
from rule import Rule
import time

d = Dictionary()
r = Rule.default()
g = Grammar(d, r)

num_sentences = 10_000
start = time.perf_counter()
with open("output/samples.txt", "a") as f:
    for i in range(num_sentences):
        print(f"Generating sentence {i+1}/{num_sentences}", end="\r")
        tokens = g.generate_sentence()
        sentence = " ".join(tokens)
        f.write(sentence + "\n")
print(f"Generated {num_sentences} sentences in {time.perf_counter() - start:.2f} seconds")
