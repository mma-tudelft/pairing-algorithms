import csv
import numpy as np

def pearson_corr(a,b):
    # Get the indexes of the rated movies.
    a_index = [ i > 0 for i in a]
    b_index = [ i > 0 for i in b]
    # Get the total number of rated movies.
    a_length = np.sum(a_index)
    b_length = np.sum(b_index)
    # Compute the mean of the total ratings.
    a_mean = float( np.sum(a) ) / a_length
    b_mean = float( np.sum(b) ) / a_length
    # Get the indexes of movies rated by both users.
    index = np.logical_and(a_index,b_index)
    # Total number of movies and init for Pearson Corr terms.
    N = len(a)
    product_ab = 0
    product_a = 0
    product_b = 0
    # For all movies:
    for i in range(N):
        # If it is in the intersection of a and b:
        if (index[i]):
            # Compute the terms.
            product_ab += (a[i] - a_mean) * (b[i] - b_mean)
            product_a += (a[i] - a_mean) ** 2
            product_b += (b[i] - b_mean) ** 2
    # Compute and return the correlation.
    corr = product_ab / (np.sqrt(product_a) * np.sqrt(product_b))
    return corr

def correlation_matrix(keys,vectors):
    # The number if users.
    N = len(identifiers)
    result = []
    # For all possible combinations of users:
    for i in range(N):
        for j in range(i+1,N):
            # Get the ratings for the users.
            a = identifiers[i]
            b = identifiers[j]
            # Create an index for the pair.
            ind = (a,b)
            # Compute the Pearson corr and add it to results.
            corr = pearson_corr(vectors[a],vectors[b])
            result.append( (ind, corr) )
    return result

with open('Sheet_1.csv', 'rb') as cvsfile:
    reader = csv.reader(cvsfile, delimiter = ",", quotechar = "\"")
    header = reader.next()
    ratings = {}
    for row in reader:
        # Store the identifier and corresponding scores.
        identifier = row[9]
        rating = map(int,[x if x is not '' else '0' for x in row[10:]])
        ratings[identifier] = rating

identifiers = ratings.keys()
scores = correlation_matrix(identifiers,ratings)
scores_sorted = sorted(scores, key=lambda scores: scores[1])

pairs = []
free_participants = identifiers

while len(scores_sorted) > 0:
    # Add the next best pair.
    best_match = scores_sorted.pop()
    best_pair = best_match[0]
    best_corr = best_match[1]
    pairs.append(best_match)
    # Remove the members of the pair from the free participants.
    a = best_pair[0]
    b = best_pair[1]
    free_participants.remove(a)
    free_participants.remove(b)
    # Remove the memebers of the pair out of the scores matrix.
    for i in range(len(scores_sorted)-1,-1,-1):
        if a in scores_sorted[i][0] or b in scores_sorted[i][0]:
            del scores_sorted[i]

# If there was an odd number of users, there is one user left:
if len(free_participants) > 0:
    free_part = free_participants[0]
    best_pair = 0
    new_pair = 0
    corr = -1
    # For all pairs find the best pair to match with:
    for p in pairs:
        pair = p[0]
        a = pair[0]
        b = pair[1]
        c = p[1]
        # Compute Pearson corr with each member of the pair.
        c1 = pearson_corr(ratings[free_part],ratings[a])
        c2 = pearson_corr(ratings[free_part],ratings[b])
        # Compute the mean of the correlations.
        c3 = (c1 + c2) / 2
        # If the new correlation is better than the previous:
        if c3 > corr:
            # Set a new best pair and update other variables.
            best_pair = p
            new_pair = ((a,b,free_part),(c,c3))
            corr = c3
    # Insert the new pair in the place of the original pair.
    pairs[pairs.index(best_pair)] = new_pair

# Print all the pairs.
for i in range(len(pairs)):
    res = str(i+1) + ".\t"
    p = pairs[i]
    students = p[0]
    corr = p[1]
    for s in students:
        res += " " + s
    res += "\t" + str(corr)
    print res
