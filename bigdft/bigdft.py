import os.path

import ase.io
import click
import sys

import yaml
import getpass

from BigDFT.Inputfiles import Inputfile
from BigDFT.Logfiles import Logfile
from BigDFT.Calculators import SystemCalculator
from BigDFT.Interop.ASEInterop import ase_to_bigdft
from BigDFT.Systems import System

from datetime import datetime


class MiniLogger:
    """
    Lightweight miniature logger for quick daemon side debugging
    """

    def __init__(self, path):
        self._path = path
        self.debug('minilogger class init', wipe=True)

    def debug(self, msg: str, wipe=False) -> None:
        """
        add a message to the log

        args:
            msg (str):
                message to write
            wipe (bool):
                wipe the log and make msg the first message

        returns:
            None
        """
        mode = 'w+' if wipe else 'a'
        timestr = datetime.now().strftime('%H:%M:%S')
        with open(self._path, mode) as o:
            o.write(f'[{timestr}] {msg}\n')


@click.command()
@click.option('--structure', help='path to structure json file')
@click.option('--parameters', help='yaml dumped dft parameters')
@click.option('--submission', help='extra submission parameters')
def run(structure=None,
        parameters=None,
        submission=None):
    params_sub = {}
    if submission is not None:
        with open(submission, 'r') as o:
            params_sub = yaml.safe_load(o)

    logger.debug(f'loaded submission paramters file {params_sub}')

    # structure input
    if structure is None:
        logger.debug('structure is None, defaulting')
        structure = 'structure.json'
    structure = os.path.abspath(structure)

    logger.debug(f'reading structure at {structure}')
    struct_ase = ase.io.read(structure)

    logger.debug('structure read')

    # bigdft parameters input
    if parameters is None:
        logger.debug('parameters is None, defaulting')
        parameters = 'input.yaml'
    logger.debug(f'reading parameters at {parameters}')
    with open(parameters, 'r') as o:
        parameters = yaml.safe_load(o)
    inp = Inputfile(parameters)

    logger.debug('parameters read')
    logger.debug(str(inp))

    # calculation proper
    if user == 'test':
        return Logfile()
    frag = ase_to_bigdft(struct_ase)
    logger.debug(f'fragment generated: {frag}')

    sys = System()
    sys['FRA:1'] = frag

    code = SystemCalculator()
    log = code.run(input=inp, sys=sys, name=params_sub["jobname"])

    return log


if __name__ == '__main__':
    user = getpass.getuser()
    path = os.path.join(os.getcwd(), 'pybigdft.log')
    logger = MiniLogger(path)
    logger.debug(f'script called with args {sys.argv}')

    run()
