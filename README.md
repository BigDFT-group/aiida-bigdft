# aiida-bigdft

Translation layer for AiiDA-PyBigDFT

## Installation

```shell
pip install aiida-bigdft
verdi quicksetup  # better to set up a new profile
verdi plugin list aiida.calculations  # should now show your calclulation plugins
```

You must ensure that your bigdft install has a copy of the `bigdft.py` in the build dir.

This can be found in this repository at `bigdft/bigdft.py`


## Usage

Here goes a complete example of how to submit a test calculation using this plugin.

A quick demo of how to submit a calculation:
```shell
verdi daemon start     # make sure the daemon is running
cd examples
./example_01.py        # run test calculation
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
