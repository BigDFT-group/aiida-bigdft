
from datetime import datetime
import getpass

try:
    from aiida_bigdft.paths import DEBUG_PATHS
except ImportError:
    DEBUG_PATHS = None


def debug(msg, wipe=False, time=True):
    if not DEBUG_PATHS:
        return
    mode = 'w+' if wipe else 'a'
    timestr = datetime.now().strftime('%H:%M:%S')

    usr = getpass.getuser()

    try:
        with open(DEBUG_PATHS[usr], mode) as o:
            if not time:
                o.write(f'{msg}\n')
                return
            o.write(f'[{timestr}] {msg}\n')
    except KeyError:
        pass
