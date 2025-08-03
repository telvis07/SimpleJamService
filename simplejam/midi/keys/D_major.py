from enum import Enum
from collections import OrderedDict
from types import MappingProxyType


class DMajorScale(Enum):
    D4 = 62
    E4 = 64
    F_SHARP_4 = 66
    G4 = 67
    A4 = 69
    B4 = 71
    C_SHARP_5 = 73
    D5 = 74
    E5 = 76
    F_SHARP_5 = 78
    G5 = 79
    A5 = 81
    B5 = 83
    C_SHARP_6 = 85


DiatonicTriads = MappingProxyType(
    OrderedDict(
        [
            ("I", (DMajorScale.D4, DMajorScale.F_SHARP_4, DMajorScale.A4)),
            ("II", (DMajorScale.E4, DMajorScale.G4, DMajorScale.B4)),
            ("III", (DMajorScale.F_SHARP_4, DMajorScale.A4, DMajorScale.C_SHARP_5)),
            ("IV", (DMajorScale.G4, DMajorScale.B4, DMajorScale.D5)),
            ("V", (DMajorScale.A4, DMajorScale.C_SHARP_5, DMajorScale.E5)),
            ("VI", (DMajorScale.B4, DMajorScale.D5, DMajorScale.F_SHARP_5)),
            ("VII", (DMajorScale.C_SHARP_5, DMajorScale.E5, DMajorScale.G5)),
            ("VIII", (DMajorScale.D5, DMajorScale.F_SHARP_5, DMajorScale.A5)),
        ]
    )
)
