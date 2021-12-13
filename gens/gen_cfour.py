#!/usr/bin/python3.4
import io, os, sys, stat

atoms = ["H", "N", "C", "O"]
name = "hnco_app"
molname = "HNCO"
basis ="AUG-PVTZ"
method = "CCSD(T)(a)"
theory = "tz"
memory = 16
nproc = 4
#read in all of the geometries from file07
with open('file07') as f:
        stuff = f.read()
#split the geoms up into separateness
geoms = stuff.split("# GEOMUP #################\n")[1:]
#make a directory
os.mkdir('{theory}'.format(theory = theory))
count = 0
with open('{theory}/submit'.format(theory = theory), 'w') as script:
        #add atom labels to the geoms
        for geom in geoms:
                count += 1
                os.mkdir('{theory}/{count:04}'.format(theory = theory, count = count))
                buf = io.StringIO()
                for i,line in enumerate(geom.rstrip().split("\n")):
                        buf.write("{atoms}{line}\n".format(atoms = atoms[i], line = line))
        #put the read in geoms into the {xyz} temp
                xyz = buf.getvalue()
        #write the stuff to a file in the directory
                with open('{theory}/{count:04}/ZMAT'.format(theory = theory, count = count), 'w') as pts:
                        pts.write("""{name} {method} {basis}
{xyz}

*CFOUR(CALC={method},BASIS={basis},COORDINATES=CARTESIAN,UNITS=BOHR
CC_CONV=10
LINEQ_CONV=12
SCF_CONV=10
FROZEN_CORE=ON
EXCITE=EOMEE
ESTATE_SYM=0/1
EOM_NONIT=STAR
CC_PROG=ECC          
MEM_UNIT=GB,MEMORY_SIZE={mem})""".format(name = name, method = method, basis = basis, xyz = xyz, mem = int(memory/nproc)))
        #copy in the pbs script
                with open('{theory}/{count:04}/ZMAT.pbs'.format(theory = theory, count = count), "w") as pbs:
                        pbs.write("""#!/bin/csh
#
#PBS -N {name}_{count:04}
#PBS -S /bin/csh
#PBS -j oe
#PBS -o cfour.out
#PBS -W umask=022
#PBS -l cput=2400:00:00
#PBS -l mem={memory}gb
#PBS -l nodes=1:ppn={nproc}

cd $PBS_O_WORKDIR
setenv NUM $NCPUS
echo "$NUM cores requested in PBS file"
echo

/home/ums/r0683/QC/bin/cfour_v2.1_seq.sh $NUM""".format(name = name, count = count, memory = memory, nproc = nproc))
        #make a submit script that submits each pbs script in its directory
                script.write("""(cd {count:04}/ && qsub ZMAT.pbs)\n""".format(count = count))

os.chmod('{theory}/submit'.format(theory = theory), stat.S_IRWXU)
