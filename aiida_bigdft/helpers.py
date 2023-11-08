""" Helper functions for automatically setting up computer & code.
Helper functions for setting up

 1. An AiiDA localhost computer
 2. A "bigdft" code on localhost

Note: Point 2 is made possible by the fact that the ``diff`` executable is
available in the PATH on almost any UNIX system.
"""
import os
import shutil
import tempfile

from aiida import __version__
from aiida.common.exceptions import NotExistent
from aiida.orm import Code, Computer

import bigdft

LOCALHOST_NAME = "localhost"

executables = {
    "bigdft": "bigdft",
}


def get_path_to_executable(executable):
    """Get path to local executable.
    :param executable: Name of executable in the $PATH variable
    :type executable: str
    :return: path to executable
    :rtype: str
    """
    path = shutil.which(executable)
    if path is None:
        raise ValueError(f"'{executable}' executable not found in PATH.")
    return path


def get_computer(name=LOCALHOST_NAME, workdir=None):
    """Get AiiDA computer.
    Loads computer 'name' from the database, if exists.
    Sets up local computer 'name', if it isn't found in the DB.

    :param name: Name of computer to load or set up.
    :param workdir: path to work directory
        Used only when creating a new computer.
    :return: The computer node
    :rtype: :py:class:`aiida.orm.computers.Computer`
    """

    try:
        computer = Computer.objects.get(label=name)
    except NotExistent:
        if workdir is None:
            workdir = tempfile.mkdtemp()

        transport = "local"
        scheduler = "direct"
        if int(__version__.split(".", maxsplit=1)[0]) >= 2:
            transport = f"core.{transport}"
            scheduler = f"core.{scheduler}"

        computer = Computer(
            label=name,
            description=f"computer set up by tests, transport {transport}, scheduler {scheduler}",
            hostname=name,
            workdir=workdir,
            transport_type=transport,
            scheduler_type=scheduler,
        )
        computer.store()
        computer.set_minimum_job_poll_interval(0.0)
        computer.configure()

    return computer


def get_code(entry_point, computer):
    """Get local code.
    Sets up code for given entry point on given computer.

    :param entry_point: Entry point of calculation plugin
    :param computer: (local) AiiDA computer
    :return: The code node
    :rtype: :py:class:`aiida.orm.nodes.data.code.installed.InstalledCode`
    """

    try:
        executable = executables[entry_point]
    except KeyError as exc:
        raise KeyError(
            f"Entry point '{entry_point}' not recognized. Allowed values: {list(executables.keys())}"
        ) from exc

    codes = Code.objects.find(  # pylint: disable=no-member
        filters={"label": executable}
    )
    if codes:
        return codes[0]

    # bigdft source
    path, file = os.path.split(get_path_to_executable(executable))
    sourcefile = os.path.join(path, "bigdftvars.sh")

    # bigdft.py location
    bigdft_script_path = os.path.join(os.path.split(bigdft.__file__)[0], "bigdft.py")

    code = Code(
        input_plugin_name=entry_point,
        remote_computer_exec=[computer, bigdft_script_path],
    )
    code.label = executable

    code.prepend_text = f"source {sourcefile}"

    return code.store()
