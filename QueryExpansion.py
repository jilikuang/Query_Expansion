import Computation


class QueryExpansion:

    a = 1           # original Query Weight recommended in the book
    b = 0.75        # Related Document Weight
    c = 0.15        # Non-Related Document Weight

    def __init__(self):
        self.stop_words = self.read_stop_words()

    def read_stop_words(self):
        f = open('stopwords.txt', 'r')
        L = f.read().splitlines()
        S = set()
        for str in L:
            S.append(str)
        return S

    # count the frequencies of the terms
    def get_word_count(self, input):
        input = input.replace(",", " ").replace(".", " ").replace(":", " ").replace("-", " ").replace("?", " ")
        words = input.split(" ")
        Set = {}
        for word in words:
            if word == '' or word in self.stop_words:       # word should not be a stop word
                continue                                    # might be empty because we replace symbol by space
            if word not in Set:
                Set[word] = 1
            else:
                Set[word] += 1
        return Set


    def compute(self, R, NR):
        return 0


