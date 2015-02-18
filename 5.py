import csv
import numpy as np
from scipy.spatial.distance import cosine
from scipy.stats.stats import pearsonr
from scipy.stats.stats import spearmanr
import math

with open('Sheet_1.csv', 'rb') as cvsfile:
    reader = csv.reader(cvsfile, delimiter = ",", quotechar="\"")
    header = reader.next()
    identifiers = []
    scores = {}
    for row in reader:
        # Store the identifier and corresponding scores
        identifier = row[9]
        ratings = map(int, [x if x is not '' else '0' for x in row[10:]])
        scores[identifier] = ratings
        identifiers.append(identifier)

#This makes a new list with all the ids
ids = []
for theId,theScore in scores.iteritems():
    ids.append(theId)
   
#Test function     
def cosine_similarity(p,q):

    numer = np.sum(np.multiply(p,q))
    denom = np.sqrt(np.sum(np.square(p)))*np.sqrt(np.sum(np.square(q)))
    
    if denom is not 0:
        return float(numer) / denom
    else:
        return 0.0

#Test function
def cosine_adjusted(p,q):
    
    p_adjusted = p - np.mean(p)
    q_adjusted = q - np.mean(q)
    
    return cosine_similarity(p_adjusted, q_adjusted)
   
    
#Test function    
def cosine_adjusted_function(vectors):
    result = []
    N = len(vectors)
    for i in range(N):
        for j in range(i+1,N):
            ind = (ids[i],ids[j])
            ca = cosine_adjusted(vectors[ids[i]], vectors[ids[j]])
            result.append( (ind, ca) )
    return result     
 

#The function that works out the pearson correlation
def pearson_correlation(vectors):
    result = []
    N = len(vectors)
    for i in range(N):
        for j in range(i+1,N):
            ind = (ids[i],ids[j])
            pr = pearsonr(vectors[ids[i]], vectors[ids[j]])[0]
            result.append( (ind, pr) )
    return result    

#This line calls up the pearson_correlation function and D is then an list with all the pearson correlations 
D = pearson_correlation(scores)

#Sorts the pearson correlations with the best correlations at the bottom.
D_sorted = sorted(D, key=lambda D: D[1])
##for (i,d) in D_sorted:
##    print (i,d)


#New list where all the final pairs will go into
pairs = []

#If the number of identifiers, the number of ids, is even.
if len(identifiers) % 2 == 0:

    #While there are still indentifiers left over in the list.
    while len(identifiers) > 0:
        # add next closest pair
        closest_pair = D_sorted.pop()
        pairs.append(closest_pair)

        # indicate participants are now paired
        p = closest_pair[0][0]
        q = closest_pair[0][1]
        identifiers.remove(q)
        identifiers.remove(p)

        # remove the newly paired participants from the distance matrix
        for i in range(len(D_sorted)-1,-1,-1):
            if p in D_sorted[i][0] or q in D_sorted[i][0]:
                del D_sorted[i]
       
#If the number of identifiers is odd.       
else:
    
    #While there are more than 3 people left over in the list
     while len(identifiers) > 3:
         
        # add next closest pair
        closest_pair = D_sorted.pop()
        pairs.append(closest_pair)

        # indicate participants are now paired
        p = closest_pair[0][0]
        q = closest_pair[0][1]
        identifiers.remove(q)
        identifiers.remove(p)

        # remove the newly paired participants from the distance matrix
        for i in range(len(D_sorted)-1,-1,-1):
            if p in D_sorted[i][0] or q in D_sorted[i][0]:
                del D_sorted[i]

#The last three people who had the lowest pearson correlation scores with other people, add them to the pairs list
three = (identifiers[0], identifiers[1], identifiers[2])
pairs.append(three)

#Printing to a txt file.
f = open("thePairs.txt", "w")

for p in pairs:
    print p
    
    f.write(str(p) + "\n")
    
f.close()
    






