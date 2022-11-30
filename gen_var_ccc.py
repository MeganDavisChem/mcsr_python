#!/home/mdavis/anaconda3/bin/python
import io, os, sys, stat

# This is all agnostic to the program
# I may put all controls I need up here
# change these
atoms = ["C", "O"]
name = "CO"
molname = "CO"
charge = 1
multiplicity = 2

# don't touch
basis = "AUG-PCVTZ"
theory = "pcvtz"

# or tqcc
# base_method = "CCSDT-3"
# level = "ccc"
base_method = sys.argv[1]
level = sys.argv[2]
state = sys.argv[3]


if level == "ccc":
    theories = {
        "tz": "AUG-PVTZ",
        "qz": "AUG-PVQZ",
        "5z": "AUG-PV5Z",
        "pcvtz": "AUG-PCVTZ",
        "pcvtz_nc": "AUG-PCVTZ",
    }
elif level == "tqcc":
    theories = {
        "tz": "AUG-PVTZ",
        "qz": "AUG-PVQZ",
        "pcvtz": "AUG-PCVTZ",
        "pcvtz_nc": "AUG-PCVTZ",
    }
elif level == "ccc+dt":
    theories = {
        "tz": "AUG-PVTZ",
        "ccsdt": "AUG-PVTZ",
        "qz": "AUG-PVQZ",
        "5z": "AUG-PV5Z",
        "pcvtz": "AUG-PCVTZ",
        "pcvtz_nc": "AUG-PCVTZ",
    }
elif level == "tz":
    theories = {
        "tz": "AUG-PVTZ",
    }
core = "ON"


for theory, basis in theories.items():
    if theory == "pcvtz":
        core = "OFF"
    else:
        core = "ON"
    if theory == "ccsdt":
        method = "CCSDT"
    else:
        method = base_method
    # maybe touch
    memory = 32
    nproc = 1
    mem = int(memory / nproc)
    # read in all of the geometries from file07
    with open("file07") as f:
        stuff = f.read()
    # split the geoms up into separateness
    geoms = stuff.split("# GEOMUP #################\n")[1:]
    # make a directory
    os.mkdir(f"{theory}")
    count = 0
    with open(f"{theory}/submit", "w") as script:
        # add atom labels to the geoms
        for geom in geoms:
            count += 1
            buf = io.StringIO()
            os.mkdir(f"{theory}/{count:04}")
            for i, line in enumerate(geom.rstrip().split("\n")):
                buf.write(f"{atoms[i]}{line}\n")
                if atoms[i] == "H":
                    xh = float(line.split()[0])
                    yh = float(line.split()[1])
                    zh = float(line.split()[2])
            if state == "a1":
                roots = "ESTATE_SYM=2/0/0/0"
                #TODO double check that
                varocc = "OCCUPATION=4-1-1-0/5-1-1-0"   
            else:           
                # B1
                roots = "ESTATE_SYM=0/1/0/0"
                varocc = "OCCUPATION=5-0-1-0/5-1-1-0"   

            # put the read in geoms into the {xyz} temp
            xyz = buf.getvalue()
            # write the stuff to a file in the directory
            # this needs to be edited for each program
            with open(f"{theory}/{count:04}/ZMAT", "w") as pts:
                pts.write(
                    f"""{name} {basis} {method}
{xyz}


*CFOUR(CALC={method},BASIS={basis},COORDINATES=CARTESIAN,UNITS=BOHR
CC_CONV=10
LINEQ_CONV=12
SCF_CONV=10
ESTATE_CONV=10
CHARGE={charge}
MULTIPLICITY={multiplicity}
REFERENCE=ROHF
FROZEN_CORE={core}
{varocc}
MEM_UNIT=GB,MEMORY_SIZE={mem})"""
                )
            # copy in the pbs script
            # also needs to be edited per program
            with open(f"{theory}/{count:04}/ZMAT.sh", "w") as pbs:
                pbs.write(
                    f"""#!/bin/sh
#SBATCH --job-name={count:04}.{name}
#SBATCH --ntasks={nproc}
#SBATCH --cpus-per-task=1
#SBATCH --mem={memory}gb

/home/qc/bin/c4_new.sh {nproc}"""
                )
            # make a submit script that submits each pbs script in its directory
            script.write(f"""(cd {count:04}/ && sbatch ZMAT.sh)\n""")

    os.chmod(f"{theory}/submit", stat.S_IRWXU)
