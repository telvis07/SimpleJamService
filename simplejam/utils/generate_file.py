"""Utility function to generate MIDI files"""

import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage
import os
from simplejam.keys.C_major import CModes


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
        self.mid.save(self.output_file)


# def generate_example_single_note_file(
#         output_file='c_notes_8_beats.mid',
#         bpm=60,
#         time_signature=TimeSignature(4, 4)):
#     """Create an example file."""
#
#     # mid = MidiFile()
#     # track = MidiTrack()
#     # mid.tracks.append(track)
#     fg = SingleTrackMidiFile(output_file)
#     fg.set_tempo(bpm)
#     fg.set_time_signature(time_signature)
#     mid = fg.mid
#     track = mid.tracks[0]
#
#     # Set tempo (60 BPM)
#     # tempo = mido.bpm2tempo(60)
#     # track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
#     #
#     # # Set time signature (4/4)
#     # track.append(MetaMessage('time_signature', numerator=4, denominator=4, time=0))
#
#     # MIDI note numbers for C major scale (C4 to C5) using CMajorScale enum
#     c_major_scale = [note.value for note in CMajorScale]
#     ticks_per_beat = mid.ticks_per_beat
#
#     for note in c_major_scale:
#         # Note on at the start of the beat
#         track.append(Message('note_on', note=note, velocity=64, time=0))
#         # Note off after the full beat
#         track.append(Message('note_off', note=note, velocity=64, time=ticks_per_beat))
#
#     mid.save(output_file)


def generate_example_chords_file(
    output_file: str = "c_chords_7_beats.mid",
    tempo: int = 60,
    time_signature: TimeSignature = TimeSignature(4, 4),
):
    """Create an example file with each chord from CModes."""
    fg = SingleTrackMidiFile(output_file)
    fg.set_tempo(tempo)
    fg.set_time_signature(time_signature)
    mid = fg.mid
    track = mid.tracks[0]
    ticks_per_beat = mid.ticks_per_beat

    for mode in CModes:
        chord_notes = [note.value for note in mode.value]
        # Note on for all notes in the chord at the start of the beat
        for note in chord_notes:
            track.append(Message("note_on", note=note, velocity=64, time=0))
        # Note off for all notes after the full beat
        for note in chord_notes:
            # track.append(Message('note_off', note=note, velocity=64, time=ticks_per_beat))
            time = ticks_per_beat if note == chord_notes[0] else 0
            track.append(Message("note_off", note=note, velocity=64, time=time))

    if os.path.exists(output_file):
        print(f"File {output_file} already exists. Removing it.")
        os.remove(output_file)

    mid.save(output_file)


if __name__ == "__main__":
    # generate_example_single_note_file(
    #     os.path.join(
    #         "/Users/telviscalhoun/work/SimpleJamService/output",
    #         "c_scale_8_beats.mid",
    #     )
    # )
    # Example usage for chords file:
    generate_example_chords_file(
        os.path.join(
            "/Users/telviscalhoun/work/SimpleJamService/output",
            "c_chords_7_beats.mid",
        ),
        tempo=60,
        time_signature=TimeSignature(4, 4),
    )
