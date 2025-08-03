"""Key of C major."""

from enum import Enum


class CMajorScale(Enum):
    C4 = 60
    D4 = 62
    E4 = 64
    F4 = 65
    G4 = 67
    A4 = 69
    B4 = 71
    C5 = 72
    D5 = 74
    E5 = 76
    F5 = 77
    G5 = 79
    A5 = 81
    B5 = 83


class CModes(Enum):
    # C Major 7
    I = (CMajorScale.C4, CMajorScale.E4, CMajorScale.G4)
    # D Minor 7
    II = (CMajorScale.D4, CMajorScale.F4, CMajorScale.A4)
    # E Minor 7
    III = (CMajorScale.E4, CMajorScale.G4, CMajorScale.B4)
    # F Major 7
    IV = (CMajorScale.F4, CMajorScale.A4, CMajorScale.C5)
    # G Dominant 7
    V = (CMajorScale.G4, CMajorScale.B4, CMajorScale.D5)
    # A Minor 7
    VI = (CMajorScale.A4, CMajorScale.C5, CMajorScale.E5)
    # B minor 7 flat 5
    VII = (CMajorScale.B4, CMajorScale.D5, CMajorScale.F5)
    # C Major 7
    VIII = (CMajorScale.C5, CMajorScale.E5, CMajorScale.G5)
