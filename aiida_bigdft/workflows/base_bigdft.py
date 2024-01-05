from aiida import orm
from aiida.engine.processes.workchains import BaseRestartWorkChain

from aiida_bigdft.calculations import BigDFTCalculation


class BigDFTBaseWorkChain(BaseRestartWorkChain):
    """Base workchain for running a BigDFT Calculation"""

    _process_class = BigDFTCalculation

    @classmethod
    def define(cls, spec):
        super().define(spec)

        spec.expose_inputs(BigDFTCalculation)

        spec.outline(cls.results)

        spec.expose_outputs(BigDFTCalculation)

        spec.output("result")

    def results(self):
        self.out("result", self.ctx.product)
