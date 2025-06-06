# Make sure we can import from the shared library and data files
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'library')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))

# Other imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter
from matplotlib import cm
from library.functions import load_data, progressBar, zipCoords
import time

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binomtest, chi2

year=2016
exceedsTop, exceedsBottom = load_data('discrete', f'{year}', f'{500}', f'{5}perday', 'exceedTopBottom')
print(f'{year} Survival Ratio: ', exceedsBottom / (exceedsTop+exceedsBottom))

# Omitted: 0.4718, 0.3996 (2019 and 2023)
ys = [0.5505, 0.5557,  0.5817, 0.6111, 0.6269]


# Observed samples
samples = np.round(1825 * np.array(ys)).astype(int)
n = 1825
m = len(samples)

qs = []
ps = []

# Evaluate for a range of q0 values
for q0 in np.linspace(0.001, 0.999, 999):  # avoid q=0 or 1 to prevent log(0)
    # Get p-values for each sample under Bin(n, q0)
    p_values = [binomtest(x, n=n, p=q0).pvalue for x in samples]

    # Fisher's method to combine p-values
    chi2_stat = -2 * np.sum(np.log(p_values))
    p_combined = 1-chi2.cdf(chi2_stat, df=2 * m)

    qs.append(q0)
    ps.append(p_combined)
    
print(qs[ps.index(max(ps))])
print(max(ps))

# Plot the combined p-values across different q0 values
plt.figure(figsize=(8, 5))
plt.plot(qs, ps, label="Combined p-value (Fisher's method)")
#plt.axhline(0.05, color='red', linestyle='--', label='Significance level (0.05)')
plt.xlabel("q₀")
plt.ylabel("Combined p-value")
# plt.title("Probability against time, with MLE $\widehat{q}=0.58518")
plt.title("$p$-value")
plt.legend()
plt.grid(True)
plt.show()



