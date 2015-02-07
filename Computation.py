import math


class Computation:

    # calculate the similarity of two vectors
    @staticmethod
    def sim(vec1, vec2):
        return float(Computation.dot(vec1, vec2)/(Computation.norm(vec1)*Computation.norm(vec2)))

    # calculate the normalization of a vector
    @staticmethod
    def norm(vec):
        summation = 0
        for i in vec:
            summation += i*i
        return math.sqrt(summation)

    # calculate the inner product of two vectors
    @staticmethod
    def dot(vec1, vec2):
        summation = 0
        for i in range(0, len(vec1)):
            summation += vec1[i]*vec2[i]
        return summation

    # calculate the summation of two vectors
    @staticmethod
    def sum(vec1, vec2):
        if len(vec1) == 0 or len(vec2) == 0:
            return vec1 if len(vec2) == 0 else vec2
        vec = []
        for i in range(0, len(vec1)):
            vec.append(vec1[i]+vec2[i])
        return vec

    # calculate the difference of two vectors
    @staticmethod
    def dif(vec1, vec2):
        if len(vec2) == 0:
            return vec1
        vec = []
        for i in range(0, len(vec1)):
            vec.append(vec1[i]-vec2[i])
        return vec

    # calculate the multiplication of a vector by a constant
    @staticmethod
    def multiply(vec, n):
        for i in range(0, len(vec)):
            vec[i] = vec[i]*n