import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, invgamma

# start parameters
mu_prior = 3
sigma_prior = 0.7

# Observed event
x_observed = 4.5

# Prior-distribution
prior_distribution = norm(mu_prior, sigma_prior)

#Starting parameters
a0 = 1
b0 = 1

# Compute posterior parameters (unknown mean and variance)
a_n = a0 + 0.5
b_n = b0 + 0.5 * (1 / sigma_prior**2 + (x_observed - mu_prior)**2 / (1 + 1 / sigma_prior**2))
mu_n = (a0 * mu_prior + 1 / sigma_prior**2 * x_observed) / (a0 + 1 / sigma_prior**2)
sigma_n = np.sqrt(1 / (a_n * b_n))

posterior_distribution = norm(mu_n, sigma_n)

# Plot results
x_values = np.linspace(mu_prior - 5 * sigma_prior, mu_prior + 5 * sigma_prior, 1000)
print(x_values)
plt.plot(x_values, prior_distribution.pdf(x_values), label='Prior')
plt.plot(x_values, posterior_distribution.pdf(x_values), label='Posterior')
plt.axvline(x=x_observed, color='red', linestyle='--', label='Observed value')
plt.title('Bayesian Inference of Gaussian Distribution')
plt.xlabel('X')
plt.ylabel('P[X]')
plt.legend()
#plt.savefig('figure_Gaussian2.png', dpi=600, bbox_inches='tight')
plt.show()

