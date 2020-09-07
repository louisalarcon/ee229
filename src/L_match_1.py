#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 19:52:19 2020

@author: louis
"""

import os
import matplotlib.pyplot as plt
from si_prefix import si_format
import numpy as np

# https://github.com/louisalarcon/ee229/blob/master/src/ngspice_link.py
import ngspice_link as ngl

# define the center frequency
f0 = 5e9

# setup the simulation configuration
cfg = {
        'ngspice' : '/Applications/ngspice/bin/ngspice', 
        'cir_dir' : '/Users/louis/Documents/UPEEEI/Classes/EE 229/2020_1/Activities/',
        'cir_file' : 'matching.sp',
        }

# create the ngspice object
sim1 = ngl.ngspice(cfg)

# delete old output file if it exists.
dfile = 'l_match_lp_a1.2.1.dat'
if os.path.isfile(dfile):
    os.remove(dfile)
    
# run ngspice with the configuration above
sim1.run_ngspice()

# read simulation data
index_list = [[1, 2], [4, 5], [7, 8], [10, 11]]
f, [v_in, i_in, v_out, i_out] = sim1.read_ac_analysis(dfile, index_list)  

# calculate input and load power
p_in = [ np.abs(a * b) * np.cos(np.angle(a, deg=False) - np.angle(b, deg=False)) \
        for a, b in zip(v_in, i_in) ]
    
p_out = [ np.abs(a * b) * np.cos(np.angle(a, deg=False) - np.angle(b, deg=False)) \
         for a, b in zip(v_out, i_out) ]

# calculate the impedances
z_in = [ a/b for a, b in zip(v_in, i_in)]
z_out = [ a/b for a, b in zip(v_out, i_out)]

# plot the powers
plt_cfg = {
        'grid_linestyle' : 'dotted',
        'title' : r'Passive L-Section: Power',
        'xlabel' : r'Frequency [Hz]',
        'ylabel' : r'Power [mW]',
        'legend_loc' : 'lower left',
        'add_legend' : True,
        'legend_title' : None
        }

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.semilogx(f, ngl.scale_vec(p_in, 1e-3), ':', label = r'$P_{IN}$')
ax.semilogx(f, ngl.scale_vec(p_out, 1e-3), '-', label = r'$P_{LOAD}$')

ngl.add_vline_text(ax, f0, 0, si_format(f0, precision=2) + 'Hz')

ngl.label_plot(plt_cfg, fig, ax)
plt.savefig('L_match_power.png', dpi=600)

# plot the impedances
plt_cfg = {
        'grid_linestyle' : 'dotted',
        'title' : r'Passive L-Section: Input Impedance',
        'xlabel' : r'Frequency [Hz]',
        'ylabel' : r'Impedance [$\Omega$]',
        'legend_loc' : 'lower left',
        'add_legend' : True,
        'legend_title' : None
        }

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.semilogx(f, np.imag(z_in), ':', label = r'$Imaginary$')
ax.semilogx(f, np.real(z_in), '-', label = r'Real')

ngl.add_vline_text(ax, f0, -40, si_format(f0, precision=2) + 'Hz')

idx, fx = ngl.find_in_data(f, f0)
z_in_str = si_format(np.real(z_in[idx]), precision=2) + r'$\Omega$'
ngl.add_hline_text(ax, np.real(z_in[idx]), 1e8, z_in_str)

ngl.label_plot(plt_cfg, fig, ax)
plt.savefig('L_match_Z.png', dpi=600)

