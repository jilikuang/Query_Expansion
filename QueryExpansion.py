import Computation
import Document
import math
import re


class QueryExpansion:

    a = 1           # original Query Weight recommended in the book
    b = 0.75        # Related Document Weight
    c = 0.15        # Non-Related Document Weight

    def __init__(self, current_query):
        self.stop_words = self.read_stop_words('stopwords.txt')
        self.query = ['']*len(current_query)
        self.query = []
        for s in current_query:
            for w in self.get_split_words(s):
                self.query.append(w.lower())
        self.word_collection = []
        self.idf = {}
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

    # construct words group and calculate the idf for each term. The words are from the titles, urls and descriptions.
    # And we iterate each document and calculate the idf.
    def construct_words_vector(self, documents):
        self.word_collection = list(self.query)
        for term in self.query:
            self.idf[term] = 0
        for doc in documents:
            current_doc = []
            for word in self.get_split_words(doc.title + ' ' + doc.url + ' ' + doc.description):
                if not isinstance(word, str):
                    word = word.encode('utf-8')
                word = word.lower()
                if (word == '') or (word in self.stop_words):
                    continue
                else:
                    word = str(word)
                    if word not in self.word_collection:
                        self.word_collection.append(word)
                        self.idf[word] = 0
                    if word not in current_doc:
                        self.idf[word] += 1
                        current_doc.append(word)
        num = len(documents)
        for key in self.idf:
            self.idf[key] = math.log(num/self.idf[key],2)

    # split the words in the document by the symbols
    @staticmethod
    def get_split_words(string):
        stripped = ""
        for c in string:
            if 0 < ord(c) < 127:
                stripped += c
            else:
                stripped += ' '
        string = stripped
        symbol_to_replace = [",",".",":","-","?","!","'","/","&","|",";","_","=","+","#","^",\
                             "*","~","\\","\'","\"","\u","%","$","@","(",")","[","]","{","}",\
                             "0","1","2","3","4","5","6","7","8","9"]
        temp = string
        for symbol in symbol_to_replace:
            temp = temp.replace(symbol, " ")
        return temp.split(" ")

    # compute the space vector for a single document. And we use tf-idf to represent the weight
    def compute_vector(self, doc):
        words = {}
        doc_string = [doc.description, doc.url, doc.title]
        factors = [1, 1, 1.2]
        for i in range(0, 3):
            for word in self.get_split_words(doc_string[i]):
                if not isinstance(word, str):
                    word = word.encode('utf-8')
                word = str(word.lower())
                if word in self.word_collection:
                    if word in words:
                        words[word] += factors[i]*self.idf[word]
                    else:
                        words[word] = factors[i]*self.idf[word]
        vector = []
        sum = 0
        for word in self.word_collection:
            if word in words:
                vector.append(words[word])
                sum += words[word]
            else:
                vector.append(0)
        Computation.Computation.multiply(vector, 1/sum)
        return vector

    # initialize query vector
    def initialize_query_vector(self):
        self.query_vector = []
        for i in range(0, len(self.word_collection)):
            if self.word_collection[i] in self.query:
                self.query_vector.append(1)
            else:
                self.query_vector.append(0)

    # compute current query vector using the Rocchio algorithm
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

    # compute new query terms by sorting the terms by weight and adding the two terms with the highest weight to the
    # old query
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
    def get_new_query(self, documents, old_query):
        new_terms = self.compute_new_term(documents)
        return old_query + new_terms
