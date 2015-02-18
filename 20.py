import csv
import numpy as np
from scipy.stats.stats import pearsonr

# Open the csv file and read from it
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

# Create a list for the student identifiers
students = []

# Fill the list with the identifiers of the students
for student, score in scores.iteritems():
    students.append(student)
 
# Matching algorithm        
def matching(vectors):
    result = []
    N = len(vectors)
    for i in range(N):
        for j in range(i+1,N):
            ind = (students[i], students[j])
            pearson_corr = pearsonr(vectors[students[i]], vectors[students[j]])[0]
            result.append((ind, pearson_corr))
    return result

# Run the matching algorithm on the scores and sort the resulting list
D = matching(scores)    
D_sorted = sorted(D, key=lambda D: D[1])

# Create list for the pairs
pairs = []

# Determine the lower bound for the greedy algorithm based on if the number of students is odd or even
bound = 3
if len(students) % 2 == 0:
    bound = 0
    
# Run the greedy algorithm
while len(students) > bound:
    
    # Add next closest pair
    closest_pair = D_sorted.pop()
    pairs.append(closest_pair)

    # Indicate participants are now paired
    p = closest_pair[0][0]
    q = closest_pair[0][1]
    students.remove(q)
    students.remove(p)

    # Remove the newly paired participants from the distance matrix
    for i in range(len(D_sorted)-1,-1,-1):
        if p in D_sorted[i][0] or q in D_sorted[i][0]:
            del D_sorted[i]

# Open the results file
resultFile = open("result.txt", "w")

# Set the start index
index = 1

# Go over all the pairs
for p in pairs:
    
    # Print the results on the screen
    print index, "(" + p[0][0] + p[0][1] + ")", p[0][0], p[0][1], round(p[1],2)
    
    # Write the results to the file
    resultFile.write(str(index) + ". (" + str(p[0][0] + p[0][1]) + ")" + str(p[0][0]) + " " + str(p[0][1]) + " " +  str(round(p[1],2)) + "\n")
    
    # Increase the index
    index += 1
    
# Handle odd numbers of students
if bound == 3:
    # Get the last three students
    student1 = students[0]
    student2 = students[1]
    student3 = students[2]
    
    # Make them one big group
    print index, "(" + student1 + student2 + student3 + ")", student1, student2, student3, " (Mixed group because of odd number of students)"
    resultFile.write(str(index) + ". (" + student1 + student2 + student3 + ")" + student1 + " " + student2 + " " +  student3 + " (Mixed group because of odd number of students)\n")
    
# Close the results file    
resultFile.close()