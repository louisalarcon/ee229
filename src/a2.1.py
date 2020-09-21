#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 10:09:13 2020

@author: louis
"""

import numpy as np
import math
import matplotlib.pyplot as plt 
from si_prefix import si_format
from scipy import signal

def poly_eval(coeffs, x):
    y = 0
    for i, a in enumerate(coeffs):
        y = y + (a * (x**i) )
        
    return y
        
def pretty_plot(xl, yl, title):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1) 
    ax.set_xlabel(xl)
    ax.set_ylabel(yl)
    ax.set_title(title)
    ax.grid(True)
    
    return ax

def amp_nonlinear(sig_in, a):
    sig_out = [poly_eval(a, si) for si in sig_in]
    
    ax = pretty_plot('Input', 'Output', 'Amplifier Transfer Function')
    ax.plot(sig_in, sig_out, '.')
    plt.tight_layout()
    
    return sig_out
    
def to_VdB(sig_in):
    sig_out = [20 * np.log10(si) for si in sig_in ] 
    
    return sig_out

def simple_fft(sig, N, fs, tones):
    # scale to the fundamental
    sig_freq = np.fft.rfft(sig)/(float(N/2)*(max(sig)/tones))
    mag_sig = np.abs(sig_freq)
    f = np.fft.rfftfreq(N, d=1./fs)
    
    return f, mag_sig

def add_signals(s1, s2):
    s3 = [a + b for a, b in zip(s1, s2)]
    return s3

def mult_signals(s1, s2):
    s3 = [a * b for a, b in zip(s1, s2)]
    return s3

def create_sinusoid(a, f, phi, time):
    s = [a * np.sin(2 * np.pi * f * t + phi) for t in time]
    return s
    
        
gain = 10
x = np.arange(-1, 1, 0.01)
a1 = [0, gain, 0, -3]
y1 = poly_eval(a1, x)

a2 = [0, gain, 0, 3]
y2 = poly_eval(a2, x)

# plot time domain
title = r'$y=\alpha_0 + \alpha_1 x + \alpha_2 x^2 + \alpha_3 x^3$'
ax = pretty_plot(r'$x$', r'$y$', title)
    
nl_label1 = ''    
for i, ai in enumerate(a1):
    nl_label1 = nl_label1 + r'$\alpha_{}=$'.format(i) + r'{:.2f}, '.format(ai)

nl_label2 = ''    
for i, ai in enumerate(a2):
    nl_label2 = nl_label2 + r'$\alpha_{}=$'.format(i) + r'{:.2f}, '.format(ai)
    
ax.plot(x, y1, '-', label = nl_label1)
ax.plot(x, y2, '--', label = nl_label2)
ax.plot(x, gain*x, ':', label = 'linear' )
ax.legend()

plt.tight_layout()
plt.savefig('odd_functions.png', dpi=600)


gain = 10
x = np.arange(-1, 1, 0.01)
a1 = [0, gain, 3, 0]
y1 = poly_eval(a1, x)

a2 = [0, gain, -3, 0]
y2 = poly_eval(a2, x)

# plot time domain
title = r'$y=\alpha_0 + \alpha_1 x + \alpha_2 x^2 + \alpha_3 x^3$'
ax = pretty_plot(r'$x$', r'$y$', title)
    
nl_label1 = ''    
for i, ai in enumerate(a1):
    nl_label1 = nl_label1 + r'$\alpha_{}=$'.format(i) + r'{:.2f}, '.format(ai)

nl_label2 = ''    
for i, ai in enumerate(a2):
    nl_label2 = nl_label2 + r'$\alpha_{}=$'.format(i) + r'{:.2f}, '.format(ai)
    
ax.plot(x, y1, '-', label = nl_label1)
ax.plot(x, y2, '--', label = nl_label2)
ax.plot(x, gain*x, ':', label = 'linear' )
ax.legend()

plt.tight_layout()
plt.savefig('even_functions.png', dpi=600)

# define sampling and FFT parameters
fs = 40e6
periods = 673
N = 2**10
Ts = 1/fs
k1 = 100
k2 = 40
# input signals
f1 = fs * k1 / N
A1 = 1
BW = 2e6

# first tone
time = [i * Ts for i in range(N)]

x1 = create_sinusoid(A1, f1, 0, time)


# pass input through a nonlinear amplifier
a = [0, 10, 0.5, -3]
b = [0, 2, 0, 0]

y1 = amp_nonlinear(x1, a)
fs_str = si_format(fs, precision=2) + 'Hz'

# spectrum of input tone
fx1, mag_x1 = simple_fft(x1, N, fs, 1)
title = r'Input: $f_s$ = ' + fs_str + ', N = {}'.format(N)
ax = pretty_plot('Frequency [MHz]', 'Magnitude [dB]', title)
ax.plot(fx1[1:]/1e6, to_VdB(mag_x1[1:]))
plt.tight_layout()
plt.savefig('single_tone.png', dpi=600)


# spectrum of output
fy1, mag_y1 = simple_fft(y1, N, fs, 1)
hd2 = to_VdB([mag_y1[2*k1]])
hd3 = to_VdB([mag_y1[3*k1]])
title = r'$f_s$ = ' + fs_str + ', N = {}, '.format(N) +\
    r'$HD_2$ = {:.2f} dB, $HD_3$ = {:.2f} dB'.format(hd2[0], hd3[0]) 
ax = pretty_plot('Frequency [MHz]', 'Magnitude [dB]', title)
ax.plot(fy1[1:]/1e6, to_VdB(mag_y1[1:]))
plt.tight_layout()
plt.savefig('harmonic_disto.png', dpi=600)

# check the results with our hand calculation
Av = a[1] + (3*a[3]/4)
HD2 = 20*np.log10(abs((a[2]/2)/Av))
HD3 = 20*np.log10(abs((a[3]/4)/Av))
