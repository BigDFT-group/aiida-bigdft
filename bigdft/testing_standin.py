#!/usr/bin/python3
import os.path

from BigDFT.Calculators import SystemCalculator
from BigDFT.Inputfiles import Inputfile
from BigDFT.Interop.ASEInterop import ase_to_bigdft
from BigDFT.Logfiles import Logfile
from BigDFT.Systems import System
import ase.io
import click
import yaml


@click.command()
@click.option("--structure", help="path to structure json file")
@click.option("--parameters", help="yaml dumped dft parameters")
@click.option("--submission", help="extra submission parameters")
def run(
    structure: str = None, parameters: str = None, submission: str = None
) -> dict:
    """
    Run the calculation. Requires three file path inputs:

    Args:
        structure (str):
            path to the serialised ASE json file
        parameters (str):
            path to the serialised BigDFTParameters yaml file
        submission (str):
            path to the serialised submission yaml file

    Returns:
        BigDFT.Logfile
    """
    ########################
    ### submission param ###
    ########################
    params_sub = {}
    if submission is not None:
        with open(submission) as o:
            params_sub = yaml.safe_load(o)

    jobname = params_sub["jobname"]

    with open(f"log-{jobname}.yaml") as o:
        yaml.dump({}, o)

    with open(f"time-{jobname}.yaml") as o:
        yaml.dump({}, o)

    return {"result": True}


if __name__ == "__main__":
    run()
