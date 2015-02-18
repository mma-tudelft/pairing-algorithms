import csv
import math
import numpy as np

def euclidean_distance(p,q):
    d = 0
    for i in range(len(p)):
        d += (p[i] - q[i])**2
    return math.sqrt(d)

def normalize_vector(p, maximum):
    return [float(x) / maximum for x in p]

def distance_matrix(vectors):
    result = []
    N = len(vectors)
    for i in range(N):
        for j in range(N):
            ind = (i,j)
            dis = euclidean_distance(vectors[i], vectors[j])
            result.append( (ind, dis) )
    
    return result

def cosine_similarity(p, q):
    numer = np.sum(np.multiply(p,q))
    denom = np.sqrt(np.sum(np.square(p)))*np.sqrt(np.sum(np.square(q)))

    if denom is not 0:
        return float(numer) / denom
    else:
        return 0.0

def dot_product(p, q):
    result = 0
    for i in range(len(p)):
        result += p[i] * q[i]
    return result

names = []
with open('Sheet_1.csv', 'rb') as cvsfile:
    reader = csv.reader(cvsfile, delimiter = ",", quotechar="\"")
    header = reader.next()
    identifiers = []
    
    scores = {}
    for row in reader:
        # Store the identifier and corresponding scores
        identifier     = row[9]
        names.append(identifier)
        ratings     = map(int, [x if x is not '' else '0' for x in row[10:]])
        scores[identifier] = ratings    

# raw keys and values
#for key, value in scores.iteritems():
#    print key, value

# M becomes a list holding all values per person
M = []
KEYS = []
for key, value in scores.iteritems():
    M.append(normalize_vector(value, 5.0))
    KEYS.append(key)

D = distance_matrix(M)
D_sorted = sorted(D, key=lambda D: D[1])
# now D_sorted is a sorted list of euclidean distance matches

# dot product
dot_prod = []
for row in range(len(D_sorted)):
    p = D_sorted[row][0][0]
    q = D_sorted[row][0][1]
    dot_prod.append(dot_product(M[p], M[q]))

# for cosine similarity
Cos_sim = []
for row in range(len(D_sorted)):
    p = D_sorted[row][0][0]
    q = D_sorted[row][0][1]
    Cos_sim.append(cosine_similarity(M[p], M[q]))
    
# get mean value for every item
sum_students = len(M)
items = len(M[1])
mean_values = []
for x in range(items):
    sum_values = 0
    for row in range(len(M)):
        if (M[row][x] > 0):
            sum_values += M[row][x]
    mean_values.append(sum_values / sum_students)
        
# now calculating adjusted cosine similarity
adjusted_cos_sim = []
for row in range(len(D_sorted)):
    p = D_sorted[row][0][0]
    q = D_sorted[row][0][1]
    pmean = []
    qmean = []
    for i in range(items):
        pmean.append(M[p][i] - mean_values[i])
        qmean.append(M[q][i] - mean_values[i])
    adjusted_cos_sim.append(math.fabs(cosine_similarity(pmean, qmean)))

# creating one list with all matchers
matching = []
for row in range(len(D_sorted)):
    matching.append([D_sorted[row], dot_prod[row], Cos_sim[row], adjusted_cos_sim[row]])

# while loop through list for amount of students
student = 0
text_file = open("output.txt", "w")
while (student < sum_students):
# loop through list once to get all matches of (x,y) for x
    matchlist = []
    for i in range(len(matching)):
        if ((matching[i][0][0][0] == student) and (matching[i][0][0][1] != student)):
            matchlist.append(matching[i])
# loop through THAT list matching for highest score and listing it
    sortlist = sorted(matchlist, key=lambda matchlist: matchlist[3])
    #sortlist.reverse()
# print first elements said list
    for i in range(5):
        student2 = sortlist[i][0][0][1]
        print "match number " + str(i+1) + " for student " + str(student) + " (" + names[student] + ") is student " + str(student2) + " (" + names[student2] +  ") with score: " + str(sortlist[i][3]) + " \n"
        text_file.write("match number " + str(i+1) + " for student " + str(student) + " (" + names[student] + ") is student " + str(student2) + " (" + names[student2] +  ") with score: " + str(sortlist[i][3]) + " \n")
    print "\n"
    text_file.write("\n")
    student+= 1
    
text_file.close()
    
#text_file = open("output.txt", "w")
#for row in range(len(D_sorted)):
    #text_file.write(str(D_sorted[row][0]) + " " + str(dot_prod[row]) + " " + str(Cos_sim[row]) + " " + str(adjusted_cos_sim[row]) + "\n")
    #print str(D_sorted[row][0]) + " " + str(dot_prod[row]) + " " + str(Cos_sim[row]) + " " + str(adjusted_cos_sim[row])
#text_file.close()
#for (i,d) in D_sorted:
#    print(i,d)
