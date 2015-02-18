import csv
import numpy as np
import operator as op
from scipy.spatial.distance import cosine

def cosine_similarity(p, q):
    numer = np.sum(np.multiply(p,q))
    denom = np.sqrt(np.sum(np.square(p)))*np.sqrt(np.sum(np.square(q)))

    if denom is not 0.0:
        return float(numer) / denom
    else:
        return 0.0

def normalize_scores(scores, baseline):
    normalized_scores = {}
    for s in scores:
        normalized_scores[s] = scores[s]
        for i in xrange(0, len(normalized_scores[s])):
            if normalized_scores[s][i] is not 0:
                normalized_scores[s][i] = normalized_scores[s][i] - baseline[i]
            else:
                normalized_scores[s][i] = 0
    return normalized_scores

def calc_baseline(scores):
    baseline = []
    score_list = scores.values()
    for i in xrange(0, len(score_list[0])):
        count = np.count_nonzero([(x[i]) for x in score_list])
        val = np.sum([(x[i]) for x in score_list])
        if count is not 0:
            norm = (val + 0.0) / count
        else:
            norm = 0
        baseline.append(norm)
    return baseline

def find_neighbours(scores, baseline):
    neighbours = []
    for v1 in scores:
        for v2 in scores:
            if v1 == v2:
                continue
            indices = (np.nonzero(scores[v1]) and np.nonzero(scores[v2]))
            scorev1, scorev2 = np.array(scores[v1]), np.array(scores[v2])
            if (len(scorev1[indices]) is 0) or (len(scorev2[indices]) is 0):
                continue
            neighbours.append([v1, v2, cosine_similarity(scorev1[indices], scorev2[indices])])
    sorted_neighbours = sorted(neighbours, key=lambda neighbours: neighbours[2])
    return sorted_neighbours

with open('Sheet_1.csv', 'U') as csvfile:
    reader = csv.reader(csvfile, delimiter = ",", quotechar="\"")
    header = reader.next()
    identifiers = []
    scores = {}
    
    for row in reader:
        # Store the identifier and corresponding scores
        identifier = row[9]
        ratings = map(int, [x if x is not '' else '0' for x in row[10:]])
        identifiers.append(identifier)
        scores[identifier] = ratings
        
    baseline = calc_baseline(scores)
    normalized_scores = normalize_scores(scores, baseline)
    neighbours = find_neighbours(normalized_scores, baseline)
    
    free_identifiers = identifiers
    pairs = []
    while len(neighbours) > 0:
        # add next closest pair
        closest_pair = neighbours.pop()
        pairs.append((closest_pair[0], closest_pair[1], closest_pair[2])) 
    
        # indicate participants are now paired
        p = closest_pair[0]
        q = closest_pair[1]
        free_identifiers.remove(p)
        free_identifiers.remove(q)
    
        # remove the newly paired participants from the distance matrix
        for i in range(len(neighbours)-1,-1,-1):
            if p in neighbours[i][0] or p in neighbours[i][1] or q in neighbours[i][0] or q in neighbours[i][1]:
                del neighbours[i]
    for p in pairs:
        print p[0], "-", p[1], ":", round(p[2],4)
    print "Identifiers paired:", (2 * len(pairs))
    print "Leftovers:", free_identifiers
