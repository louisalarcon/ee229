* MOSFET noise
* LPA 10/4/2019

******************************
* Include model files
******************************
.include ./45nm_NMOS_bulk69327.pm

******************************
* Additional options
******************************
.option TEMP=27C 
.option abstol=1e-24 reltol=1e-24 vntol=1e-24
.option savecurrents

******************************
* Circuit netlist
******************************

.param w_value = 100u
.param l_value = 90n
.param vdd_supply = 1

vsup1			vdd1 0			dc vdd_supply ac 0
vsup2			vdd2 0			dc vdd_supply ac 0

r2				vdd2 d2 		2k noisy=0
r1				vdd1 d1 		2k noisy=0

m1				d1 g1 0 0 		nmos	W=w_value L=l_value
m2				d2 d2 0 0	 	nmos	W=w_value L=l_value

cinf			d2 0			1
vin				g1 d2			dc=0 ac=1

cload			d1 0			100f
hout			out 0 vsup1 	1.0

******************************
* Control section
******************************

.control 
set sqrnoise
* setplot noise2
op
print @m1[gm] 1/@m1[gds] @m1[id] @m1[vgs] @m1[vds] @m2[id]

noise v(out) vin dec 1000 1 10G
* print onoise_total
setplot noise1
* plot onoise_spectrum
wrdata MOS_noise_1.dat onoise_spectrum

alterparam w_value = 200u
alterparam l_value = 180n
reset

op
print @m1[gm] 1/@m1[gds] @m1[id] @m1[vgs] @m1[vds] @m2[id]

noise v(out) vin dec 1000 1 10G
* print onoise_total
setplot noise3
* plot onoise_spectrum
wrdata MOS_noise_2.dat onoise_spectrum

alterparam w_value = 100u
alterparam l_value = 180n
reset

op
print @m1[gm] 1/@m1[gds] @m1[id] @m1[vgs] @m1[vds] @m2[id]

noise v(out) vin dec 1000 1 10G
* print onoise_total
setplot noise5
* plot onoise_spectrum
wrdata MOS_noise_3.dat onoise_spectrum

.endc


******************************
* End of file
******************************
.end
