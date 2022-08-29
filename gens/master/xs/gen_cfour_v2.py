#!/usr/bin/env python3.7
import io, os, sys, stat

#This is all agnostic to the program
#I may put all controls I need up here
#change these
atoms = ["H", "C", "F"]
name = "HCF"
molname = "HCF"
charge = 0
multiplicity = 1

#don't touch 
basis = "AUG-PVTZ"
method = "CCSD(T)(a)"
theory = "tz"

#maybe touch
memory = 8
nproc = 1
mem = int(memory / nproc)
#read in all of the geometries from file07
with open('file07') as f:
        stuff = f.read()
#split the geoms up into separateness
geoms = stuff.split("# GEOMUP #################\n")[1:]
#make a directory
os.mkdir(f'{theory}')
count = 0
with open(f'{theory}/submit', 'w') as script:
        #add atom labels to the geoms
        for geom in geoms:
                count += 1
                buf = io.StringIO()
                os.mkdir(f'{theory}/{count:04}')
                for i,line in enumerate(geom.rstrip().split("\n")):
                        buf.write(f"{atoms[i]}{line}\n")
                        if atoms[i] == "H":
                            xh = float(line.split()[0])
                            yh = float(line.split()[1])
                            zh = float(line.split()[2])
                if xh == 0:
                    roots = "ESTATE_SYM=0/1"
                else:
                    roots = "ESTATE_SYM=2"

        #put the read in geoms into the {xyz} temp
                xyz = buf.getvalue()
        #write the stuff to a file in the directory
        #this needs to be edited for each program
                with open(f'{theory}/{count:04}/ZMAT', 'w') as pts:
                         pts.write(f"""{name} {basis} {method}
{xyz}


*CFOUR(CALC={method},BASIS={basis},COORDINATES=CARTESIAN,UNITS=BOHR
CC_CONV=10
LINEQ_CONV=12
SCF_CONV=10
CHARGE={charge}
MULTIPLICITY={multiplicity}
FROZEN_CORE=ON
CC_PROG=ECC          
EXCITE=EOMEE
{roots}
EOM_NONIT=STAR
MEM_UNIT=GB,MEMORY_SIZE={mem})""")
        #copy in the pbs script
        #also needs to be edited per program
                with open(f'{theory}/{count:04}/ZMAT.sh', "w") as pbs:
                       pbs.write(f"""#!/bin/sh
#SBATCH --job-name={count:04}.{name}
#SBATCH --ntasks={nproc}
#SBATCH --cpus-per-task=1
#SBATCH --mem={memory}gb

/home/qc/bin/c4_new.sh {nproc}""")
        #make a submit script that submits each pbs script in its directory
                script.write(f"""(cd {count:04}/ && sbatch ZMAT.sh)\n""")

os.chmod(f'{theory}/submit', stat.S_IRWXU)
