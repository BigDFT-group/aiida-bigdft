#!/usr/bin/python3
import os.path

import ase.io
import click

import yaml

from BigDFT.Inputfiles import Inputfile
from BigDFT.Logfiles import Logfile
from BigDFT.Calculators import SystemCalculator
from BigDFT.Interop.ASEInterop import ase_to_bigdft
from BigDFT.Systems import System


@click.command()
@click.option('--structure', help='path to structure json file')
@click.option('--parameters', help='yaml dumped dft parameters')
@click.option('--submission', help='extra submission parameters')
def run(structure: str = None,
        parameters: str = None,
        submission: str = None) -> Logfile:
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
        with open(submission, 'r') as o:
            params_sub = yaml.safe_load(o)

    mpirun_cmd = params_sub["mpirun"]

    ########################
    ####    structure    ###
    ########################
    if structure is None:
        structure = 'structure.json'
    structure = os.path.abspath(structure)
    struct_ase = ase.io.read(structure)

    # structure proper
    frag = ase_to_bigdft(struct_ase)

    sys = System()
    sys['FRA:1'] = frag

    ########################
    ####   calc params   ###
    ########################
    if parameters is None:
        parameters = 'input.yaml'
    with open(parameters, 'r') as o:
        parameters = yaml.safe_load(o)
    inp = Inputfile(parameters)

    ########################
    ###    calculation   ###
    ########################
    code = SystemCalculator(mpi_run=mpirun_cmd)
    log = code.run(input=inp,
                   sys=sys,
                   name=params_sub["jobname"])

    return log


if __name__ == '__main__':
    run()
