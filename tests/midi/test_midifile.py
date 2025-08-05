import pytest
from enum import Enum
from unittest.mock import patch, MagicMock

from simplejam.midi.midifile import generate_midi_file_from_chord_sequence, TimeSignature, SingleTrackMidiFile


class MockScale(Enum):
    C4 = 60
    E4 = 64
    G4 = 67
    F4 = 65
    A4 = 69
    C5 = 72


@pytest.mark.parametrize("chord_sequence,tempo,time_signature,expected_notes", [
    pytest.param(
        [(MockScale.C4, MockScale.E4, MockScale.G4), (MockScale.F4, MockScale.A4, MockScale.C5)],
        120,
        TimeSignature(4, 4),
        [[60, 64, 67], [65, 69, 72]],
        id="2 chords as input"
    ),
    pytest.param(
        [],
        60,
        None,
        [],
        id="empty_sequence"
    )
])
@patch('simplejam.midi.midifile.SingleTrackMidiFile')
def test_generate_midi_file_from_chord_sequence(mock_single_track_midi_file, chord_sequence, tempo, time_signature, expected_notes):
    mock_midi_file_instance = MagicMock()
    mock_single_track_midi_file.return_value = mock_midi_file_instance
    
    # Mock the MIDI file and track attributes properly
    mock_mid = MagicMock()
    mock_track = MagicMock()
    mock_mid.tracks = [mock_track]
    mock_mid.ticks_per_beat = 480  # Standard MIDI ticks per beat
    mock_midi_file_instance.mid = mock_mid
    
    output_file = "test_output.mid"
    
    # Call function with parameters
    kwargs = {"output_file": output_file, "chord_sequence": chord_sequence, "tempo": tempo}
    if time_signature is not None:
        kwargs["time_signature"] = time_signature
    
    generate_midi_file_from_chord_sequence(**kwargs)
    
    # Assertions
    mock_single_track_midi_file.assert_called_once_with(output_file)
    mock_midi_file_instance.set_tempo.assert_called_once_with(tempo)
    if time_signature is not None:
        mock_midi_file_instance.set_time_signature.assert_called_once_with(time_signature)
    mock_midi_file_instance.save.assert_called_once()
    
    # Verify track.append was called for the expected number of messages
    if expected_notes:
        total_notes_events = sum(len(chord) for chord in expected_notes)
        expected_messages = total_notes_events * 2  # note_on + note_off per note
        assert mock_track.append.call_count == expected_messages
    else:
        # For empty sequence, no note messages should be added
        assert mock_track.append.call_count == 0


@pytest.mark.parametrize("denominator", [
    pytest.param(3, id="invalid_denominator_3"),
    pytest.param(1, id="invalid_denominator_1")
])
def test_time_signature_invalid_denominator_raises_value_error(denominator):
    with pytest.raises(ValueError, match="Note value must be one of: 2, 4, 8, or 16."):
        TimeSignature(4, denominator)


@pytest.mark.parametrize("numerator,denominator", [
    pytest.param(4, 4, id="4/4_time"),
    pytest.param(3, 8, id="3/8_time")
])
def test_time_signature_valid_input(numerator, denominator):
    time_sig = TimeSignature(numerator, denominator)
    assert time_sig.numerator == numerator
    assert time_sig.denominator == denominator
    assert str(time_sig) == f"{numerator}/{denominator}"


@pytest.mark.parametrize("output_file", [
    pytest.param("test.mid", id="custom_filename"),
    pytest.param("output.mid", id="standard_filename")
])
@patch('simplejam.midi.midifile.MidiFile')
@patch('simplejam.midi.midifile.MidiTrack')
def test_single_track_midi_file_constructor(mock_midi_track, mock_midi_file, output_file):
    mock_midi_file_instance = MagicMock()
    mock_track_instance = MagicMock()
    mock_midi_file.return_value = mock_midi_file_instance
    mock_midi_track.return_value = mock_track_instance
    
    midi_file = SingleTrackMidiFile(output_file)
    
    assert midi_file.output_file == output_file
    mock_midi_file.assert_called_once()
    mock_midi_track.assert_called_once()
    mock_midi_file_instance.tracks.append.assert_called_once_with(mock_track_instance)


