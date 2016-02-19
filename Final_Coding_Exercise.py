from collections import Counter
from numpy import mean
from scipy.spatial.distance import cosine
from scipy.stats import pearsonr
import random
import matplotlib.pyplot as plt

plt.switch_backend('TkAgg') #change the backend in case you have a different one in order for the plt.show() command to work

fig, ax = plt.subplots()

# We need to draw the canvas, otherwise the labels won't be positioned and won't have values yet.
fig.canvas.draw()

def create_user_version(tA, tB):
    user_A_ratings = random.randrange(0,101) # The number of movies this version of user A rated 
    user_B_ratings = random.randrange(0,101) # The number of movies this version of user B rated 
    
    A_indexes = [] # The indexes of the movies for A
    B_indexes = [] # The indexes of the movies for B
    A_version = [] # This version of A
    B_version = [] # This version of B
    
    for m in range(user_A_ratings): # Get a random rating from A
        temp_index = random.randrange(0,len(tA)) 
        while (temp_index in A_indexes):
            temp_index = random.randrange(0,len(tA))
        A_indexes.append(temp_index)
        A_version.append(tA[temp_index]) # Fill the list of this version

    for m in range(user_B_ratings): # Get a random rating from B
        temp_index = random.randrange(0,len(tB)) 
        while (temp_index in B_indexes):
            temp_index = random.randrange(0,len(tB))
        B_indexes.append(temp_index)
        B_version.append(tB[temp_index]) # Fill the list of this version
    
    intersection_count = list(set(A_indexes) & set(B_indexes)) # How many items belong to the intersection = number of common indexes
    intersection_elements = set(A_indexes) & set(B_indexes) # Common element indexes
    intersections.append(len(intersection_count))
    A_common = []
    B_common = []
    
    for x in range(len(intersection_elements)): # Create the lists of common elements
        tp = intersection_elements.pop()
        A_common.append(tA[tp]) 
        B_common.append(tB[tp]) 
    
    # Here we compute  Pearson Correlation
    A_version_adj = list(A_common)
    B_version_adj = list(B_common)
    
    Pearsons.append(pearsonr(A_common,B_common)[0]) # this uses only the common elements without the mean subtraction 

    # Here we compute the Adjusted Cosine Similarity
    full_tA = []
    full_tB = []
    for y in range(len(tA)): # Create full tables
        if ((y in A_indexes) and (y in B_indexes)):
            full_tA.append(tA[y])
            full_tB.append(tB[y])
        if ((y in A_indexes) and (y not in B_indexes)):
            full_tA.append(tA[y])
            full_tB.append(0)            
        if ((y not in A_indexes) and (y in B_indexes)):
            full_tA.append(0)
            full_tB.append(tB[y])   
            
    for i in range(len(full_tA)): # Adjusting vectors by subtracting their means
        full_tA[i] = float(full_tA[i]) - float(mean(full_tA))
    for i in range(len(full_tB)): # Adjusting vectors by subtracting their means
        full_tB[i] = float(full_tB[i]) - float(mean(full_tB))      
    
    Cosines.append(1 - cosine(full_tA,full_tB))

A = []
B = []
RealUser1 = [1,3,1,4,5,3,5,0,4,0,0,1,5,3,4,1,1,0,5,0,5,2,0,4,2,0,5,5,5,3,0,0,2,5,5,3,5,2,3,0,4,0,0,3,1,0,2,0,0,3,0,3,0,0,5,0,5,1,3,4,5,2,0,0,1,2,0,2,0,0,5,5,0,0,3,3,2,4,4,5,3,1,0,5,5,5,5,0,0,5,3,5,2,4,0,0,0,1,0,0,0]
RealUser2 = [0,4,3,4,5,4,4,0,1,0,2,0,5,3,4,5,3,2,4,5,0,3,1,1,2,4,5,3,3,4,0,5,5,5,1,2,5,3,2,0,4,3,4,5,3,2,3,0,3,1,4,1,2,0,5,3,4,4,5,4,5,4,2,0,3,3,4,4,5,0,3,5,0,1,4,3,5,5,4,5,3,1,4,4,5,3,4,3,0,5,4,3,3,4,0,5,3,1,0,0,0]

for r in range(100): # Randomly create 100 ratings for users A and B
    A.append(random.randrange(1,6))
    B.append(random.randrange(1,6))
		
Cosines = []
Pearsons = []
intersections = []

for i in range(1000): # Create 1000 user versions
    #create_user_version(A,B) # run the script based on the randomly generated user ratings
	create_user_version(RealUser1,RealUser2) # run the script based on the ratings of real users

plt.plot(intersections, Cosines,'ko' ,label="Adjusted Cosine")
plt.plot(intersections, Pearsons,'ro' ,label="Pearson")
plt.title("2 Real Users")
#plt.title("2 Random Users")
plt.ylabel('Similarity')
plt.xlabel('Number of intersection items')
plt.legend(bbox_to_anchor=(1, 1.1))
plt.show()
fig.savefig('CodingExercise.png', dpi=500) # saves the figure