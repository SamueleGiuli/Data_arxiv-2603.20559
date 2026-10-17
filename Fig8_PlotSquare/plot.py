import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import h5py

U_kunes, T_kunes = np.loadtxt('Kunes.data',unpack=True,skiprows=1,delimiter=',')
U_schafer, T_schafer = np.loadtxt('Schafer.data',unpack=True,skiprows=1,delimiter=',')

with h5py.File('Data.h5','r') as F:
    U_list = F['U_list'][()]
    T_list = F['T_list'][()]
    M_list = F['M_list'][()]



plt.figure(figsize=(4, 3),dpi=200)

plt.pcolormesh(
    U_list,
    T_list,
    M_list,
    cmap=cm.viridis,
    shading='nearest',
    vmin=0.0,vmax=1
)

plt.xlabel("$U/D$")
plt.ylabel("$T/D$")

plt.colorbar(label=r"$ m_z $")

plt.plot(U_kunes,T_kunes,linestyle='--',color='magenta',marker='o',markersize=4, markerfacecolor='none',label='Ref. [114]')
plt.plot(U_schafer,T_schafer,linestyle=':',color='white',marker='s',markersize=4, markerfacecolor='none',label='Ref. [115]')
plt.legend(framealpha=0.65)
plt.tight_layout()
plt.savefig('Figure8.png',bbox_inches="tight")
plt.show()