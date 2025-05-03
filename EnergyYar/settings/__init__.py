"""
try to activate local settings. if it failed, we
load the production environment.
"""

try:
    from EnergyYar.settings.local import *
except ImportError:
    from EnergyYar.settings.production import *

