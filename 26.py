import csv
import math
import numpy as np

def custom_taxicab(p,q):
    result = 0
    amountofmovies = 0
    for i in range(len(p)):
        if p[i] != 0 and q[i] != 0:
            amountofmovies += 1
            result += math.fabs(p[i] - q[i])
    
    if amountofmovies > 1:
        result = result / amountofmovies
    return result

def score_matrix(scores,participants):
    result = []
    N = len(participants)
    for i in range(N):
        for j in range(i+1,N):
            ind1 = participants[i]
            ind2 = participants[j]
            ind = (ind1,ind2)
            entries1 = scores[ind1]
            entries2 = scores[ind2]
            score = custom_taxicab(entries1,entries2)
            result.append((ind,score))

    return result

with open('Sheet_1.csv', 'rb') as cvsfile:
    reader = csv.reader(cvsfile, delimiter = ",", quotechar="\"")
    header = reader.next()
    scores = {}
    for row in reader:
        # Store the identifier and corresponding scores
        identifier  = row[9]
        ratings     = map(int, [x if x is not '' else '0' for x in row[10:]])
        scores[identifier] = ratings

        
participants = []
for key, value in scores.iteritems():
    participants.append(key)

M = score_matrix(scores,participants)
M_sorted = sorted(M, key=lambda M: M[1])

pairs = []
M_sorted.reverse()

while len(participants) > 1:
    # add next closest pair
    closest_pair = M_sorted.pop()
    pair = closest_pair[0]
    score = closest_pair[1]
    pairs.append((pair,score))

    # indicate participants are now paired
    p = pair[0]
    q = pair[1]
    participants.remove(q)
    participants.remove(p)

    # remove the newly paired participants from the distance matrix
    for i in range(len(M_sorted)-1,-1,-1):
        if p in M_sorted[i][0] or q in M_sorted[i][0]:
            del M_sorted[i]

place = 1            
for pair,score in pairs:
    print(str(place) + ". " + str(pair) + " " + str(round(score,3)))
    place += 1

if len(participants) == 1:
    leftover = participants[0]
    loscoring = []
    for ((p1,p2),score) in pairs:
        person1vector = scores[p1]
        person2vector = scores[p2]
        leftovervector = scores[leftover]
        loscore = custom_taxicab(person1vector,leftovervector) + custom_taxicab(person2vector,leftovervector)
        loscoring.append(((p1,p2),loscore))
    
    los_sorted = sorted(loscoring, key=lambda loscoring: loscoring[1])
    los_sorted.reverse()
    bestpairforleftover = los_sorted.pop()[0]
    
    print
    print("Leftover student is: '" + participants[0] + "'")
    print("Suggested pair for leftover student is: " + str(bestpairforleftover))
