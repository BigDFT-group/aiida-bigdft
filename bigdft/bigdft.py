import os.path

import ase.io
import click

import yaml

from BigDFT.Inputfiles import Inputfile
from BigDFT.Logfiles import Logfile
from BigDFT.Calculators import SystemCalculator
from BigDFT.Interop.ASEInterop import ase_to_bigdft
from BigDFT.Systems import System

from aiida_bigdft.debug import debug


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
    params_sub = {}
    if submission is not None:
        with open(submission, 'r') as o:
            params_sub = yaml.safe_load(o)

    debug(f'loaded submission parameters file {params_sub}')

    # structure input
    if structure is None:
        debug('structure is None, defaulting')
        structure = 'structure.json'
    structure = os.path.abspath(structure)

    debug(f'reading structure at {structure}')
    struct_ase = ase.io.read(structure)

    debug('structure read')

    # bigdft parameters input
    if parameters is None:
        debug('parameters is None, defaulting')
        parameters = 'input.yaml'
    debug(f'reading parameters at {parameters}')
    with open(parameters, 'r') as o:
        parameters = yaml.safe_load(o)
    inp = Inputfile(parameters)

    debug('parameters read')
    debug(str(inp))

    # calculation proper
    frag = ase_to_bigdft(struct_ase)
    debug(f'fragment generated: {frag}')

    sys = System()
    sys['FRA:1'] = frag

    code = SystemCalculator()
    log = code.run(input=inp, sys=sys, name=params_sub["jobname"])

    return log


if __name__ == '__main__':
    run()
