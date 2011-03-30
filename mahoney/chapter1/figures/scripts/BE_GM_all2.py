"""
Try to use AxesGrid to do something nice
might not be working...
"""

import cmpy
import numpy as np
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid import AxesGrid


"""
    grid = AxesGrid(fig, 132, # similar to subplot(132)
                    nrows_ncols = (2, 2),
                    axes_pad = 0.0,
                    share_all=True,
                    label_mode = "L",
                    cbar_location = "top",
                    cbar_mode="single",
                    )

    Z, extent = get_demo_image()
    for i in range(4):
        im = grid[i].imshow(Z, extent=extent, interpolation="nearest")
    #plt.colorbar(im, cax = grid.cbar_axes[0])
    grid.cbar_axes[0].colorbar(im)

    for cax in grid.cbar_axes:
        cax.toggle_label(False)
        
    # This affects all axes as share_all = True.
    grid.axes_llc.set_xticks([-2, 0, 2])
    grid.axes_llc.set_yticks([-2, 0, 2])
"""

fig = plt.figure()
#fig.set_figheight(5)
#fig.set_figwidth(10)
#fig.subplots_adjust(right = 0.95)

grid = AxesGrid(fig, 111, # similar to subplot(132)
				nrows_ncols = (1, 2),
				aspect=True,
				axes_pad = 1,
				share_all=False,
				label_mode = "all",
				cbar_location = "right",
				cbar_mode="single",
				cbar_pad="2%"
				)

maxL=5

Np = 5
ps = np.linspace(0.01, 0.99, Np)

lines1 = []
lines2 = []

for p in ps:
	gm = cmpy.machines.GoldenMean(bias = p)
	data = gm.cmech_quantities(['HX0L', 'hmu'], maxL)
	lines1.append(zip(range(maxL+1),data[0]))
	data[1].mask[0] = False
	lines2.append(zip(range(maxL+1),data[1,:]))

lc1 = LineCollection(lines1)
lc1.set_array(ps)
lc1.set_cmap(plt.cm.jet)
lc1.set_linewidth(2)

grid[0].add_collection(lc1)

grid[0].set_xlabel("Length []")
grid[0].set_ylabel("Entropy [bits]")
grid[0].axis('auto')

lc2 = LineCollection(lines2)
lc2.set_array(ps)
lc2.set_cmap(plt.cm.jet)
lc2.set_linewidth(2)

grid[1].add_collection(lc2)

grid[1].set_xlabel("Length []")
grid[1].set_ylabel("Entropy rate [bits/symbol]")
grid[1].axis('auto')

grid.cbar_axes[1].colorbar(lc2)

for cax in grid.cbar_axes:
	cax.toggle_label(False)

"""
ax1 = fig.add_subplot(1,2,1)

lc1 = LineCollection(lines1)
lc1.set_array(ps)
lc1.set_cmap(plt.cm.jet)
lc1.set_linewidth(2)

ax1.add_collection(lc1)

ax1.set_xlabel("Length []")
ax1.set_ylabel("Entropy [bits]")
ax1.axis('auto')

ax2 = fig.add_subplot(1,2,2)

lc2 = LineCollection(lines2)
lc2.set_array(ps)
lc2.set_cmap(plt.cm.jet)
lc2.set_linewidth(2)

ax2.add_collection(lc2)

cbar = fig.colorbar(lc2)
cbar.ax.set_ylabel("probability p")

ax2.set_xlabel("Length []")
ax2.set_ylabel("Entropy rate [bits/symbol]")
ax2.axis('auto')
"""

#plt.savefig("BE_GM_all.pdf")
plt.show()
