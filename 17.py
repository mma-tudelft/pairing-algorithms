import csv
import numpy as np
from scipy.spatial.distance import cosine
import math

with open('Sheet_1.csv', 'rb') as cvsfile:
    reader = csv.reader(cvsfile, delimiter = ",", quotechar="\"")
    header = reader.next()
    identifiers = []
    scores = {}
    for row in reader:
        # Store the identifier and corresponding scores
        identifiers.append(row[9])
        identifier     = row[9]
        ratings     = map(int, [x if x is not '' else '0' for x in row[10:]])
        scores[identifier] = ratings    

def cosine_similarity(p, q):
        numer = np.sum(np.multiply(p,q))
        denom = np.sqrt(np.sum(np.square(p)))*np.sqrt(np.sum(np.square(q)))
    
        if denom is not 0:
            return float(numer) / denom
        else:
            return 0.0
        
def euclidean_distance(p,q):
    d = 0
    for i in range(len(p)):
        d += (p[i] - q[i])**2
    return math.sqrt(d)

def normalize_vector(p, maximum):
    return [float(x) / maximum for x in p]

M = []
for m in scores:
    M.append(scores[m])

def dot_product(p, q):
    d = 0
    for i in range(len(p)):
        d += p[i] * q[i]
    return d
    
def distance_matrix(vectors):
    result = []
    N = len(vectors)
    for i in range(N):
        for j in range(i+1,N):
            ind = (i,j)
            a_cos = cosine_similarity(vectors[i] - np.mean(vectors), vectors[j] - np.mean(vectors))
            result.append( (ind, abs(a_cos)) )
        
    return result

D = distance_matrix(M)
D_sorted = sorted(D, key=lambda D: D[1])

free_participants = range(len(identifiers))
pairs = []
D_sorted.reverse()

while len(free_participants) > len(free_participants)%2:
    # add next closest pair
    closest_pair = D_sorted.pop()
    pairs.append(closest_pair)

    # indicate participants are now paired
    p = closest_pair[0][0]
    q = closest_pair[0][1]
    free_participants.remove(q)
    free_participants.remove(p)

    # remove the newly paired participants from the distance matrix
    for i in range(len(D_sorted)-1,-1,-1):
        if p in D_sorted[i][0] or q in D_sorted[i][0]:
            del D_sorted[i]

print ("The pairs with corresponding points are:")
for p in pairs:
    print (identifiers[p[0][0]], identifiers[p[0][1]], p[1])
print(identifiers[free_participants[0]] + " is the only one over and can be placed with another group")
