"""Classes to generate MIDI files"""

import mido
from mido import MidiFile, MidiTrack, MetaMessage
import os


class TimeSignature:
    """Class to represent a time signature."""

    def __init__(self, numerator=4, denominator=4):
        self.numerator = numerator
        self.denominator = denominator

        if denominator not in [2, 4, 8, 16]:
            raise ValueError("Note value must be one of: 2, 4, 8, or 16.")

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"


class SingleTrackMidiFile:
    """Class to generate MIDI files."""

    def __init__(self, output_file="output.mid"):
        self.output_file = output_file
        self.mid = MidiFile()
        self.track = MidiTrack()
        self.mid.tracks.append(self.track)

    def set_tempo(self, bpm=60):
        """Set the tempo for the MIDI file."""
        tempo = mido.bpm2tempo(bpm)
        self.track.append(MetaMessage("set_tempo", tempo=tempo, time=0))

    def set_time_signature(self, time_signature: TimeSignature):
        """Set the time signature for the MIDI file."""

        self.track.append(
            MetaMessage(
                "time_signature",
                numerator=time_signature.numerator,
                denominator=time_signature.denominator,
                time=0,
            )
        )

    def save(self):
        """Save the MIDI file."""
        if os.path.exists(self.output_file):
            print(f"File {self.output_file} already exists. Removing it.")
            os.remove(self.output_file)

        print("Saving MIDI file to:", self.output_file)
        self.mid.save(self.output_file)
