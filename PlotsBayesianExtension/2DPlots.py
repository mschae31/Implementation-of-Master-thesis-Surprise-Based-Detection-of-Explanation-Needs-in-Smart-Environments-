import numpy as np
import matplotlib.pyplot as plt
from scipy.special import digamma

alpha_h = np.linspace(2, 10, 100)
y_digamma = digamma(alpha_h)
y_ln = np.log(alpha_h)
diff = (y_ln-y_digamma)
diff2 = (y_digamma-y_ln)

#print(np.log(1)-digamma(1)) #highest possible value for KL

#plt.plot(alpha_h, y_digamma, label='Digamma Function')
#plt.plot(alpha_h, y_ln, label='Natural Logarithm')
plt.plot(alpha_h,(np.log(alpha_h)-digamma(alpha_h))*alpha_h,label=r'upper bound of KL divergence')
plt.plot(alpha_h,(np.log(alpha_h-1)-digamma(alpha_h-1)+digamma(alpha_h)-np.log(alpha_h))*alpha_h,
          label=r'lower bound of KL divergence for $\alpha_h-1$')
#plt.plot(alpha_h,diff,label=r'ln($\alpha_h$)-$\psi$($\alpha_h$)')
#plt.plot(alpha_h,diff*alpha_h,label=r'$\alpha_h$*(ln($\alpha_h$)-$\psi$($\alpha_h$))')
plt.xlabel(r'$\alpha_h$')
plt.ylabel('y')
#plt.title('ln(alpha_h)_digamma(alpha_h)')
plt.legend()
plt.grid(True)
#plt.savefig('upper_lower_bound2.png', dpi=600, bbox_inches='tight')
plt.show()
