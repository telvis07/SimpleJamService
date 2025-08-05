import pytest
from unittest.mock import patch, MagicMock
from simplejam.commands import chord_progression_demo
from simplejam.schemas import KeyChordProgression


@pytest.mark.parametrize("progressions,expected_chord_sequences", [
    pytest.param(
        [KeyChordProgression(key="C", number_chord_sequence=("II", "V", "I"))],
        "mock_chord_sequences_single",
        id="single_progression"
    ),
    pytest.param(
        [
            KeyChordProgression(key="C", number_chord_sequence=("II", "V", "I", "I")),
            KeyChordProgression(key="D", number_chord_sequence=("IV", "V", "I", "I"))
        ],
        "mock_chord_sequences_multiple",
        id="multiple_progressions"
    )
])
@patch('simplejam.commands.chord_progression_demo.generate_midi_file_from_chord_sequence')
@patch('simplejam.commands.chord_progression_demo.generate_number_chord_sequence')
@patch('simplejam.commands.chord_progression_demo.config')
@patch('simplejam.commands.chord_progression_demo.os.path.join')
def test_run(mock_join, mock_config, mock_generate_number, mock_generate_midi, progressions, expected_chord_sequences):
    mock_chord_sequences = ["mock_chord_1", "mock_chord_2"]
    mock_generate_number.return_value = mock_chord_sequences
    mock_config.OUTPUT_FILES_DIRECTORY = "/mock/output/dir"
    mock_join.return_value = "/mock/output/dir/chord_progression_demo.mid"
    
    chord_progression_demo.run()
    
    mock_generate_number.assert_called_once()
    called_progressions = mock_generate_number.call_args[0][0]
    
    assert len(called_progressions) == 2
    assert called_progressions[0].key == "C"
    assert called_progressions[0].number_chord_sequence == ("II", "V", "I", "I")
    assert called_progressions[1].key == "D"
    assert called_progressions[1].number_chord_sequence == ("IV", "V", "I", "I")
    
    mock_join.assert_called_once_with(mock_config.OUTPUT_FILES_DIRECTORY, "chord_progression_demo.mid")
    mock_generate_midi.assert_called_once_with(
        output_file="/mock/output/dir/chord_progression_demo.mid",
        chord_sequence=mock_chord_sequences
    )