import csv
import numpy as np
from scipy.spatial.distance import cosine
import operator

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

def cosine_similarity(p, q):
	numer = np.sum(np.multiply(p, q))
	denom = np.sqrt(np.sum(np.square(p)))*np.sqrt(np.sum(np.square(q)))

	if denom is not 0:
		return float(numer) / denom
	else:
		return 0.0

def adjusted_cosine(x, y):
	avg1 = sum(x) / len(x)
	avg2 = sum(y) / len(y)

	x2 = []
	y2 = []
	for i in range(len(x)):
		# Only count movies that user x watched
		if x[i] is not 0:
			x2.append(x[i] - avg1)
			y2.append(y[i] - avg2)
	return cosine_similarity(x2, y2)

# Finding pairs:
free_keys = scores.keys() # The list of people who have not yet been paired
bestMatch = {} # Keep track of the best match for everyone in case there is an odd number of people
pairs = [] # Used to store the pairs of people
# While there are still unmatched keys
while len(free_keys) > 1:
	# In every loop, calculate the person for everyone with whom they have the highest correlation
	matches = {}

	# Calculate the max correlations for everyone
	for key in free_keys:
		maxCor = -1
		maxCorKey = ""
		for key2 in free_keys:
			if key != key2:
				c = adjusted_cosine(scores[key], scores[key2])
				if c > maxCor:
					maxCor = c
					maxCorKey = key2
		matches[key] = (maxCorKey, maxCor)
		bestMatch[key] = (maxCorKey, maxCor)

	# If two keys point to each other, create a pair
	pair_made = False
	matchKeys = matches.keys()
	for matchKey in matchKeys:
		if matchKey == matches[matches[matchKey][0]][0]:
			# Add them as pairs and remove from free_keys
			pairs.append((matchKey, matches[matchKey][0], matches[matchKey][1]))
			free_keys.remove(matchKey)
			free_keys.remove(matches[matchKey][0])
			matchKeys.remove(matches[matchKey][0])
			pair_made = True

	# Else, create a pair between the persons whose correlation is the highest
	if not(pair_made):
		matchKey = max(matches, key = operator.itemgetter(1))
		pairs.append((matchKey, matches[matchKey][0], matches[matchKey][1]))
		free_keys.remove(matchKey)
		free_keys.remove(matches[matchKey][0])

# Sort on correlation and print
pairs_sorted = sorted(pairs, key=operator.itemgetter(2))
pairs_sorted.reverse()
for i in range(0, len(pairs)):
	pair = pairs_sorted[i]
	print("%d. %s (%s, %s)" % (i + 1, "%.2f" % pair[2], pair[0], pair[1]))
	
# If there is someone left, find their best match
if len(free_keys) == 1:
	print("%s is left. Best match: %s, correlation: %s" % (free_keys[0], bestMatch[free_keys[0]][0], "%.2f" % pair[2] % bestMatch[free_keys[0]][1]))
