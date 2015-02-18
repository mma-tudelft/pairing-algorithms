#NOTE: changed cvsfile into csvfile
import csv
import math

#Loads data into global variable "scores" 
with open("movie.txt","rb") as csvfile:
  reader = csv.reader(csvfile, delimiter=",", quotechar="\"")
  header = reader.next()
  identifiers = []
  scores = {}
  for row in reader:
    identifier = row[9]
    ratings = [x if x is not '' else '0' for x in row[10:]]
    scores[identifier] = map(int,ratings)

def center(p):
  sum = 0.0
  for i in range(len(p)):
    sum+= p[i]
  mean = sum/len(p)
  return [c-mean for c in p]



def dot(p,q):
  d = 0
  for i in range(len(p)):
    d+=(p[i]*p[i])
  return d

def cos(p,q):
  down = dot(p,p) * dot(q,q)
  if down==0:
    return 1
  return dot(p,q) / down

def acos(p,q):
  p =center(p)
  q =center(q)
  down = dot(p,p) * dot(q,q)
  if down==0:
    return 1
  return dot(p,q) / down



#Takes a score map (key=user, value= list of scores) and a distance function
#returns a list: ((user,otheruser),distance)

def distance_matrix(scores,disfunc):
  result =[]
  for user,scorelist in scores.iteritems():
    for otheruser,otherscorelist in scores.iteritems():
      #Prevents double pairs
      if user>otheruser:
        ind = (user,otheruser)
        dis = disfunc(scorelist,otherscorelist)
        result.append( (ind,dis) )
  return result

D = distance_matrix(scores,acos)

D_sorted = sorted(D, key =lambda D:D[1])
D_sorted.reverse()

#for (i,d) in D_sorted:
#  print (i,d)
#
#print "---------"

free_participants = len(scores)

pairs = []

while (free_participants>1):
  #Get pair
  (p,q),d = D_sorted.pop()
  #closest_pair = popped[0]
  pairs.append((p,q,d))

  #p = closest_pair[0]
  #q = closest_pair[1]

  #Say they are no longer avaible
  free_participants -= 2

  #Iterate backwards
  for i in range(len(D_sorted)-1,-1,-1):
    pairtuple = D_sorted[i][0]
    if (p in pairtuple) or (q in pairtuple):
      del D_sorted[i]


for p,q,d in pairs:
  print p,q,d

