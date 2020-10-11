#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 19:21:42 2020

@author: louis
"""

import matplotlib.pyplot as plt
import numpy as np

# import our custom ngspice module
import ngspice_link as ngl

# setup the simulation configuration
cfg = {
        'ngspice' : '/Applications/ngspice/bin/ngspice', 
        'cir_dir' : '/Users/louis/Documents/UPEEEI/Classes/EE 229/2020_1/Activities/',
        'cir_file' : 'MOS_noise.sp',
        }

# constants
Tc = 27                 # Celsius
Tk = Tc + 273.15        # Kelvin
k = 1.38064852e-23      # J/K

# create the ngspice object
sim1 = ngl.ngspice(cfg)

# run ngspice with the configuration above
sim1.run_ngspice()

dfile = 'MOS_noise_1.dat'
f, [vno2_1] = sim1.read_dc_analysis(dfile, [1])    
vot1 = np.trapz(vno2_1, f)

dfile = 'MOS_noise_2.dat'
f, [vno2_2] = sim1.read_dc_analysis(dfile, [1])    
vot2 = np.trapz(vno2_2, f)

dfile = 'MOS_noise_3.dat'
f, [vno2_3] = sim1.read_dc_analysis(dfile, [1])    
vot3 = np.trapz(vno2_3, f)

plt_cfg = {
        'grid_linestyle' : 'dotted',
        'title' : r'NMOS Noise Power Spectral Density',
        'xlabel' : r'Frequency [Hz]',
        'ylabel' : r'$\frac{\overline{v_o^2}}{\Delta f}$ [$\frac{V^2}{Hz}$]',
        'legend_loc' : 'upper right',
        'add_legend' : True,
        'legend_title' : None
        }

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.loglog(f, vno2_1, '-', label=r'W=100$\mu$m, L=90nm')
ax.loglog(f, vno2_2, '-', label=r'W=200$\mu$m, L=180nm')
ax.loglog(f, vno2_3, '-', label=r'W=100$\mu$m, L=180nm')

ngl.label_plot(plt_cfg, fig, ax)
plt.savefig('MOS_noise_spectrum.png', dpi=600)

plt_cfg = {
        'grid_linestyle' : 'dotted',
        'title' : r'NMOS Noise Root Power Spectral Density',
        'xlabel' : r'Frequency [Hz]',
        'ylabel' : r'$\sqrt{\frac{\overline{v_o^2}}{\Delta f}}$ [$\frac{V}{\sqrt{Hz}}$]',
        'legend_loc' : 'upper right',
        'add_legend' : True,
        'legend_title' : None
        }

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.loglog(f, np.sqrt(vno2_1), '-', label=r'W=100$\mu$m, L=90nm')
ax.loglog(f, np.sqrt(vno2_2), '-', label=r'W=200$\mu$m, L=180nm')
ax.loglog(f, np.sqrt(vno2_3), '-', label=r'W=100$\mu$m, L=180nm')

ngl.label_plot(plt_cfg, fig, ax)
plt.savefig('MOS_noise_root_spectrum.png', dpi=600)


