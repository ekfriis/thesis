"""
Make an order-3 Markov chain (as an edge hmm) and randomize the probabilities.
Plot stuff
"""

import cmpy
import numpy as np
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt

cmap = plt.cm.jet

s = "A A 0 1;\
	A D 1 1;\
	B A 0 1;\
	B D 1 1;\
	C B 0 1;\
	C E 1 1;\
	D C 0 1;\
	D H 1 1;\
	E C 0 1;\
	E H 1 1;\
	F B 0 1;\
	F E 1 1;\
	G F 0 1;\
	G G 1 1;\
	H F 0 1;\
	H G 1 1;"
	
# max word length
maxL=7

# number of samples from the one parameter family
Np = 5
ps = np.linspace(0.01, 0.99, Np)

lines1 = []
#lines2 = []

mtopology = cmpy.machines.from_string(s)


# Note : the probabilities ps are really only used as an index here
for p in ps:
	m = cmpy.machines.uniform_mealyhmm(mtopology)
	data = m.cmech_quantities(['hmu','HX0L'], maxL)
	lines1.append(zip(range(maxL+1),data[0]))
	#data[1].mask[0] = False
	#er = m.entropy_rate()
	#data[1] -= er
	#lines2.append(zip(range(maxL+1),data[1,:]))

fig = plt.figure()
#fig.set_figheight(5)
#fig.set_figwidth(10)
#fig.subplots_adjust(left = 0.09, right = 0.86)
ax1 = fig.add_subplot(1,1,1)

lc1 = LineCollection(lines1)
lc1.set_array(ps)
lc1.set_cmap(cmap)

ax1.add_collection(lc1)

ax1.set_xlabel(r"$L$ [symbols]")
ax1.set_ylabel(r"$\mathbf{E}(L)$ [bits]")
ax1.axis('auto')
ax1.set_xlim((0,maxL))

#ax2 = fig.add_subplot(1,2,2)

#lc2 = LineCollection(lines2)
#lc2.set_array(ps)
#lc2.set_cmap(cmap)

#ax2.add_collection(lc2)

#ax2.set_yscale('log', basey=2)

#ax3 = fig.add_subplot(1,15,15)

#ax2.set_xlabel(r"$L$ [symbols]")
#ax2.set_ylabel(r"$h_{\mu}(L)$ [bits/symbol]")
#ax2.axis('auto')
#ax2.set_xlim((0,maxL))

#cbar = fig.colorbar(lc1, ax3)
#cbar.ax.set_ylabel("probability $p$")
#cbar.ax.set_position([0.88,0.1, 0.025, 0.8])

plt.savefig("H_random_order3.pdf")
#plt.show()


