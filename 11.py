import math
import numpy as np
import csv

with open('Sheet_1.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter = ",", quotechar="\"")
    header = reader.next()
    identifiers = []
    scores = {}
    for row in reader:
        # Store the identifier and corresponding scores
        identifier = row[9]
        ratings = map(int, [x if x is not '' else '0' for x in row[10:]])
        scores[identifier] = ratings
    
def adjusted_cosine_similarity(p,q):
    p_average = np.mean(p)
    q_average = np.mean(q)
    numer = np.sum(np.multiply(p-p_average,q-q_average))
    denom = np.sqrt(np.sum(np.square(p-p_average)))*np.sqrt(np.sum(np.square(q-q_average)))
    if denom is not 0:
        return float(numer) / denom
    else:
        return 0.0

M=[]
for a, b in scores.iteritems():
    M.append(a)

a=0;
c=[]
names = []    
n=len(M)
for i in range(n):
    names.append(M[i])
    for j in range(i+1,n):
        
        b = ((M[i], M[j]), adjusted_cosine_similarity(scores[M[i]], scores[M[j]]))
        c.append(b)
        a=a+1

c_sorted = sorted(c, key=lambda c: c[1])

free_participants = names
pairs = []

while len(free_participants) > 1:
    #add next closest pair
    closest = c_sorted.pop()
    closest_pair = closest[0]
    pairs.append(closest)
    
    # inddicate participants are now paired
    p = closest_pair[0]
    q = closest_pair[1]
    free_participants.remove(q)
    free_participants.remove(p)
    
    # remove the newly paired participants from the disance matrix
    for i in range(len(c_sorted)-1,-1,-1):
        if p in c_sorted[i][0] or q in c_sorted[i][0]:
            del c_sorted[i]

for p in pairs:
    print p
print free_participants


