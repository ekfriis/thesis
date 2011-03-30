"""
E(L)
hmu(L)
Keep track of the parameter 'p' with a colorbar.
"""

import cmpy
import numpy as np
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt

cmap = plt.cm.jet

# max word length
maxL=15

# number of samples from the one parameter family
Np = 50
ps = np.linspace(0.01, 0.99, Np)

lines1 = []
lines2 = []

for p in ps:
	gm = cmpy.machines.Even(bias = p)
	data = gm.cmech_quantities(['El','hmu'], maxL)
	lines1.append(zip(range(maxL+1),data[0]))
	data[1].mask[0] = False
	#er = gm.entropy_rate()
	#data[1] -= er
	lines2.append(zip(range(maxL+1),data[1,:]))

fig = plt.figure()
fig.set_figheight(5)
fig.set_figwidth(10)
fig.subplots_adjust(left = 0.09, right = 0.86)
ax1 = fig.add_subplot(1,2,1)

lc1 = LineCollection(lines1)
lc1.set_array(ps)
lc1.set_cmap(cmap)

ax1.add_collection(lc1)

ax1.set_xlabel(r"$L$ [symbols]")
ax1.set_ylabel(r"$\mathbf{E}(L)$ [bits]")
ax1.axis('auto')
ax1.set_xlim((0,maxL))

ax2 = fig.add_subplot(1,2,2)

lc2 = LineCollection(lines2)
lc2.set_array(ps)
lc2.set_cmap(cmap)

ax2.add_collection(lc2)

#ax2.set_yscale('log', basey=2)

ax3 = fig.add_subplot(1,15,15)

ax2.set_xlabel(r"$L$ [symbols]")
ax2.set_ylabel(r"$h_{\mu}(L)$ [bits/symbol]")
ax2.axis('auto')
ax2.set_xlim((0,maxL))

cbar = fig.colorbar(lc2, ax3)
cbar.ax.set_ylabel("probability $p$")
cbar.ax.set_position([0.88,0.1, 0.025, 0.8])

plt.savefig("E_hmu_Even_all.pdf")
#plt.show()
