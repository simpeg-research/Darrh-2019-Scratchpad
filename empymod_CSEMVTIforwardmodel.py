#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSEM forward modeling code

empymod
"""
import numpy as np
# Load the bipole-modeling routine from empymod
from empymod import bipole
# Load plotting library

import matplotlib.pyplot as plt
# Define times
t6 =  np.linspace(0, 1, 1000)
t6[0] = 0.0005  # Set a small starting time, slightly bigger than 0
# Collect input parameters
bg_res_h=[2e14, 100, 5, 100]  #horizontal resistivity
bg_res_v=[2e14, 100, 20, 100] #vertical resistivity
aniso_lay=[np.sqrt(bg_res_v[ii]/bg_res_h[ii]) for ii in range(0,len(bg_res_h))] #Calculate aniso

bg_dep=[0,100,500] #Depth of interfaces btwn layers

inp6 = {'src': [0, 0, 0.01, 400, 0], #source at origin, .01 m z
        'rec': [1000, 0, 0.01, 0, 0], #source at x=1000, .01m z
        'depth': bg_dep,
        'freqtime': t6, 
        'signal': -1, #Switch off
        'verb': 0} #How much info output
#sig_horiz 3,4x higher than sig v for shale.
#rho_ver, 3,4x higher than rho_horiz


#Their anisotropy is sqrt(rhov/rhoh) so aniso of roughly 2 


# Isotropic case
res_isotr = bipole(res=bg_res_h, aniso=[1, 1, 1, 1], **inp6)

# Keep horizontal resistivity constant
res_hor_2 = bipole(res=bg_res_h, aniso=aniso_lay, **inp6)



plt.figure(figsize=(9.8, 4), num='1. Anisotropy')

plt.title('Effect of anisotropy; offset = 2 km', fontsize=20)

# 1. Constant rho_h
plt.semilogy(t6, res_isotr, 'k',label='Isotropic')
plt.semilogy(t6, res_hor_2, 'C0',label='Anisotropic')
plt.xlabel('Time (s)')
plt.ylabel('E (V/m)')
plt.legend()


fig = plt.figure(figsize=(9.8, 6), num='2. Variation of rho at depth')
plt.subplots_adjust(left=0.07, right=.93, bottom=0.1, top=.92, wspace=.05)

# 1. Plot resistivity model; initialize target with background
ax1 = plt.subplot2grid((2, 3), (0, 0), rowspan=2)
ax1.set_title('Resistivity model')

depth=np.linspace(0,4000,1000)
bgres_h=np.zeros(len(depth))
bgres_v=np.zeros(len(depth))
bgres_h[depth<bg_dep[0]]=bg_res_h[0]
bgres_v[depth<bg_dep[0]]=bg_res_v[0]
nn=0

for dep in bg_dep: 
    bgres_h[depth>=bg_dep[nn]]=bg_res_h[nn+1]
    bgres_v[depth>=bg_dep[nn]]=bg_res_v[nn+1]
    
    nn=nn+1


bgdep = np.r_[bg_dep, bg_dep[-1], 4000]/1000
ax1.semilogx(bgres_h, depth, 'k', label=r'$\rho_{h}$')
ax1.semilogx(bgres_v, depth, 'r--', label=r'$\rho_{v}$')
ax1.legend()
ax1.set_ylabel('Depth (m)')
ax1.set_xlabel(r'Resistivity ($\Omega\,$m)')

plt.gca().invert_yaxis()
# Display

plt.show()