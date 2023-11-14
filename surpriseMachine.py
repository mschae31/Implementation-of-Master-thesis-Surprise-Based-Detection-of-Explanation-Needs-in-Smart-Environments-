import numpy as np
from scipy.stats import dirichlet
from scipy.special import gamma
from scipy import special
import math
import time
import sys

with open("input_output.txt", "r") as file:
    data = file.read().splitlines()

start = time.time()

# Function for compution the Kullback-Leibler divergence
def KL_dirichlet(alpha1, alpha2, index, sum_alpha):
    #term1 = np.log(math.factorial(sum(alpha1)-1)/math.factorial(sum(alpha2)-1))
    term1 = np.log(1/(sum_alpha-1))
    term2 = 0
    """for i in range(0, len(alpha1)):
        term2 += (np.log(math.factorial(alpha2[i]-1)/math.factorial(alpha1[i]-1))
        +(alpha1[i]-alpha2[i])*(special.digamma(alpha1[i]) - special.digamma(sum(alpha1)))
        )"""
    term2 += (np.log(alpha2[index]-1)
        -1*(special.digamma(alpha1[index]) - special.digamma(sum_alpha-1))
        )  
    return term1 + term2

#Alice does not have any previous knowledge -> uniform distribution
a = np.zeros(1700, dtype="int64")  #Assume uniform-distribution as prior
b = np.zeros(1700, dtype="int64")

#Set 10 "dummy" alphas to 1 to start with sum_alpha=10 and get similar KLDs for all events at the start
for i in range(len(a)-10,len(a)):
    a[i]=1
    b[i]=1


#Bob knows how a coffee machine works from home, but there the machine makes a bigger coffee when pressing
# the button a second time
"""a[0]+=100
a[5]+=100
a[10]+=100
a[14]+=100
b[0]+=100
b[5]+=100
b[10]+=100
b[14]+=100"""

#Carol has the same model with the same fail at home
"""a[0]+=100
a[5]+=100
a[10]+=100
a[11]+=5
a[15]+=100
b[0]+=100
b[5]+=100
b[10]+=100
b[11]+=5
b[15]+=100"""


sum_alpha = sum(a)

for i in range(len(data)):

    if(data[i] == "(Doing nothing,Doing nothing)"):      # User is doing nothing
        event = 1
    elif(data[i] == "(Pressing button to start,Starting the brewing)"):
        event = 6
    elif(data[i] =="(Waiting,Brewing)"):
        event = 11
    elif(data[i] == "(Waiting,Stopping)"):
        event = 12
    elif(data[i] == "(Pressing button to stop,Stopping)"):
        event = 16
    else:
        event= 17

    index = event-1
    if(b[index]==0):
        b[index] += 2
        sum_alpha += 2
        a[index] += 1
    else:
        b[index] += 1   # Posterior
        sum_alpha += 1     # Sum of alpha of b (posterior)

 
    # Check if it was surprising
    if(KL_dirichlet(a,b,index,sum_alpha) > 0.51/a[index]):
        print("This was surprising! At time "+ str(i+1) + ", we have event " + str(data[i]) + " with KL " + str(KL_dirichlet(a,b,index,sum_alpha)*a[event-1]))   

    #Print when event 12 occurs to check if it was detected as surprising 
    #if(event==12):
    #    print("Fail! At time "+ str(i+1) + ", we have event " + 
    #          str(data[i]) + " with KL " + str(KL_dirichlet(a,b,index,sum_alpha)*a[event-1])) 
    
    # Posterior is the prior in the next iteration
    a[index] += 1  
    

#Testing how big the surprise is after all events if a new event occurs:    
#event=30000
#b[event-1]=b[event-1]+1
#print(str(KL_dirichlet(a,b,event-1,sum_alpha+1)))
#a[event-1]=a[event-1]+1
#event=15
#b[event-1]=b[event-1]+1
#print(str(KL_dirichlet(a,b,event-1,sum_alpha+2))


end = time.time()

time = end - start

print("surpriseMachine worked.")
print(f'The execution time is {time}s')