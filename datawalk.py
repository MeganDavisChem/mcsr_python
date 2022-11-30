#!/home/mdavis/anaconda3/bin/python
"""Walks through a data structure, finds spectro2.out and runs rsummarize
in each dir"""
import os
from os.path import join
import random
import subprocess

# import sys


def main():
    """Locate spectro2.out files in subdirs,
    runs rsummarize on each then prints a summary of remaining work to be done
    spectro2.out files are assumed to all be located at the same level of depth
    for summary.txt to be accurate"""
    # TODO allow choosing input directory
    # TODO form composite tables? Or use my own stuff to do that idk
    completed, incompleted = check_completed()
    rsum_options = ["json", "csv", "tex"]

    for spec_dir in completed:
        rsum_outputs = run_rsummarize(spec_dir, rsum_options)
        write_rsums(spec_dir, rsum_outputs)

    write_summary()


def write_summary(directory: str = "."):
    """I should make this reusable and just operate on the filesystem...
    It's redundant computational cost but that doesn't
    matter compared to the convenience of reusing this fn
    """

    def get_motivational():
        """Print friendly message"""
        # TODO add more
        motivationals = [
            "Do your best!\n",
            "Keep going!\n",
            "Good progress!\n",
            "Get to work!\n",
            "Don't stop now!\n",
        ]
        return random.choice(motivationals)

    completed, incompleted = check_completed(directory)
    filename = join(directory, "summary.txt")
    completed_str = ""
    incompleted_str = ""
    for path in completed:
        completed_str += f"{path} completed\n"
    for path in incompleted:
        incompleted_str += f"{path} incompleted\n"
    with open(filename, "w") as file:
        file.write("--COMPLETED QFFs--\n")
        file.write(completed_str)
        file.write("--INCOMPLETED QFFs--\n")
        file.write(get_motivational())
        file.write(incompleted_str)


def write_rsums(spec_dir: str, rsum_outputs: dict):
    """Runs rustsummarize and outputs files.
    Actually I guess I should decompose this function"""
    for flag, output in rsum_outputs.items():
        filename = "spectro2." + flag
        filepath = join(spec_dir, filename)
        with open(filepath, "w") as file:
            file.write(output)


def run_rsummarize(completed_dir: str, options: list = ["json"]):
    """Runs rsummarize and gives outputs as a dict for each completed dir"""
    rsum_outputs = {}
    outfile = join(completed_dir, "spectro2.out")
    for opt in options:
        out = subprocess.run(
            ["rsummarize", f"--{opt}", outfile], capture_output=True, check=False
        ).stdout.decode()
        rsum_outputs[opt] = out

    # Do a plain run
    opt = "sum"
    out = subprocess.run(
        ["rsummarize", outfile], capture_output=True, check=False
    ).stdout.decode()
    rsum_outputs[opt] = out
    # dirs_and_outputs = zip(completed_dirs, rsums)
    return rsum_outputs
    # return dirs_and_outputs


def check_completed(target_dir: str = "."):
    """Check if spectro files are in current directory, return completed and
    incompleted as lists"""

    def get_depth(path):
        """helper function that was probably dumb"""
        depth = len(path.split("/"))
        return depth

    completed = []
    incompleted = []
    print("what")
    for root, dirs, files in os.walk(target_dir):
        if "spectro2.out" in files:
            completed.append(root)
        else:
            incompleted.append(root)
    max_depth = max([get_depth(path) for path in incompleted])
    incompleted = [path for path in incompleted if get_depth(path) == max_depth]
    return completed, incompleted


if __name__ == "__main__":
    main()  # I think this is how you do this?
