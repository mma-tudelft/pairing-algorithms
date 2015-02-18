import csv
import numpy as np
from scipy.spatial.distance import cosine

def dot_product(p, q):
    """
    dot_product returns the dot_product between the input: Two vectors p and q.
    """
    
    return np.sum(np.multiply(p,q))

def cosine_similarity(p, q):
    """
    cosine_similarity returns the similarity between the input: Two vectors
    p and q. It uses the standard function for cosine similarity, the dot product
    divided by the lengths of the vectors
    """
    
    numer = dot_product(p,q)
    denom = np.sqrt(np.sum(np.square(p)))*np.sqrt(np.sum(np.square(q)))

    if denom is not 0:
        return float(numer) / denom
    else:
        return 0.0
        
def adjusted_cosine_similarity(p, q):
    """
    Adjusted_cosine_similarity returns the similarity between the input:
    Two vectors p and q. It uses the mean of both vectors to calculate
    the similarity on mean-centered vectors instead of just the normal
    ratings
    """

    #calculate the mean subtracted value
    diff_mean_p = np.subtract(p, float(np.sum(p)) / len(p))
    diff_mean_q = np.subtract(q, float(np.sum(q)) / len(q))
    
    numer = dot_product(diff_mean_p,diff_mean_q)
    denom = np.sqrt(np.sum(np.square(diff_mean_p)))*np.sqrt(np.sum(np.square(diff_mean_q)))
    
    if denom is not 0:
        return float(numer) / denom
    else:
        return 0.0

def compute_similarities(scores_m, sim_function):
    """
    compute_similarities computes the list of similarities for all pairs of students sorted
    from highest to lowest. The input is the scores matrix/list and the function of choice
    for calculating the similarity.
    """
    
    temp = []
    list_of_scores = []
    for key1 in scores_m:
        #use a list to keep record of who already has been matched
        temp.append(key1)
        for key2 in scores_m:
            if key2 not in temp:
                list_of_scores.append(((key1, key2), sim_function(scores_m[key1], scores_m[key2])))
    return sorted(list_of_scores, key = lambda list_of_scores : list_of_scores[1], reverse = True)




#Start reading the info from the file
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

#compute the similarities with the similarty function of choice
s_sorted = compute_similarities(scores, adjusted_cosine_similarity)

free_students = scores.keys()
result = []

idx = 0 #We use an index to traverse the list, because we want to keep the list items

#Calculate the matches using a greedy algorithm based on the highest
#similarity
while free_students:
    if len(free_students) == 1:
        #Iterate the pairs again to match this student with the student that has
        #highest similarity. This match will no longer be a duo, but have three people
        idx = 0
        while free_students:
            c_p = s_sorted[idx] 
            if free_students[0] in c_p[0]:
                other_student = c_p[0][0] if free_students[0] == c_p[0][1] else c_p[0][1]
                for idx in range(len(result)):
                    if other_student in result[idx][0]:
                        result[idx][0].append(free_students[0])
                        free_students = []
                    
            idx += 1
    else:
        c_p = s_sorted[idx]
        if c_p[0][0] in free_students and c_p[0][1] in free_students:
            result.append(([c_p[0][0], c_p[0][1]], c_p[1]))
            free_students.remove(c_p[0][0])
            free_students.remove(c_p[0][1])
        idx += 1

#Print our matchings
for (m,s) in result:
    print m, s
