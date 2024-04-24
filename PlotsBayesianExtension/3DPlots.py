import numpy as np
import matplotlib.pyplot as plt
from scipy import special

def KL(sum_alpha, alpha1):
    term1 = np.log(1 / (sum_alpha - 1))
    term2 = (np.log(alpha1)
             - 1 * (special.digamma(alpha1) - special.digamma(sum_alpha - 1)))
    return (term1 + term2)*alpha1 #without *alpha1 we get the KL divergence from the papers (Plot1)


sum_alpha_values = np.linspace(3, 100, 1000) #for a high range of sum_alpha we can see the "converging" of KL
alpha1_values = np.linspace(1, 100, 1000)
sum_alpha_grid, alpha1_grid = np.meshgrid(sum_alpha_values, alpha1_values)

mask = sum_alpha_grid > alpha1_grid
sum_alpha_grid_filtered = np.ma.masked_where(~mask, sum_alpha_grid)
alpha1_grid_filtered = np.ma.masked_where(~mask, alpha1_grid)
z = np.ma.masked_where(~mask, KL(sum_alpha_grid, alpha1_grid))
z = np.ma.masked_less(z, 0)

#Create 3D Plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(sum_alpha_grid, alpha1_grid, z, cmap='viridis')


ax.set_zlim(0, 1)
ax.set_xlabel(r'$\alpha_0$')
ax.set_ylabel(r'$\alpha_1$')
ax.set_zlabel('Bayesian Surprise Value')
ax.view_init(elev=17, azim=140)

#plt.savefig('3d_plot_2.png', dpi=600, bbox_inches='tight')
plt.show()
