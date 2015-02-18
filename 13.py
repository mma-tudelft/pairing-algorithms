import csv
import numpy
import math
from collections import Counter
#Groepje van 3
#Returns all combinations of pairs
def combinations(vectors):
    result = []
    N = len(vectors)
    for i in range(N):
        for j in range(i+1,N):
            result.append((i,j))
    return result
#Returns a centered vector
def center_vector(p):
    mean = numpy.mean(p)
    ret = numpy.subtract(p,mean)
    return ret
#Returns the lists in with both n and m have rated a movie
def pearson_vectors(n,m):
    likelist = []
    for i in range(len(n)):
        if not(n[i]==0 or m[i]==0):
            likelist.append(i)
    newn = []
    newm = []
    for k in range(len(likelist)):
        newn.append(n[likelist[k]])
        newm.append(m[likelist[k]])
    raten = (float(len(n))-float(n.count(0)))/float(len(n))
    ratem = (len(m)-float(m.count(0)))/float(len(m))
    watchrate = raten*ratem
    return [newn,newm,watchrate]
#Returns the cosine simularity of two vectors
def cosine_similarity(p,q):
    numer = float(numpy.sum(numpy.multiply(p,q)))
    denom = float(numpy.sqrt(numpy.sum(numpy.square(p)))*numpy.sqrt(numpy.sum(numpy.square(q))))
    if denom != 0 and denom != 0.0:
        return numer / denom
    else:
        return 0.0
with open('Sheet_1.csv', 'rb') as cvsfile:
    reader = csv.reader(cvsfile, delimiter = ",", quotechar="\"")
    header = reader.next()
    identifiers = []
    scores = {}
    for row in reader:
        identifier = row[9]
        ratings = map(int, [x if x is not '' else '0' for x in row[11:]])
        scores[identifier] = ratings
    M = []
    for m in scores:
        M.append((scores[m],m))
    I = []
    CM = combinations(M)
    for (i,j) in CM:
        Z = pearson_vectors(M[i][0],M[j][0])
        #Takes the ratio of films watched by both into account (Z[2])
        I.append([(i,j),cosine_similarity(center_vector(Z[0]),center_vector(Z[1]))+Z[2],Z[2]])
    I_sorted = sorted(I, key=lambda I: I[1])
    free_participants = range(0,len(M))
    pairs = []
    #First uses the greedy approach to determine the pairs
    while len(free_participants) > 1:
        datapair = I_sorted.pop()
        closest_pair = datapair[0]
        pairs.append((closest_pair,(M[closest_pair[0]][1],M[closest_pair[1]][1]),datapair[1],datapair[2]*100))
        p = closest_pair[0]
        q = closest_pair[1]
        free_participants.remove(p)
        free_participants.remove(q)
        for i in range(len(I_sorted)-1,-1,-1):
            if p in I_sorted[i][0] or q in I_sorted[i][0]:
                del I_sorted[i]
                
    if len(free_participants) == 1:
        print "Participant with last three letters ending in",M[free_participants[0]][1],"Could not be matched"
    #If the list has an odd number of users one user cannot not be matched
    print "List using greedy approach"
    print "((p1,p2), (name1,name2), pearson simularity + bonus, watched ratio)"
    for p in pairs:
        print p
    
    current_lowest = pairs[-1][2]
    previous_lowest = 0
    while(current_lowest > previous_lowest):
        last_pair = pairs[-1][1]
        for i in range(0,len(pairs)-1):
            comp_pair = pairs[i][1]
            Z1 = pearson_vectors(scores[last_pair[0]],scores[comp_pair[0]])
            Z2 = pearson_vectors(scores[last_pair[1]],scores[comp_pair[1]])
            if((cosine_similarity(center_vector(Z1[0]),center_vector(Z1[1])))+Z1[2]>current_lowest and (cosine_similarity(center_vector(Z2[0]),center_vector(Z2[1])))+Z2[2]>current_lowest):
                insert1 = ((pairs[-1][0][0],pairs[i][0][0]),(last_pair[0],comp_pair[0]),cosine_similarity(center_vector(Z1[0]),center_vector(Z1[1]))+Z1[2],Z1[2]*100)
                insert2 = ((pairs[-1][0][1],pairs[i][0][1]),(last_pair[1],comp_pair[1]),cosine_similarity(center_vector(Z2[0]),center_vector(Z2[1]))+Z2[2],Z2[2]*100)
                del pairs[-1]
                del pairs[i]
                pairs.append(insert1)
                pairs.append(insert2)
                pairs = sorted(pairs, key=lambda pairs: pairs[2])
                pairs.reverse()
                last_pair = pairs[-1][1]
                current_lowest = pairs[-1][2]
            Z3 = pearson_vectors(scores[last_pair[1]],scores[comp_pair[0]])
            Z4 = pearson_vectors(scores[last_pair[0]],scores[last_pair[1]])
            if((cosine_similarity(center_vector(Z3[0]),center_vector(Z3[1])))+Z3[2]>current_lowest and (cosine_similarity(center_vector(Z4[0]),center_vector(Z4[1])))+Z4[2]>current_lowest):
                insert1 = ((pairs[-1][0][1],pairs[i][0][0]),(last_pair[1],comp_pair[0]),cosine_similarity(center_vector(Z3[0]),center_vector(Z3[1]))+Z3[2],Z3[2]*100)
                insert2 = ((pairs[-1][0][0],pairs[i][0][1]),(last_pair[0],comp_pair[1]),cosine_similarity(center_vector(Z4[0]),center_vector(Z4[1]))+Z4[2],Z4[2]*100)
                del pairs[-1]
                del pairs[i]
                pairs.append(insert1)
                pairs.append(insert2)
                pairs = sorted(pairs, key=lambda pairs: pairs[2])
                pairs.reverse()
                
            previous_lowest = current_lowest
            current_lowest = pairs[-1][2]
    print "List after crossing lowest scores with the highest"
    print "((p1,p2), (name1,name2), pearson simularity + bonus, watched ratio)"
    for p in pairs:
        print p
    
