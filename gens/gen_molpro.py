#!/usr/bin/python3.4
import io, os, sys, stat

atoms = ["O", "C", "H", "H"]
name = "H2CO_b1"
molname = "H2CO"
basis ="aug-cc-pvtz"
method = "CCSD(T)"
theory = "tz"
charge = 1
spin = 1
memory = 8
nproc = 4
#read in all of the geometries from file07
with open('file07') as f:
        stuff = f.read()
#split the geoms up into separateness
geoms = stuff.split("# GEOMUP #################\n")[1:]
#make a directory
os.mkdir('{}'.format(theory))
count = 0
with open('{}/submit'.format(theory), 'w') as script:
        #add atom labels to the geoms
        for geom in geoms:
                count += 1
                buf = io.StringIO()
                for i,line in enumerate(geom.rstrip().split("\n")):
                        buf.write("{}{}\n".format(atoms[i], line))
        #put the read in geoms into the {xyz} temp
                xyz = buf.getvalue()
        #write the stuff to a file in the directory
                with open('{}/{:04}.com'.format(theory, count), 'w') as pts:
                        pts.write("""*** {name} {method} {basis}
memory, {mem}, m;
gthresh,energy=1.d-12,zero=1.d-22,oneint=1.d-22,twoint=1.d-22;
gthresh,optgrad=1.d-8,optstep=1.d-8;
nocompress;
nosym;
bohr;
geometry={{
 {xyz}
}}

set,charge={charge}
set,spin={spin}
basis={basis}
  {{hf,maxit=500;accu,20;}}
  {{uccsd(t),maxit=250;orbital,IGNORE_ERROR;}}""".format(name=name,method=method,basis=basis,mem=int((memory*1000/nproc-50)),xyz=xyz,
      charge=charge, spin=spin))




        #copy in the pbs script
                with open('{theory}/{count:04}.pbs'.format(theory = theory, count = count), "w") as pbs:
                        pbs.write("""#!/bin/sh
#PBS -N {name}
#PBS -S /bin/bash
#PBS -j oe
#PBS -W umask=022
#PBS -l walltime=600:00:00
#PBS -l ncpus={nproc}
#PBS -l mem={memory}gb

module load intel
module load mvapich2
module load pbspro
export PATH=/usr/local/apps/molpro/2015.1.35/bin:$PATH

export WORKDIR=$PBS_O_WORKDIR
export TMPDIR=/tmp/$USER/$PBS_JOBID
cd $WORKDIR
mkdir -p $TMPDIR

date
hostname
molpro -t {nproc} {count:04}.com
qstat -f $PBS_JOBID
date

rm -rf $TMPDIR""".format(name = name, count = count, memory = memory, nproc = nproc))
        #make a submit script that submits each pbs script in its directory
                script.write("""qsub {count:04}.pbs\n""".format(count = count))

os.chmod('{theory}/submit'.format(theory = theory), stat.S_IRWXU)
