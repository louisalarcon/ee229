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
        'cir_file' : 'RC_noise.sp',
        }

# constants
Tc = 27                 # Celsius
Tk = Tc + 273.15        # Kelvin
k = 1.38064852e-23      # J/K

# create the ngspice object
sim1 = ngl.ngspice(cfg)

# run ngspice with the configuration above
sim1.run_ngspice()

dfile = 'RC_noise_1.dat'
f, [vno2_1] = sim1.read_dc_analysis(dfile, [1])    
vot1 = np.trapz(vno2_1, f)

dfile = 'RC_noise_2.dat'
f, [vno2_2] = sim1.read_dc_analysis(dfile, [1])    
vot2 = np.trapz(vno2_2, f)

plt_cfg = {
        'grid_linestyle' : 'dotted',
        'title' : r'RC Noise Power Spectral Density',
        'xlabel' : r'Frequency [Hz]',
        'ylabel' : r'$\frac{\overline{v_o^2}}{\Delta f}$ [$\frac{V^2}{Hz}$]',
        'legend_loc' : 'lower left',
        'add_legend' : True,
        'legend_title' : r'C=1$\mu$F'
        }

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.loglog(f, vno2_1, '-', label=r'R=1k$\Omega$')
ax.loglog(f, vno2_2, '-', label=r'R=10k$\Omega$')
ax.set_ylim([1e-26,1e-14])
ngl.add_hline_text(ax, vno2_1[0], 1e-2, '{:.2e}'.format(vno2_1[0]))
ngl.add_hline_text(ax, vno2_2[0], 1e-2, '{:.2e}'.format(vno2_2[0]))
plt.text(1e-2, 1e-19, 'Area1={:.2e}'.format(vot1))
plt.text(1e-2, 2e-20, 'Area2={:.2e}'.format(vot2))

ngl.label_plot(plt_cfg, fig, ax)
plt.savefig('RC_noise_spectrum.png', dpi=600)

plt_cfg = {
        'grid_linestyle' : 'dotted',
        'title' : r'RC Noise Root Power Spectral Density',
        'xlabel' : r'Frequency [Hz]',
        'ylabel' : r'$\sqrt{\frac{\overline{v_o^2}}{\Delta f}}$ [$\frac{V}{\sqrt{Hz}}$]',
        'legend_loc' : 'lower left',
        'add_legend' : True,
        'legend_title' : r'C=1$\mu$F'
        }

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.loglog(f, np.sqrt(vno2_1), '-', label=r'R=1k$\Omega$')
ax.loglog(f, np.sqrt(vno2_2), '-', label=r'R=10k$\Omega$')
ax.set_ylim([1e-13,1e-7])

ngl.add_hline_text(ax, np.sqrt(vno2_1[0]), 1e-2, '{:.2e}'.format(np.sqrt(vno2_1[0])))
ngl.add_hline_text(ax, np.sqrt(vno2_2[0]), 1e-2, '{:.2e}'.format(np.sqrt(vno2_2[0])))

ngl.label_plot(plt_cfg, fig, ax)
plt.savefig('RC_noise_root_spectrum.png', dpi=600)


