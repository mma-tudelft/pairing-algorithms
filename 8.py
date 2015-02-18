import csv
import numpy as np

def cosine_similarity(p, q):
    numer = np.sum(np.multiply(p,q))
    denom = np.sqrt(np.sum(np.square(p)))*np.sqrt(np.sum(np.square(q)))
    
    if denom is not 0:
        return float(numer) / denom
    else:
        return 0.0
        
def jaccard(p,q):
    A = [int(x!=0) for x in p]
    B = [int(x!=0) for x in q]
    intersection = [int(A[x] == B[x] and A[x] == 1) for x in range(len(p))]
    union = [int(A[x] == 1 or B[x] == 1) for x in range(len(p))]
    return float(sum(intersection))/sum(union)

with open('Sheet_1.csv', 'U') as cvsfile:
    reader = csv.reader(cvsfile, delimiter = ",", quotechar="\"")
    header = reader.next()
    identifiers = []
    scores = {}
    for row in reader:
        # Store the identifier and corresponding scores
        identifier     = row[9]
        ratings     = map(int, [x if x is not '' else '0' for x in row[10:]])
        scores[identifier] = ratings    
    
    ranking = []
    
    for i in range(len(scores.keys())):
        for j in range(i+1, len(scores.keys())):
            A = scores[scores.keys()[i]]
            B = scores[scores.keys()[j]]
            ranking.append((scores.keys()[i],scores.keys()[j],cosine_similarity(A,B) - abs(jaccard(A,B)-0.4)))
            
    finalRanking = []
    ranked = []
    
    for x in sorted(ranking,key=lambda ranking: ranking[2], reverse=True):
        if not x[0] in ranked and not x[1] in ranked:
            finalRanking.append(x)
            ranked.append(x[0])
            ranked.append(x[1])
    
    for rank in finalRanking:
        print str(finalRanking.index(rank)+1)+'.',rank
