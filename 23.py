import csv
from math import sqrt

with open('Sheet_1.csv', 'rb') as cvsfile:
	reader = csv.reader(cvsfile, delimiter = ",", quotechar="\"")
	header = reader.next()
	identifiers = []
	scores = {}
	for row in reader:
		# Store the identifier and corresponding scores
		identifier 	= row[9]
		ratings 	= map(int, [x if x is not '' else '0' for x in row[10:]])
		scores[identifier] = ratings

def euclidean_distance(p,q):
    d = 0
    for i in range(len(p)):
        d += (p[i]-q[i])**2
    return sqrt(d)

def normalize_vector(p, maximum):
    return [float(x) /  maximum for x in p]

def distance_matrix(vectors):
    result = []
    N = len(vectors)
    for i in range(N):
        for j in range(i+1, N):
            ind = (i,j)
            dis = euclidean_distance(vectors[i], vectors[j])
            result.append( (ind, dis) )
        
    return result

namen = scores.keys()
result = []
M = []
for i in range(len(namen)):
    M.append(normalize_vector(scores.get(namen[i]), 5.0))
        
D = distance_matrix(M)
D_sorted = sorted(D, key=lambda D:D[1])

for (i, d) in D_sorted:
    print(i,d)

free_participants = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
pairs = []
D_sorted.reverse()

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

last_person = free_participants[0]
for p in pairs:
    print p
print last_person
