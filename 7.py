import csv
import numpy as np
from scipy.spatial.distance import cosine

def pearson_similarity(p, q):
    p0 = np.nonzero(p)[0]
    numer = 0
    psqr = 0
    qsqr = 0
    for z in p0:
        if q[z] !=0:
            numer+= np.multiply(p[z],q[z])
            psqr+= np.square(p[z])
            qsqr+= np.square(q[z])
    denom = np.sqrt(psqr)*np.sqrt(qsqr)

    if denom is not 0:
        return float(numer) / denom
    else:
        return 0.0

def dot_product(p,q):
    return np.dot(p,q)

def average(p):
    n = np.nonzero(p)[0]
    tot = 0
    for a in n:
        tot += p[a]
    return float(tot)/len(n)   

with open('Sheet_1.csv', 'rb') as cvsfile:
    reader = csv.reader(cvsfile, delimiter = ",", quotechar="\"")
    header = reader.next()
    identifiers = []
    scores = {}
    av = []
    for row in reader:
        # Store the identifier and corresponding scores
        identifier 	= row[9]
        ratings 	= map(int, [x if x is not '' else '0' for x in row[10:]])
        scores[identifier] = ratings
        av.append(average(ratings))	
       

result = []
k = scores.keys()
matches = []

adjscore = scores
for m in scores:
    avg = average(scores[m])
    avr = []
    for x in scores[m]:
        if x !=0:
            avr.append(x-avg)
        else:
            avr.append(0)
    adjscore[m] = avr

    
for a in scores:
    k.remove(a)
    for b in k:
        matches.append(((a,b),pearson_similarity(adjscore[a],adjscore[b])))

D_sorted = sorted(D, key=lambda D: D[1])

free_participants = scores.keys()
    
pairs = []

while len(free_participants) > 1:
    # add next closest pair
    closest_pair = D_sorted.pop()[0]
    pairs.append(closest_pair)

    # indicate participants are now paired
    p = closest_pair[0]
    q = closest_pair[1]
    free_participants.remove(q)
    free_participants.remove(p)

    # remove the newly paired participants from the distance matrix
    for i in range(len(D_sorted)-1,-1,-1):
        if p in D_sorted[i][0] or q in D_sorted[i][0]:
            del D_sorted[i]
    
sort = sorted(D, key=lambda D:D[1])
while len(free_participants)>0:
    closest_pair = sort.pop()[0]
    if closest_pair[0] == free_participants[0]:
        for pr in pairs:
            if pr[0] == closest_pair[1] or pr[1] == closest_pair[1]:
                pairs.remove((pr[0],pr[1]))
            pairs.append((pr[0],pr[1],free_participants[0]))
            break
        free_participants.remove(free_participants[0])
    elif closest_pair[1] == free_participants[0]:
        for pr in pairs:
            if pr[0] == closest_pair[0] or pr[1] == closest_pair[0]:
                pairs.remove((pr[0],pr[1]))
            pairs.append((pr[0],pr[1],free_participants[0]))
            break
        free_participants.remove(free_participants[0])
        
for pr in pairs:
    print pr
