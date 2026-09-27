"""The drawing helpers are shared by every car and live in lib/wiring.py; this points them at this car's folder."""
import os, sys
_here = os.path.dirname(os.path.abspath(__file__))
os.environ['WIRING_CAR_DIR'] = os.path.dirname(_here)
sys.path.insert(0, os.path.join(_here, '..', '..', 'lib'))
from wiring import *                                   # noqa: F401,F403
from wiring import _ink                                # a leading underscore isn't exported by *
