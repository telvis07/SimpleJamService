from enum import Enum

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

class DModes(Enum):
    I = [DMajorScale.D4, DMajorScale.F_SHARP_4, DMajorScale.A4]      # D major (I)
    II = [DMajorScale.E4, DMajorScale.G4, DMajorScale.B4]          # E minor (ii)
    III = [DMajorScale.F_SHARP_4, DMajorScale.A4, DMajorScale.C_SHARP_5]  # F# minor (iii)
    IV = [DMajorScale.G4, DMajorScale.B4, DMajorScale.D5]          # G major (IV)
    V = [DMajorScale.A4, DMajorScale.C_SHARP_5, DMajorScale.E5]     # A major (V)
    VI = [DMajorScale.B4, DMajorScale.D5, DMajorScale.F_SHARP_5]    # B minor (vi)
    VII = [DMajorScale.C_SHARP_5, DMajorScale.E5, DMajorScale.G5]   # C# diminished (vii°)
    VIII = [DMajorScale.D5, DMajorScale.F_SHARP_5, DMajorScale.A5]  # D major (I) in higher octave

