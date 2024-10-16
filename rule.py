import random

rules = {
    "S": [
        ["NP", "VP"],
        ["PP", "NP", "VP"],  # bỏ qua trạng ngữ ở các vị trí giữa hoặc cuối câu
    ],
    "NP": [
        ["auxiliary", "NP"], # chính ông
        ["noun"],
        ["noun", "adjective"],
        ["noun", "adjective", "PP"],
        ["numeral", "noun"],
        ["pronoun"],
        ["determiner", "noun"],
        ["determiner", "noun", "adjective"],
        ["determiner", "noun", "adjective", "PP"],
    ],
    "VP": [
        ["adjective"],
        ["verb"],
        ["verb", "adverb"],
        ["verb", "NP"],
    ],
    "PP": [["preposition", "NP"]],
}

ReverseRule = dict[tuple[str, ...], str]

class Rule(dict[str, list[list[str]]]):
    def __init__(self, rules: dict[str, list[list[str]]]):
        super().__init__(rules)

    @classmethod
    def from_string(cls, s: str, delimiters: list[str] = ["->", "="]):
        """ string of type:
            S -> NP VP | PP NP VP
            S = NP VP | PP NP VP
        or
            S -> NP VP
            S -> PP NP VP
        """
        rules = {}
        for line in s.split("\n"):
            if not line:
                continue
            for delimiter in delimiters:
                line = line.replace(delimiter, "|")
            lhs, *rhs = line.split("|")
            lhs = lhs.strip()
            rhs = [i.split() for i in rhs]
            if lhs in rules:
                rules[lhs].extend(rhs)
            else:
                rules[lhs] = rhs
        return cls(rules)

    def reverse(self):
        """
        Instead of mapping constituents to their rules, map rules to their constituents
        """
        reverse_rules: ReverseRule = {}
        for k, v in self.items():
            for r in v:
                reverse_rules[tuple(r)] = k
        return reverse_rules

    # this will search for leave nodes from nonterminal nodes like "NP", "VP", "PP"
    # this will prevent infinite recursion
    # leave nodes are tags such as "noun", "verb", "adjective", "preposition"
    def recursively_search_for_leaves(self, symbol: str):
        if symbol not in self.keys():
            return [symbol]
        arr = [symbol]

        while any(tmp := list(map(lambda x: x in self.keys(), arr))):
            index = tmp.index(True)
            s = arr[index]
            v = self[s]
            new_v = list(filter(lambda x: set(x).isdisjoint(set(self.keys())), v))
            choice = random.choice(new_v if new_v else v)
            arr = arr[:index] + choice + arr[index + 1:]
        return arr

    @classmethod
    def default(cls):
        return cls(rules)
