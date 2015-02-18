import math
import csv
import numpy as np

print("Matching Pairs")

def normalize_vector(p,maximum):
    #normalize vector by dividing all terms by the maximum
    return [float(x)/maximum for x in p]

def mean_center(vector):
    #average vector value from all entries
    collection = 0
    for m in vector:
        collection += m
    average =  collection/len(vector)
    return average    
        
def adjusted_cosine(p,q):
    mean_p = mean_center(p)
    mean_q = mean_center(q)
    numer = np.sum(np.multiply(np.subtract(p,mean_p),np.subtract(q,mean_q)))
    denom = math.sqrt(np.sum(np.square(np.subtract(p,mean_p)))*math.sqrt(np.sum(np.square(np.subtract(q,mean_q)))))
    if denom is not 0:
        return float(numer) / denom
    else:
        return 0.0
        

    
with open('Sheet_1.csv', 'rb') as cvsfile:
    reader = csv.reader(cvsfile, delimiter = ",", quotechar="\"")
    header = reader.next()
    identifiers = []
    scores = {}
    for row in reader:
        # Store the identifier and corresponding scores
        identifier = row[9]
        ratings = map(int, [x if x is not '' else '0' for x in row[10:]])
        identifiers.append(identifier)
        scores[identifier] = ratings
        
def similarity_matrix(vectors,ids):
    result = []
    N = len(vectors)
    for i in range(N):
        for j in range(i+1,N):
            ind = (i,j)
            cos_sim = adjusted_cosine(normalize_vector(vectors[ids[i]],np.amax(vectors[ids[i]])),normalize_vector(vectors[ids[j]],np.amax(vectors[ids[j]])))
            result.append( (ind[0],ind[1],cos_sim) )
    return result

SM = similarity_matrix(scores,identifiers)


D = SM
D_sorted = sorted(D, key=lambda D: D[2])
#for m in range(len(D_sorted)):
#    print(D_sorted[m])
free_participants = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
pairs = []
     

while len(free_participants) > 1:
    
    # indicate participants are now paired
    popped = D_sorted.pop()
    p = popped[0]
    q = popped[1]
    # add next closest pair
    pairs.append((identifiers[p],identifiers[q],popped[2]))
    free_participants.remove(q)
    free_participants.remove(p)
    # remove the newly paired participants from the distance matrix
    for i in range(len(D_sorted)-1,-1,-1):
        if p == D_sorted[i][0] or p == D_sorted[i][1] or q == D_sorted[i][0] or q == D_sorted[i][1]:
            del D_sorted[i]
#finally print the results            
for m in range(len(pairs)):
    print(pairs[m])
if len(free_participants)==1:
    print'People without a match:', identifiers[free_participants[0]]

