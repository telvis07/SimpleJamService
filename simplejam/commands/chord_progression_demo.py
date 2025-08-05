"""Chord progression demo for generating MIDI files with number chord sequences."""

from simplejam.midi.midifile import generate_midi_file_from_chord_sequence
from simplejam.midi.logic.generators import generate_number_chord_sequence
from simplejam.schemas import KeyChordProgression
from simplejam import config
import os


def run() -> None:
    """Demo generate_number_chord_sequence."""

    # Example: C major II-V-I and D major IV-V-I
    progressions = [
        KeyChordProgression(key="C", number_chord_sequence=("II", "V", "I", "I")),
        KeyChordProgression(key="D", number_chord_sequence=("IV", "V", "I", "I")),
    ]
    chord_sequences = generate_number_chord_sequence(progressions)
    output_file = os.path.join(
        config.OUTPUT_FILES_DIRECTORY,
        "chord_progression_demo.mid",
    )

    generate_midi_file_from_chord_sequence(
        output_file=output_file, chord_sequence=chord_sequences
    )


if __name__ == "__main__":
    run()
    print("Generated chord progression demo MIDI file.")
