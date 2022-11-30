#!/home/mdavis/anaconda3/bin/python
import io, os, sys, stat

#This is all agnostic to the program
#I may put all controls I need up here
#change these
atoms = ["C", "O"]
name = "CO"
molname = "CO"
charge = 1
multiplicity = 2

#don't touch
basis = "aug-cc-pVTZ"
method = "eom-cc3"
theory = "tz"


base_method = sys.argv[1]
level = sys.argv[2]
state = sys.argv[3]

if level == "ccc":
    theories = {
        "tz": "aug-cc-pvtz",
        "qz": "aug-cc-pvqz",
        "5z": "aug-cc-pv5z",
        "mtc": "mt",
        "mt": "mt",
    }
elif level == "tqcc":
    theories = {
        "tz": "aug-cc-pvtz",
        "qz": "aug-cc-pvqz",
        "mtc": "mt",
        "mt": "mt",
    }
elif level == "tz":
    theories = {
        "tz": "aug-cc-pvtz",
    }
core = "true"


#maybe touch
memory = 32
nproc = 4

for theory, basis in theories.items():
    if theory == "mtc":
        core = "false"
    else:
        core = "true"
    method = base_method


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
                            #THIS PART MAY NEED TO GET CHANGED
                            if atoms[i] == "H":
                                xh = float(line.split()[0])
                                yh = float(line.split()[1])
                                zh = float(line.split()[2])
                    #Cs. Change as appropriate.
                    if state == "a1":
                        roots = "roots_per_irrep = [1, 0, 0, 0]"
                    #C1
                    elif state == "b1":
                        roots = "roots_per_irrep = [0,0,1,0]"
    
                    
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
 reference rohf
 basis {basis}
 freeze_core {core}
 cachelevel=0
 maxiter=500
 dertype none
 ints_tolerance 20
 {roots}
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
