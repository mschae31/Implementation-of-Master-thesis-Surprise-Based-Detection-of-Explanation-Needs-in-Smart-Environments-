import numpy as np
import matplotlib.pyplot as plt
from scipy.special import digamma
from scipy.stats import dirichlet


x = np.linspace(2, 100, 100) 

y = np.log(1 / (x-1 )) + digamma(x-1) -digamma(1)
y2 =  (np.log(1/(x-1))+ np.log(3-1) - 1*(digamma(2) - digamma(x-1)))*2
#y3 =  (np.log(1/(x-1))+ np.log(11-1) - 1*(digamma(10) - digamma(x-1)))*10


plt.figure(figsize=(10, 6))
plt.plot(x, y, label='KL divergence')
plt.plot(x,y2)
#plt.plot(x,y3)
plt.xlabel('x')
plt.ylabel('Funktionswert')
plt.title('Plot von KL divergence für sum_alpha [1, 1000]')
plt.legend()
plt.grid()
plt.show()

#If sum_alpha=sum what is then the current KLD for event seen first time - tenth time
sum=150
for i in range(1,11):
    print(str((-digamma(i)+np.log(i)+digamma(sum)+np.log(1/sum))*i)) 

#If event was observed "seen-1" times, then the current KLD for sum_alpha 1 - 15
seen=1    
for i in range(1,150):
    print(str((-digamma(seen)+np.log(seen)+digamma(i)+np.log(1/i))*seen))    
