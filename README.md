# aiida-bigdft

Translation layer for AiiDA-PyBigDFT

## Installation

```shell
pip install aiida-bigdft
verdi quicksetup  # better to set up a new profile
verdi plugin list aiida.calculations  # should now show your calclulation plugins
```

## Requirements

- A functioning BigDFT installation
- A copy of `bigdft.py` (available in this repository at `bigdft/bigdft.py`)

When setting up the BigDFT code, ensure that the executable is set to the `bigdft.py` script.

It is also important to source the `install/bin/bigdftvars.sh` script in your prepend.

```shell
# aiida code prepend

source ${BIGDFT_BUILD_DIR}/install/bin/bigdftvars.sh
```

Where BIGDFT_BUILD_DIR is the directory in which BigDFT was built.


## Usage

Here goes a complete example of how to submit a test calculation using this plugin.

A quick demo of how to submit a calculation:

```shell
verdi daemon start     # make sure the daemon is running
cd examples
verdi run examples/example_01.py        # run test calculation
verdi process list -a  # check record of calculation
```

The plugin also includes verdi commands to inspect its data types:
```shell
verdi data bigdft list
verdi data bigdft export <PK>
```

## License

MIT
## Contact

louis.j.beal@gmail.com
