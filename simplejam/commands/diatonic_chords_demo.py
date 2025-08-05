"""Demonstration of generating diatonic chords in MIDI files for C major and D major keys."""

import os
from simplejam.midi.keys import C_major, D_major
from simplejam.midi.midifile import (
    TimeSignature,
    generate_midi_file_from_chord_sequence,
)


def run() -> None:
    generate_midi_file_from_chord_sequence(
        os.path.join(
            "/Users/telviscalhoun/work/SimpleJamService/output",
            "c_major.mid",
        ),
        chord_sequence=list(C_major.DiatonicTriads.values()),
        tempo=60,
        time_signature=TimeSignature(4, 4),
    )

    generate_midi_file_from_chord_sequence(
        os.path.join(
            "/Users/telviscalhoun/work/SimpleJamService/output",
            "d_major.mid",
        ),
        chord_sequence=list(D_major.DiatonicTriads.values()),
        tempo=60,
        time_signature=TimeSignature(4, 4),
    )
    print("Generated chords file")


if __name__ == "__main__":
    run()
