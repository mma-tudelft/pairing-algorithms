import csv
import numpy as np
from scipy.spatial.distance import cosine

def cosine_similarity(p, q):
    numer = np.sum(np.multiply(p,q))
    denom = np.sqrt(np.sum(np.square(p)))*np.sqrt(np.sum(np.square(q)))

    if denom is not 0:
        return float(numer) / denom
    else:
        return 0.0
        
def adjusted_cosine_similarity(p, q):
    numer = np.sum(np.multiply((p-np.mean(p)),(q-np.mean(q))))
    denom = np.sqrt(np.sum(np.square(p-np.mean(p))))*np.sqrt(np.sum(np.square(q-np.mean(q))))

    if denom is not 0:
        return float(numer) / denom
    else:
        return 0.0

with open('Sheet_1.csv', 'rU') as cvsfile:
    reader = csv.reader(cvsfile, delimiter = ",", quotechar="\"")
    header = reader.next()
    identifiers = []
    scores = {}
    for row in reader:
        # Store the identifier and corresponding scores
        identifier 	= row[9]
        ratings 	= map(int, [x if x is not '' else '0' for x in row[10:]])
        scores[identifier] = ratings
        identifiers.append(identifier)

result = []
for i in range(len(scores)):
    for j in range(i):
        v1_index = identifiers[i]
        v2_index = identifiers[j]
        # dot_product = dot(scores[i], scores[j])
        # cosine = cosine_similarity(scores[i], scores[j])
        adjusted_cosine = adjusted_cosine_similarity(scores[v1_index], scores[v2_index])
        ind = (v1_index, v2_index)
        result.append( (ind, adjusted_cosine) )

result_sorted = sorted(result, key=lambda result: result[1])
free_participants = identifiers;
pairs = []
# result_sorted.reverse()

while len(free_participants) > 1:
    # add next closest pair
    magic = result_sorted.pop()
    closest_pair = magic[0]
    pairs.append(magic)

    # indicate participants are now paired
    p = closest_pair[0]
    q = closest_pair[1]
    free_participants.remove(q)
    free_participants.remove(p)

    # remove the newly paired participants from the adjusted cosine matrix
    for i in range(len(result_sorted)-1,-1,-1):
        if p in result_sorted[i][0] or q in result_sorted[i][0]:
            del result_sorted[i]
    
for index, p in enumerate(pairs):
    print index, p

if len(free_participants) > 0:
    print free_participants.pop()
