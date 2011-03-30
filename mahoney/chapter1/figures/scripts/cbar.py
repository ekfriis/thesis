import matplotlib.pyplot as plt
import numpy as np

f = plt.figure()
a = f.add_subplot(1,1,1)

d = np.random.random(100)

d = d.reshape(10,10)
p = a.imshow(d)

cb = f.colorbar(p)
cb.ax.set_position([0.8,0.1, 0.9, 0.99])

plt.show()