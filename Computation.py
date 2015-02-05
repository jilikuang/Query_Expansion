import math


class Computation:

    # calculate the similarity of two vectors
    @staticmethod
    def sim(vec1, vec2):
        return float(Computation.dot(vec1, vec2)/(Computation.norm(vec1)*Computation.norm(vec2)))

    # calculate the normalization of a vector
    @staticmethod
    def norm(vec):
        sum = 0
        for i in vec:
            sum += i*i
        return math.sqrt(sum)

    # calculate the inner product of two vectors
    @staticmethod
    def dot(vec1, vec2):
        sum = 0
        for i in range(0, len(vec1)):
            sum += vec1[i]*vec2[i]
        return sum
