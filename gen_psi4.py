#!/usr/bin/env python3.7
import io, os, sys, stat

atoms = ["H", "O", "S", "H"]
#read in all of the geometries from file07
with open('../file07') as f:
        stuff = f.read()
#split the geoms up into separateness
geoms = stuff.split("# GEOMUP #################\n")[1:]
#make a directory
os.mkdir('inp')
count = 0
with open('inp/submit', 'w') as script:
        #add atom labels to the geoms
        for geom in geoms:
                count += 1
                os.mkdir(f'inp/{count:04}')
                buf = io.StringIO()
                for i,line in enumerate(geom.rstrip().split("\n")):
                        buf.write(f"{atoms[i]}{line}\n")
        #put the read in geoms into the {xyz} temp
                xyz = buf.getvalue()
        #write the stuff to a file in the directory
                with open(f'inp/{count:04}/ZMAT', 'w') as pts:
                        pts.write(f"""HOSH CCSDT/atz single-point energy
{xyz}

*CFOUR(CALC=CCSDT,BASIS=AUG-PVTZ,COORDINATES=CARTESIAN,UNITS=BOHR
MEM_UNIT=GB,MEMORY_SIZE=8)""")
        #copy in the pbs script
                with open(f'inp/{count:04}/ZMAT.pbs', "w") as pbs:
                        pbs.write(f"""#!/bin/csh
#
#PBS -N ZMAT_{count:04}
#PBS -S /bin/csh
#PBS -j oe
#PBS -o cfour.out
#PBS -W umask=022
#PBS -l cput=2400:00:00
#PBS -l mem=32gb
#PBS -l nodes=1:ppn=4

cd $PBS_O_WORKDIR
setenv NUM $NCPUS
echo "$NUM cores requested in PBS file"
echo

/ddn/home1/r1621/maple/bin/tempQC/bin/c4ext_old.sh 4""")
        #make a submit script that submits each pbs script in its directory
                script.write(f"""(cd {count:04}/ && qsub ZMAT.pbs\n)""")

os.chmod('inp/submit', stat.S_IRWXU)
