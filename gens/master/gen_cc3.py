#!/usr/bin/env python3.7
import io, os, sys, stat

#This is all agnostic to the program
#I may put all controls I need up here
#change these
atoms = ["O", "C", "H", "H"]
name = "h2co+_b1"
molname = "H2CO"
charge = 0
multiplicity = 1

#don't touch
basis = "aug-cc-pVTZ"
method = "cc3"
theory = "tz"

#maybe touch
memory = 8
nproc = 4
#read in all of the geometries from file07
with open('file07') as f:
        stuff = f.read()
#split the geoms up into separateness
geoms = stuff.split("# GEOMUP #################\n")[1:]
#make a directory
os.makedirs(f'{theory}')
count = 0
with open(f'{theory}/submit', 'w') as script:
        #add atom labels to the geoms
        for geom in geoms:
                count += 1
                buf = io.StringIO()
                for i,line in enumerate(geom.rstrip().split("\n")):
                        buf.write(f"{atoms[i]}{line}\n")
                        if atoms[i] == "O":
                            xo = float(line.split()[0])
                            yo = float(line.split()[1])
                            zo = float(line.split()[2])

        #put the read in geoms into the {xyz} temp
                xyz = buf.getvalue()
        #write the stuff to a file in the directory
        #this needs to be edited for each program
                with open(f'{theory}/{count:04}.com', 'w') as pts:
                         pts.write(f"""#{name} {basis} {method}
memory {memory*1000-50} mb

molecule {molname}{{
{charge} {multiplicity}
{xyz}
units bohr
}}
 
set globals {{
 reference rhf
 basis {basis}
 freeze_core true
 cachelevel=0
 maxiter=500
 dertype none
 ints_tolerance 20
}}

set scf d_convergence 12
set ccenergy r_convergence 12
set cceom r_convergence 8

energy('{method}')""")
        #copy in the pbs script
        #also needs to be edited per program
                with open(f'{theory}/{count:04}.sh', "w") as pbs:
                       pbs.write(f"""#!/bin/sh
#SBATCH --job-name={count:04}.{name}
#SBATCH --ntasks={nproc}
#SBATCH --cpus-per-task=1
#SBATCH --mem={memory}gb

/home/qc/bin/psi4v12.sh -n {nproc} -i {count:04}.com""")
        #make a submit script that submits each pbs script in its directory
                script.write(f"""sbatch {count:04}.sh\n""")

os.chmod(f'{theory}/submit', stat.S_IRWXU)
