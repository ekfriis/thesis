import cmpy
import matplotlib.pyplot as plt

m = cmpy.machines.BiasedCoin(bias=0.4)

N=5
bes = m.block_entropies(lengths = range(N))

plt.plot(range(N), bes)

plt.xlabel("Length []")
plt.ylabel("Entropy [bits]")

plt.savefig("BE_IID.pdf")
#plt.show()