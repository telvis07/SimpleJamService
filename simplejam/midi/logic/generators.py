from simplejam.midi.keys import C_major
from simplejam.midi.keys import D_major
from simplejam.schemas import KeyChordProgression


def generate_number_chord_sequence(
    progressions: list[KeyChordProgression],
) -> list[list]:
    """Generate sequences of chords for a list of KeyChordProgression objects.

    Example input:

    generate_number_chord_sequence([
        KeyChordProgression(key="C", number_chord_sequence=("II", "V", "I")),
        KeyChordProgression(key="D", number_chord_sequence=("IV", "V", "I")),
    ])

    Example output:
        [
            C_major.DiatonicTriads.II,
            C_major.DiatonicTriads.V,
            C_major.DiatonicTriads.I,
            D_major.DiatonicTriads.IV,
            D_major.DiatonicTriads.V,
            D_major.DiatonicTriads.I,
        ]
    """
    key_modes = {
        "C": C_major.DiatonicTriads,
        "D": D_major.DiatonicTriads,
    }

    results = []
    for progression in progressions:
        key = progression.key
        number_chord_sequence = tuple(
            n.upper() for n in progression.number_chord_sequence
        )
        if key not in key_modes:
            raise ValueError(
                f"Key '{key}' is not supported. Available keys: {list(key_modes.keys())}"
            )
        key_chords = key_modes[key]
        chords = []
        for numeral in number_chord_sequence:
            try:
                chord = key_chords[numeral]
                chords.append(chord)
            except AttributeError:
                raise ValueError(f"Invalid chord numeral '{numeral}' for key '{key}'")
        results.extend(chords)
    return results
