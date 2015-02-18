import csv
import numpy as np
from math import sqrt
from scipy.spatial.distance import cosine
    
def cosine_similarity(p, q):
    numer = np.sum(np.multiply(p,q))
    denom = np.sqrt(np.sum(np.square(p)))*np.sqrt(np.sum(np.square(q)))

    if denom is not 0:
        return float(numer) / denom
    else:
        return 0.0
        
def normalize_vector(p,maximum):
    return [float(x) / maximum for x in p]

def distance_matrix(vectors):
    result = []

    N = len(vectors)
    for i in range(N):
        for j in range(i+1,N):
            ind = [i,j]
            dis = cosine_similarity(vectors[i], vectors[j])
            result.append( (ind, dis) )
            
    return result


            
with open('Sheet_1.csv', 'rb') as cvsfile:
    reader = csv.reader(cvsfile, delimiter = ",", quotechar="\"")
    header = reader.next()
    identifiers = []
    scores = {}
    for row in reader:
        # Store the identifier and corresponding scores
        identifier     = row[9]
        identifiers.append(identifier)
        ratings     = map(int, [x if x is not '' else '0' for x in row[10:]])
        scores[identifier] = ratings    
        
    #adjust the scores using the mean
    adjscores = {}    
    adjratings = []
    for key, v in scores.iteritems():
        # Avoid counting 0's when calculating the mean
        leng = 0
        for score in v:
            if (score != 0):
                leng = leng + 1
        mean = sum(v)/leng
        adjrow = []
        for score in v:
            adjrow.append(score-mean)
        adjratings.append(adjrow)
        i = 0
    for identifier in identifiers:
        adjscores[identifier] = adjratings[i]
        i = i + 1
    
    M = []
    for identifier in identifiers:
        m = adjscores[identifier]
        M.append(normalize_vector(m,5))
    D = distance_matrix(M)

    D_sorted = sorted(D, key=lambda D: D[1])

        
    pairs = []
    free_participants = list(identifiers)
    D_sorted.reverse()
    D_odd = list(D_sorted)

    while len(free_participants) > 1:
        pair_result = D_sorted.pop()
        closest_pair = pair_result[0]
        score = pair_result[1]
        
        pairs.append([closest_pair,score])
        
        p = closest_pair[0]
        q = closest_pair[1]
        free_participants.remove(identifiers[p])
        free_participants.remove(identifiers[q])
        for i in range(len(D_sorted)-1,-1,-1):
            if p in D_sorted[i][0] or q in D_sorted[i][0]:
                del D_sorted[i]
                
    #If there is an odd amount of participants
    if (len(free_participants) == 1):
        last = free_participants[0]
        closest_to_last = -1
        paired_with_closest = -1
        index = -1
        score = -1
        
        i = 0
        while closest_to_last == -1:
            if last == identifiers[D_odd[i][0][0]]:
                closest_to_last = D_odd[i][0][1]
            elif last == identifiers[D_odd[i][0][1]]:
                closest_to_last = D_odd[i][0][0]
            i = i + 1
            
        j = 0
        while paired_with_closest == -1:
            if closest_to_last == pairs[j][0][0]:
                paired_with_closest = pairs[j][0][1]
                score = pairs[j][1]
            elif closest_to_last == pairs[j][0][1]:
                paired_with_closest = pairs[j][0][0]
                score = pairs[j][1]
            j = j + 1

        for p in pairs:
            if p == [[closest_to_last,paired_with_closest],score]:
                pairs.remove([[closest_to_last,paired_with_closest],score])
            elif p == [[paired_with_closest,closest_to_last],score]:
                pairs.remove([[paired_with_closest,closest_to_last],score])
        pairs.append([[last,closest_to_last,paired_with_closest],score])
        
    #print the pairs    
    pairs.reverse()
    for p in pairs:
        pair = []
        for i in p:
            if isinstance(i,list):
                for name in i:
                    if isinstance(name,int):
                        pair.append(identifiers[name])
                    else:
                        pair.append(name)
            else:
                pair.append(i)
        
        print pair
