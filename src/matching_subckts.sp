* Passive Matching Circuits
* LPA 05 Aug 2020

.subckt l_match_lp hiR loR C=1p L=1n 

V1		hiR z	dc=0 ac=0
C1		z y 	{C}
VC1		y 0		dc=0 ac=0
L1		loR x	{L}
VL1		x z		dc=0 ac=0	

.ends l_match_lp


.subckt t_match_hp in out Ca = 1p Lb = 1n Cc = 1p

VC1		in y	dc=0 ac=0
C1		y x		{Ca}
L2 		x w		{Lb}
VL2		w 0		dc=0 ac=0
C3 		x z		{Cc}
VC3		out z	dc=0 ac=0

.ends t_match_hp