@pytest.mark.parametrize("bpm", [
    pytest.param(120, id="standard_tempo"),
    pytest.param(60, id="default_tempo")
])
@patch('simplejam.midi.midifile.mido.bpm2tempo')
@patch('simplejam.midi.midifile.MetaMessage')
@patch('simplejam.midi.midifile.MidiFile')
@patch('simplejam.midi.midifile.MidiTrack')
def test_single_track_midi_file_set_tempo(mock_midi_track, mock_midi_file, mock_meta_message, mock_bpm2tempo, bpm):
    mock_midi_file_instance = MagicMock()
    mock_track_instance = MagicMock()
    mock_midi_file.return_value = mock_midi_file_instance
    mock_midi_track.return_value = mock_track_instance
    mock_tempo_value = 500000
    mock_bpm2tempo.return_value = mock_tempo_value
    mock_tempo_message = MagicMock()
    mock_meta_message.return_value = mock_tempo_message
    
    midi_file = SingleTrackMidiFile("test.mid")
    midi_file.set_tempo(bpm)
    
    mock_bpm2tempo.assert_called_once_with(bpm)
    mock_meta_message.assert_called_once_with("set_tempo", tempo=mock_tempo_value, time=0)
    mock_track_instance.append.assert_called_with(mock_tempo_message)


@pytest.mark.parametrize("numerator,denominator", [
    pytest.param(4, 4, id="4/4_time"),
    pytest.param(3, 8, id="3/8_time")
])
@patch('simplejam.midi.midifile.MetaMessage')
@patch('simplejam.midi.midifile.MidiFile')
@patch('simplejam.midi.midifile.MidiTrack')
def test_single_track_midi_file_set_time_signature(mock_midi_track, mock_midi_file, mock_meta_message, numerator, denominator):
    mock_midi_file_instance = MagicMock()
    mock_track_instance = MagicMock()
    mock_midi_file.return_value = mock_midi_file_instance
    mock_midi_track.return_value = mock_track_instance
    mock_time_sig_message = MagicMock()
    mock_meta_message.return_value = mock_time_sig_message
    
    midi_file = SingleTrackMidiFile("test.mid")
    time_signature = TimeSignature(numerator, denominator)
    midi_file.set_time_signature(time_signature)
    
    mock_meta_message.assert_called_once_with(
        "time_signature",
        numerator=numerator,
        denominator=denominator,
        time=0
    )
    mock_track_instance.append.assert_called_with(mock_time_sig_message)


@pytest.mark.parametrize("file_exists", [
    pytest.param(True, id="file_exists"),
    pytest.param(False, id="file_does_not_exist")
])
@patch('simplejam.midi.midifile.os.remove')
@patch('simplejam.midi.midifile.os.path.exists')
@patch('simplejam.midi.midifile.MidiFile')
@patch('simplejam.midi.midifile.MidiTrack')
def test_single_track_midi_file_save(mock_midi_track, mock_midi_file, mock_exists, mock_remove, file_exists):
    mock_midi_file_instance = MagicMock()
    mock_track_instance = MagicMock()
    mock_midi_file.return_value = mock_midi_file_instance
    mock_midi_track.return_value = mock_track_instance
    mock_exists.return_value = file_exists
    
    output_file = "test.mid"
    midi_file = SingleTrackMidiFile(output_file)
    midi_file.save()
    
    mock_exists.assert_called_once_with(output_file)
    if file_exists:
        mock_remove.assert_called_once_with(output_file)
    else:
        mock_remove.assert_not_called()
    mock_midi_file_instance.save.assert_called_once_with(output_file)
