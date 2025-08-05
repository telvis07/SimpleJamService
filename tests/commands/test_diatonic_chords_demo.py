import pytest
from unittest.mock import patch, call, ANY
from simplejam.commands import diatonic_chords_demo


@pytest.mark.parametrize("c_major_chords,d_major_chords", [
    pytest.param(
        ["mock_c_chord_1", "mock_c_chord_2"],
        ["mock_d_chord_1", "mock_d_chord_2"],
        id="mock_chord_sequences"
    ),
    pytest.param(
        ["single_c_chord"],
        ["single_d_chord"], 
        id="single_chords"
    )
])
@patch('simplejam.commands.diatonic_chords_demo.generate_midi_file_from_chord_sequence')
@patch('simplejam.commands.diatonic_chords_demo.os.path.join')
@patch('simplejam.commands.diatonic_chords_demo.C_major')
@patch('simplejam.commands.diatonic_chords_demo.D_major')
@patch('builtins.print')
def test_run(mock_print, mock_d_major, mock_c_major, mock_join, mock_generate_midi, c_major_chords, d_major_chords):
    mock_c_major.DiatonicTriads.values.return_value = c_major_chords
    mock_d_major.DiatonicTriads.values.return_value = d_major_chords
    
    mock_join.side_effect = [
        "/Users/telviscalhoun/work/SimpleJamService/output/c_major.mid",
        "/Users/telviscalhoun/work/SimpleJamService/output/d_major.mid"
    ]
    
    diatonic_chords_demo.run()
    
    assert mock_generate_midi.call_count == 2
    
    # Check the first call (C major)
    first_call = mock_generate_midi.call_args_list[0]
    assert first_call[0][0] == "/Users/telviscalhoun/work/SimpleJamService/output/c_major.mid"
    assert first_call[1]['chord_sequence'] == list(c_major_chords)
    assert first_call[1]['tempo'] == 60
    assert first_call[1]['time_signature'].numerator == 4
    assert first_call[1]['time_signature'].denominator == 4
    
    # Check the second call (D major)
    second_call = mock_generate_midi.call_args_list[1]
    assert second_call[0][0] == "/Users/telviscalhoun/work/SimpleJamService/output/d_major.mid"
    assert second_call[1]['chord_sequence'] == list(d_major_chords)
    assert second_call[1]['tempo'] == 60
    assert second_call[1]['time_signature'].numerator == 4
    assert second_call[1]['time_signature'].denominator == 4
    
    mock_join.assert_has_calls([
        call("/Users/telviscalhoun/work/SimpleJamService/output", "c_major.mid"),
        call("/Users/telviscalhoun/work/SimpleJamService/output", "d_major.mid")
    ])
    
    mock_print.assert_called_once_with("Generated chords file")