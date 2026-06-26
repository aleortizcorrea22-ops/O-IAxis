"""API route modules for O-IAxis motors and services"""

from . import m2_tesoreria
from . import m5_fiscal
from . import m1_m3_m4_m6
from . import m7_m12_frontera
from . import ml_predictions
from . import quantum

__all__ = [
    "m2_tesoreria", "m5_fiscal", "m1_m3_m4_m6",
    "m7_m12_frontera", "ml_predictions", "quantum"
]
