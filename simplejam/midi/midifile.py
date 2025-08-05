"""Classes to generate MIDI files"""

import mido
from mido import MidiFile, MidiTrack, MetaMessage, Message
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

    def __init__(self, output_file):
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


def generate_midi_file_from_chord_sequence(
    output_file: str,
    chord_sequence: list,
    tempo: int = 60,
    time_signature: TimeSignature = TimeSignature(4, 4),
):
    """Create an example file with each chord from CModes."""
    fg = SingleTrackMidiFile(output_file)
    fg.set_tempo(tempo)
    fg.set_time_signature(time_signature)
    mid = fg.mid
    track = mid.tracks[0]
    ticks_per_beat = mid.ticks_per_beat * 4

    for chord in chord_sequence:
        # Convert the scale enum entry to the mapped value
        chord_notes = [note.value for note in chord]

        # Note on for all notes in the chord at the start of the beat
        for note in chord_notes:
            track.append(Message("note_on", note=note, velocity=90, time=0))
        # Note off for all notes after the full beat
        for note in chord_notes:
            # ensure that the time delta (the delay before the MIDI event) is
            # only set for the first note in the chord.
            time = ticks_per_beat if note == chord_notes[0] else 0
            track.append(Message("note_off", note=note, velocity=90, time=time))

    fg.save()
