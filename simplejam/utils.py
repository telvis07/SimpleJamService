"""Utility function to generate MIDI files"""

from mido import Message
import os
from simplejam.keys.C_major import CModes
from simplejam.keys.D_major import DModes
from simplejam.midifile import TimeSignature, SingleTrackMidiFile


def generate_example_chords_file(
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
    ticks_per_beat = mid.ticks_per_beat

    for mode in chord_sequence:
        chord_notes = [note.value for note in mode.value]
        # Note on for all notes in the chord at the start of the beat
        for note in chord_notes:
            track.append(Message("note_on", note=note, velocity=64, time=0))
        # Note off for all notes after the full beat
        for note in chord_notes:
            # ensure that the time delta (the delay before the MIDI event) is
            # only set for the first note in the chord.
            time = ticks_per_beat if note == chord_notes[0] else 0
            track.append(Message("note_off", note=note, velocity=64, time=time))

    fg.save()


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
            "c_major.mid",
        ),
        chord_sequence=list(CModes),
        tempo=60,
        time_signature=TimeSignature(4, 4),
    )

    generate_example_chords_file(
        os.path.join(
            "/Users/telviscalhoun/work/SimpleJamService/output",
            "d_major.mid",
        ),
        chord_sequence=list(DModes),
        tempo=60,
        time_signature=TimeSignature(4, 4),
    )
