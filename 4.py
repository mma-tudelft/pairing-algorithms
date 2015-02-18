import csv
import numpy as np

with open('Sheet_1.csv', 'rb') as cvsfile:
    reader = csv.reader(cvsfile, delimiter = ",", quotechar="\"")
    header = reader.next()
    scores = {}
    for row in reader:
        # Store the identifier and corresponding scores
        identifier = row[9]
        ratings = map(int, [x if x is not '' else '0' for x in row[10:]])
        scores[identifier] = ratings, row[7]
        

def pearson(p, q):    
    averageP = p - np.mean(p)
    averageQ = q - np.mean(q)
    numer = np.sum(np.multiply(averageP,averageQ))
    denom = np.sqrt(np.sum(np.square(p-np.mean(p))))*np.sqrt(np.sum(np.square(q-np.mean(q))))
    
    if denom is not 0:
        return float(numer) / denom
    else:
        return 0.0

keys = []
def pairing(vectors):
    for key, value in vectors.iteritems():
        keys.append(key)
    
    
    result = []
    N = len(keys)
    for i in range(N):
        for j in range(i+1,N):
            ind = (keys[i], keys[j])
            pear = pearson(vectors[keys[i]][0], vectors[keys[j]][0])
            result.append( (ind, pear, (vectors[keys[i]][1],vectors[keys[j]][1])) )
    return result

pairs = pairing(scores)

pairs_sorted = sorted(pairs, key=lambda pairs: pairs[1])

final_pairs = []
while len(keys) > 1:
    
    # add next closest pair
    closest_pair = pairs_sorted.pop()
    final_pairs.append((closest_pair))
    
    # indicate persons are now paired
    p = closest_pair[0][0]
    q = closest_pair[0][1]
    keys.remove(q)
    keys.remove(p)
    
    # remove the newly paired participants from the sorted pairs list
    for i in range(len(pairs_sorted)-1,-1,-1):
        if p in pairs_sorted[i][0] or q in pairs_sorted[i][0]:
            del pairs_sorted[i]

# output the pairs to output.txt file
outputFile = open("output.txt", "w")

for idx, p in enumerate(final_pairs):
    print p[0][0] + p[0][1], round(p[1],2), p[2]
    index = str(idx+1)
    pairscat = str(p[0][0]+p[0][1])
    coeff = str(round(p[1],2))
    names = str("(" + p[2][0] + ", " + p[2][1] + ")")
    outputFile.write(index + ". " + pairscat + " " + coeff + " " + names + "\n")
    
if len(keys) != 0:
    for i in keys:
        personLeft = "Uneven number of participants, so person not paired: " + str(i) + " (" + scores[i][1] + ")"
        print personLeft
        outputFile.write(personLeft + "\n")
    
outputFile.close()
