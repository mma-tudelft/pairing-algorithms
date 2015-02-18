import csv
import numpy as np
from scipy.spatial.distance import cosine

with open('Sheet_1.csv', 'rb') as cvsfile:
    reader = csv.reader(cvsfile, delimiter = ",", quotechar="\"")
    header = reader.next()
    identifiers = []
        
    scores = {}
    for row in reader:
        # Store the identifier and corresponding scores
        identifier  = row[9]
        ratings = map(int, [x if x is not '' else '0' for x in row[10:]])
        scores[identifier] = ratings

def meancent_vector(x):
        return [( float(p))- (np.sum(x)/len(x)) for p in x]

def cosine_similarity(p, q):
        numer = np.sum(np.multiply(p,q))
        denom = np.sqrt(np.sum(np.square(p)))*np.sqrt(np.sum(np.square(q)))
    
        if denom is not 0:
            return float(numer) / denom
        else:
            return 0.0     

def jaccard(p,q):
    y = 0
    for x in range(len(p)):
        if(p[x] > 0 & p[x] == q[x]):
            y =y+1
   
    
    a = 0
    for z in range(len(p)):
        if(p[z] > 0 or q[z]>0):
            a = a +1
    
    return (float(y)/float(a))
    
       
    
    
result = []
niet = []
y = ''
for m in scores:
    if(m not in niet):
        x = 0
        z = 0
        for n in scores:
            if n != m:
                if (n not in niet )   :
                    jacc = jaccard(scores[m],scores[n])
                    adcos=  cosine_similarity(meancent_vector(scores[m]), meancent_vector(scores[n]))
                    if adcos > x and (adcos -jacc) < 0.3 : 
                        x = adcos
                        y = n
                        z = jacc 
        niet.append(m)
        niet.append(y)
        if(z != 0):            
            result.append([x,z, m + y])
 
 
 

result.sort(reverse =True)

for i in range(len(result)):
    
    print(str(i+1)+ ". " +str((result[i])[0]) + ' ' + str((result[i])[1]) + " "+ (result[i])[2])

    


