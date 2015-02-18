import csv
import numpy as np
import operator

def average(scorelist):
	return np.average(scorelist)

def adjusted_cosine_similarity(score1, score2):
	avg1 = np.average(score1)
	avg2 = np.average(score2)
	numer = np.sum(np.multiply(np.subtract(score1,avg1),np.subtract(score2,avg2)))
	denom = np.sqrt(np.sum(np.square(np.subtract(score1,avg1))))*np.sqrt(np.sum(np.square(np.subtract(score2,avg2))))
	if denom is not 0:
		return float(numer) / denom
	else:
		return 0.0

with open('Sheet_1.csv', 'rb') as cvsfile:
	reader = csv.reader(cvsfile, delimiter = ",", quotechar = "\"")
	header = reader.next()
	scores = {}
	names = {}
	for row in reader:
		identifier = row[9]
		ratings = map(int, [x if x is not '' else '0' for x in row[10:]])
		scores[identifier] = ratings
		names[identifier] = row[6]
	similarity = {}
	alreadycalculated = []
	for person1 in scores:
		alreadycalculated.append(person1)
		for person2 in scores:
			if person2 not in alreadycalculated:
				similarity[(person1,person2)] = adjusted_cosine_similarity(scores[person1],scores[person2])
	ordered_similarity = sorted(similarity.items(), key=operator.itemgetter(1), reverse=True)
	av_vec = [pair[1] for pair in ordered_similarity]
	overall_average = np.average(av_vec)
	deviance = [(pair[0],np.absolute(pair[1] - overall_average)) for pair in ordered_similarity]
	deviance = sorted(deviance, key=operator.itemgetter(1))
	bestpairs = []
	alreadypaired = []
	for pair in deviance:
		if((pair[0][0] not in alreadypaired) and (pair[0][1] not in alreadypaired)):
			alreadypaired.append(pair[0][0])
			alreadypaired.append(pair[0][1])
			bestpairs.append((pair[0],adjusted_cosine_similarity(scores[pair[0][0]],scores[pair[0][1]])))
	i = 1
	for pair in bestpairs:
		print str(i) + ". " + pair[0][0] + pair[0][1] + " %.2f" % pair[1] + " (" + names[pair[0][0]] + ", " + names[pair[0][1]] + ")"
		i += 1