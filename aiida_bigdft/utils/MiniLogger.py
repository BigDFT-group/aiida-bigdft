import os.path
from datetime import datetime

_FILES = {
    'bigdft.py': '/home/aiida/plugin_work/pybigdft.log',
    'aiida': '/home/aiida/plugin_work/aiida.log'
}


class MiniLogger:

    def __init__(self, path):
        self._path = path
        self.debug('minilogger class init', wipe=True)

    def debug(self, msg, wipe=False):
        mode = 'w+' if wipe else 'a'
        timestr = datetime.now().strftime('%H:%M:%S')
        with open(self._path, mode) as o:
            o.write(f'[{timestr}] {msg}\n')
