import Computation
import Document


class QueryExpansion:

    a = 1           # original Query Weight recommended in the book
    b = 0.75        # Related Document Weight
    c = 0.15        # Non-Related Document Weight

    def __init__(self, current_query):
        self.stop_words = self.read_stop_words('stopwords.txt')
        self.query = ['']*len(current_query)
        for i in range(0,len(current_query)):
            self.query[i] = current_query[i].lower()
        self.word_collection = []
        self.query_vector = []

    # read the stop words from a file
    @staticmethod
    def read_stop_words(path):
        f = open(path, 'r')
        L = f.read().splitlines()
        S = []
        for s in L:
            S.append(s.lower())
        return S

    # construct words group
    def construct_words_vector(self, documents):
        self.word_collection = list(self.query)
        for doc in documents:
            for word in self.get_split_words(doc.title + ' ' + doc.url + ' ' + doc.description):
                if not isinstance(word, str):
                    word = word.encode('utf-8')
                word = word.lower()
                if (word == '') or (word in self.stop_words) or (word in self.word_collection):
                    continue
                else:
                    self.word_collection.append(str(word))

    # split the words in the document
    @staticmethod
    def get_split_words(str):
        symbol_to_replace = [",",".",":","-","?","!","'","/","&","|","_","=","+","#","^",\
                             "*","~","\\","\'","\"","\u","%","$","@","(",")","[","]","{","}",\
                             "0","1","2","3","4","5","6","7","8","9"]
        temp = str
        for symbol in symbol_to_replace:
            temp = temp.replace(symbol, " ")
        return temp.split(" ")

    # compute the vector for a single document
    def compute_vector(self, doc):
        words = {}
        doc_string = [doc.description, doc.url, doc.title]
        factors = [1, 1.2, 1.5]
        for i in range(0, 3):
            for word in self.get_split_words(doc_string[i]):
                if not isinstance(word, str):
                    word = word.encode('utf-8')
                word = str(word.lower())
                if word in self.word_collection:
                    if word in words:
                        words[word] += factors[i]
                    else:
                        words[word] = factors[i]
        vector = []
        for word in self.word_collection:
            if word in words:
                vector.append(words[word])
            else:
                vector.append(0)
        return vector

    # initialize query vector
    def initialize_query_vector(self):
        self.query_vector = []
        for i in range(0, len(self.word_collection)):
            if self.word_collection[i] in self.query:
                self.query_vector.append(1)
            else:
                self.query_vector.append(0)

    # compute current query vector
    def compute_query_vector(self, documents):
        self.construct_words_vector(documents)
        self.initialize_query_vector()
        count_R = 0
        vector_R = []
        count_NR = 0
        vector_NR = []
        for doc in documents:
            if doc.is_relevant:
                count_R += 1
                v = self.compute_vector(doc)
                vector_R = Computation.Computation.sum(vector_R, v)
            else:
                count_NR += 1
                v = self.compute_vector(doc)
                vector_NR = Computation.Computation.sum(vector_NR, v)
        Computation.Computation.multiply(self.query_vector, self.a)
        Computation.Computation.multiply(vector_R, self.b/count_R)
        Computation.Computation.multiply(vector_NR, self.c/count_NR)
        self.query_vector = Computation.Computation.sum(self.query_vector, vector_R)
        self.query_vector = Computation.Computation.dif(self.query_vector, vector_NR)

    # compute new query terms
    def compute_new_term(self, documents):
        self.compute_query_vector(documents)
        word_set = {}
        for i in range(0,len(self.word_collection)):
            word_set[self.word_collection[i]] = self.query_vector[i]
        sorted_set = sorted(word_set, key=word_set.get, reverse=True)
        new_term = []
        i = 0
        while len(new_term) < 2 and i < len(sorted_set):
            word = sorted_set[i]
            i += 1
            if word in self.query or not isinstance(word, str):
                continue
            new_term.append(word)
        print 'Augmenting by ' + new_term[0] + ' ' + new_term[1]
        return new_term

    # call this function to start query expansion computation
    def get_new_query(self, documents):
        new_terms = self.compute_new_term(documents)
        return self.query + new_terms
