* Noise simulations
* LPA 05 Aug 2020

.option seed=random
.option TEMP=27C 
.option abstol=1e-12 reltol=1e-12 vntol=1e-12
.option savecurrents

* A simple RC circuit

R1		in out		1k
C1		out 0		1u

Vs 		in 0		dc=0 ac=1

.control
set sqrnoise
noise v(out) Vs dec 1000 1m 1Meg
print onoise_total

setplot noise1
wrdata RC_noise_1.dat onoise_spectrum

alter R1 10k
noise v(out) Vs dec 1000 1m 1Meg
print onoise_total

setplot noise3
wrdata RC_noise_2.dat onoise_spectrum

.endc

.end
