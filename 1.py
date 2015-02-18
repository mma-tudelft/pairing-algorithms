import csv
import numpy as np
from scipy.spatial.distance import cosine
import math

print("Exercise 1 - Pairer")

# Eaclidean distance correlation'
# Modified for when one of the students had not seen the movie,
#   because the penalty should be smaller
def euclidean_distance(p,q):
    d = 0
    for i in range(len(p)):
        if p[i] == 0:
            d += q[i]
        else:
            if q[i] == 0:
                d += p[i]
            else:
                d += (p[i] - q[i])**2
    return math.sqrt(d)

with open('Sheet_1.csv', 'rb') as cvsfile:
    reader = csv.reader(cvsfile, delimiter = ",", quotechar="\"")
    header = reader.next()
    identifiers = []
    scores = []
    indexes = {}    # List to combine students and numbers
    index = 0       # The amount of students
    for row in reader:
        # Store the identifier and corresponding scores
        identifier = row[9]
        ratings = map(int, [x if x is not '' else '0' for x in row[10:]])
        scores.append( (identifier, ratings) )   
        indexes[index] = identifier
        index +=1
        
    # Calculate each combination (n*n)
    pairs = []
    N = len(scores)
    for i in range(N):
        for j in range(N):
            if i != j:  # Calculate correlation based on the modified euc. dist.
                ind = (i,j)
                score = euclidean_distance(scores[i][1], scores[j][1])
                pairs.append( (ind, score) ) 
            else:       # You shouldn't be able to pair with yourself
                pairs.append( ((i, i), 9223372036854775807) )
                    
    # Sort the scores and reverse the list
    P_sorted = sorted(pairs, key=lambda pairs: pairs[1])
    P_sorted.reverse()
    
    result = []
    participants = range(len(P_sorted)) # List with 0 or 1 if a student was paired
    students = index                    # Remaining student
    for i in range(len(P_sorted)):
        participants[i] = 1
        
    # Greedy method for pairing
    while students > 0:
        next_best_pair = P_sorted.pop()[0]
        me = next_best_pair[0]
        you = next_best_pair[1]
        
        if students == 1:  # Last student with an uneven amount of students
            students = 0
            for i in range(len(result)):
                if you in result[i]:
                    result[i] = ( (result[i][0], result[i][1], me) )
        else:           # Make a pair if compatible
            if participants[me] and participants[you]:
                participants[me] = 0
                participants[you] = 0
                students = students - 2
                result.append(next_best_pair)
            
    # Show all the pairs
    for p in result:
        if len(p) == 2:
            print(str(indexes[p[0]]) + " " + str(indexes[p[1]]))
        else:
            print(str(indexes[p[0]]) + " " + str(indexes[p[1]]) + " " + str(indexes[p[2]]) + " (group of 3)")
