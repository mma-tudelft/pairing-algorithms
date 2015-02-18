import csv
import numpy as np
from scipy.spatial.distance import cosine

with open('Sheet_1.csv', 'rb') as cvsfile:
    reader = csv.reader(cvsfile, delimiter = ",", quotechar="\"")
    header = reader.next()
    identifiers = []

    def normalize_vector(p, maximum):
        return [float(x) / maximum for x in p]
        
    def meancentered(vector):
        total = 0
        for v in vector:
            total += v
        mean = total / len(vector)
        result = []
        for v in vector:
            value = v - mean
            result.append(value)
        return result
        
    def outputmatrix(vectors, scores):
        result = []
        N = len(vectors)
        for i in range(N):
            for j in range(i+1,N):
                ind = (i,j)
                acos = 1 - cosine(meancentered(vectors[i]),meancentered(vectors[j]))
                pair = scores.item(i) + " " + scores.item(j)
                result.append( (ind, acos, pair) )
        return result
    
    scores = {}
    for row in reader:
        # Store the identifier and corresponding scores
        identifier = row[9]
        ratings = map(int, [x if x is not '' else '0' for x in row[10:]])
        scores[identifier] = ratings

    M = []
    for key, value in scores.iteritems():
        # normalize the matrix for maximum rating of 5.
        M.append(normalize_vector(value, 5))
        # print key, value
    
    M = outputmatrix(M, scores)
    
    M_sorted = sorted(M, key=lambda M: M[1])
    for (i,d) in M_sorted:
        print(i,d)
    
