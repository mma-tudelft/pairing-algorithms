import csv
import numpy

identifiers = []

with open('Sheet_1.csv', 'rb') as cvsfile:
    reader = csv.reader(cvsfile, delimiter = ",", quotechar="\"")
    header = reader.next()
    scores = {}
    for row in reader:
        # Store the identifier and corresponding scores
        identifiers.append(row[9])
        identifier = row[9]
        ratings = map(int, [x if x is not '' else '0' for x in row[10:]])
        scores[identifier] = ratings    

import numpy as np
def cosine_similarity(p, q):
    numer = np.sum(np.multiply(p,q))
    denom = np.sqrt(np.sum(np.square(p)))*np.sqrt(np.sum(np.square(q)))

    if denom is not 0:
        return float(numer) / denom
    else:
        return 0.0

import math
from math import sqrt as square_root

def euclidean_distance(p,q):
    d = 0
    for i in range(len(p)):
        d += (p[i] - q[i])**2
    return math.sqrt(d)
    
def average(p):
    res = 0
    for i in p:
        res += i
    res = res/len(p)
    return res

def adjusted_cosine(p, q):
    ap = np.average(p)
    aq = np.average(q)
    numer = 0
    denom = 0
    for i in range(len(p)):
        numer = numer + (p[i] - ap) * (q[i] - aq)
    for i in range(len(p)):
        denom = denom + math.sqrt((p[i] - ap)**2) * math.sqrt((q[i] - aq)**2)

    if denom is not 0:
        return float(numer) / denom
    else:
        return 0.0

def normalize_vector(p, maximum):
    return [float(x) / maximum for x in p]

M = []
for m in scores:
    M.append(scores[m])


def distance_matrix(vectors):
    result = []
    N = len(vectors)
    for i in range(N):
        for j in range(i+1,N):
            ind = (i,j)
            sim = adjusted_cosine(vectors[i], vectors[j])
            result.append( (ind, abs(sim)) )
    return result

D = distance_matrix(M)
D_sorted = sorted(D, key=lambda D: D[1])
    
free_participants = range(len(identifiers))
pairs = []
D_sorted.reverse()

while len(free_participants) > len(free_participants)%2:
    # add next closest pair
    closest_pair = D_sorted.pop()
    pairs.append((closest_pair[0], closest_pair[1]))

    # indicate participants are now paired
    p = closest_pair[0][0]
    q = closest_pair[0][1]
    free_participants.remove(q)
    free_participants.remove(p)

    # remove the newly paired participants from the distance matrix
    for i in range(len(D_sorted)-1,-1,-1):
        if p in D_sorted[i][0] or q in D_sorted[i][0]:
            del D_sorted[i]
i = 1
for s in pairs:
    print("%d. (%s, %s) |sim| = %.4f" % (i, identifiers[s[0][0]], identifiers[s[0][1]], s[1]))
    i += 1
if len(free_participants)%2 == 1:
    print("Sadly unable to pair '%s' due to odd amount of students :(" % identifiers[free_participants[0]])
