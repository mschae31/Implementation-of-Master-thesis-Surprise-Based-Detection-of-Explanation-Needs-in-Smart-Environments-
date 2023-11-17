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
    term1 = np.log(1/(sum_alpha-1))
    term2 = (np.log(alpha2[index]-1)
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
a[16]+=100
b[0]+=100
b[5]+=100
b[10]+=100
b[14]+=100
b[16]+=100"""

#Carol has the same model with the same fail at home
"""a[0]+=100
a[5]+=100
a[10]+=100
a[11]+=5
a[15]+=100
a[16]+=100
b[0]+=100
b[5]+=100
b[10]+=100
b[11]+=5
b[15]+=100
b[16]+=100"""


sum_alpha = sum(a)
events= []

for i in range(len(data)):

    if data[i] not in events:
        events.append(data[i])
    index = events.index(data[i])


    if(b[index]==0):
        b[index] += 2
        sum_alpha += 2
        a[index] += 1
    else:
        b[index] += 1   # Posterior
        sum_alpha += 1     # Sum of alpha of b (posterior)

 
    # Check if it was surprising
    if(KL_dirichlet(a,b,index,sum_alpha) > 0.51/a[index]): # and a[index]>1): (excludes events first time seen)
        print("This was surprising! At time "+ str(i+1) + 
              ", we have event " + str(data[i]) + " with KL " +
                str(round(KL_dirichlet(a,b,index,sum_alpha)*a[index],3)))   

    #Print when coffeemachine fail occurs to check if it was detected as surprising 
    """if(data[i]==("Waiting,Stopping")):
        print("Fail! At time "+ str(i+1) + ", we have event " + 
              str(data[i]) + " with KL " + str(round(KL_dirichlet(a,b,index,sum_alpha)*a[index],3))

        # When choosing alternatives as distance measures the probability will be important:
        print("Probability of event is " + str(b[index]/sum_alpha)) """  

    # Posterior is the prior in the next iteration
    a[index] += 1  
    

end = time.time()
time = end - start

#print(f'The execution time is {time}s')