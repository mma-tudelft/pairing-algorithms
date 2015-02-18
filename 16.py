import numpy as np
import csv

print "---Chak Shun's pairing algorithm---"
def sim(u,v):
    return pearson(u,v)

def pearson(u,v):
    umc = []
    vmc = []
    for x in range(len(u)):
        if(u[x]>0 and v[x]>0):
            umc.append(u[x]-np.mean(u))
            vmc.append(v[x]-np.mean(v))
    numer = np.sum(np.multiply(umc,vmc))
    denom = np.sqrt(np.sum(np.square(umc)))*np.sqrt(np.sum(np.square(vmc)))
    if denom != 0.0:
        return float(numer)/float(denom)
    else:
        return 0.0
    
with open('Sheet_1.csv', 'rb') as cvsfile:
    reader = csv.reader(cvsfile, delimiter = ",", quotechar="\"")
    header = reader.next()
    identifiers = []
    scores = {}
    score = []
    counter = 0
    for row in reader:
        identifier = row[9]
        identifiers.append(identifier)
        ratings = map(int, [x if x is not '' else '0' for x in row[10:]])
        scores[identifier] = ratings
        
    results = []
    N = len(identifiers)
    for i in range(N):
        for j in range(i+1,N):
            results.append(((identifiers[i],identifiers[j]), sim(scores[identifiers[i]],scores[identifiers[j]])))
    
    results_sorted = sorted(results, key=lambda results:results[1])
    free_participants = identifiers
    pairs = []
    
    while len(free_participants) > 0 and len(free_participants) != 3:
        # Add next closest pair
        closest_pair = results_sorted.pop()
        pairs.append(closest_pair)
        
        # Indicate participants are now paired
        p = closest_pair[0][0]
        q = closest_pair[0][1]
        free_participants.remove(p)
        free_participants.remove(q)
        
        # Remove the newly paired participants from the distance matrix
        for i in range(len(results_sorted)-1,-1,-1):
            if p in results_sorted[i][0] or q in results_sorted[i][0]:
                del results_sorted[i]
                
    if len(free_participants) == 3:
        a = results_sorted.pop()
        b = results_sorted.pop()
        c = results_sorted.pop()
        if b[0][0] != a[0][0] and b[0][0] != a[0][1]:
            third = b[0][0]
        else:
            third = b[0][1]
        pairs.append(((a[0][0],a[0][1],third),min(a[1],b[1],c[1])))
    for p in pairs:
        print p
