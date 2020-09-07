* Passive Matching Circuits
* LPA 05 Aug 2020

.options savecurrents seed=random
.include matching_subckts.sp

X1 		hir lor		l_match_lp		C=636.62f L=795.77p
Rs		hir vin		50
Rl		lor 0		25

Vs		vin 0		dc=0 ac=1

.control

ac dec 1000 100meg 100G

let zin_mag = v(hir)/(-i(vs))
let zin_imag = imag(v(hir)/(-i(vs)))
let zin_real = real(v(hir)/(-i(vs)))

let zout_mag = v(lor)/(-i(v.x1.vl1))
let zout_imag = imag(v(lor)/(-i(v.x1.vl1)))
let zout_real = real(v(lor)/(-i(v.x1.vl1)))

meas ac zin_real_f0 find zin_real at=5G
meas ac zin_imag_f0 find zin_imag at=5G

meas ac zout_real_f0 find zout_real at=5G
meas ac zout_imag_f0 find zout_imag at=5G

wrdata l_match_lp_a1.2.1.dat v(hir) (-i(vs)) v(lor) (-i(v.x1.vl1))

.endc

.end
