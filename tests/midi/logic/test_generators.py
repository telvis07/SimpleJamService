import pytest
from unittest.mock import patch, MagicMock
from simplejam.midi.logic.generators import generate_number_chord_sequence
from simplejam.schemas import KeyChordProgression


@pytest.mark.parametrize("progressions,expected_result", [
    pytest.param(
        [KeyChordProgression(key="C", number_chord_sequence=("I", "V", "VI"))],
        ["mock_c_I", "mock_c_V", "mock_c_VI"],
        id="single_c_major_progression"
    ),
    pytest.param(
        [
            KeyChordProgression(key="C", number_chord_sequence=("II", "V")),
            KeyChordProgression(key="D", number_chord_sequence=("IV", "I"))
        ],
        ["mock_c_II", "mock_c_V", "mock_d_IV", "mock_d_I"],
        id="multiple_progressions"
    )
])
@patch('simplejam.midi.logic.generators.C_major')
@patch('simplejam.midi.logic.generators.D_major')
def test_generate_number_chord_sequence_valid(mock_d_major, mock_c_major, progressions, expected_result):
    # Setup mocks
    mock_c_chords = MagicMock()
    mock_d_chords = MagicMock()
    
    # Configure C major chord access
    mock_c_chords.__getitem__ = MagicMock(side_effect=lambda x: f"mock_c_{x}")
    mock_c_major.DiatonicTriads = mock_c_chords
    
    # Configure D major chord access  
    mock_d_chords.__getitem__ = MagicMock(side_effect=lambda x: f"mock_d_{x}")
    mock_d_major.DiatonicTriads = mock_d_chords
    
    result = generate_number_chord_sequence(progressions)
    
    assert result == expected_result


@pytest.mark.parametrize("invalid_key,expected_error", [
    pytest.param(
        "E",
        r"Key 'E' is not supported. Available keys: \['C', 'D'\]",
        id="unsupported_key_E"
    ),
    pytest.param(
        "G",
        r"Key 'G' is not supported. Available keys: \['C', 'D'\]",
        id="unsupported_key_G"
    )
])
def test_generate_number_chord_sequence_invalid_key(invalid_key, expected_error):
    progressions = [KeyChordProgression(key=invalid_key, number_chord_sequence=("I", "V"))]
    
    with pytest.raises(ValueError, match=expected_error):
        generate_number_chord_sequence(progressions)


@pytest.mark.parametrize("key,invalid_numeral,expected_error", [
    pytest.param(
        "C",
        "IX",
        "Invalid chord numeral 'IX' for key 'C'",
        id="invalid_numeral_c_major"
    ),
    pytest.param(
        "D", 
        "X",
        "Invalid chord numeral 'X' for key 'D'",
        id="invalid_numeral_d_major"
    )
])
@patch('simplejam.midi.logic.generators.C_major')
@patch('simplejam.midi.logic.generators.D_major')
def test_generate_number_chord_sequence_invalid_numeral(mock_d_major, mock_c_major, key, invalid_numeral, expected_error):
    # Setup mocks to raise AttributeError for invalid numerals
    mock_c_chords = MagicMock()
    mock_d_chords = MagicMock()
    
    def c_chord_getter(numeral):
        if numeral in ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]:
            return f"mock_c_{numeral}"
        raise AttributeError()
    
    def d_chord_getter(numeral):
        if numeral in ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]:
            return f"mock_d_{numeral}"
        raise AttributeError()
    
    mock_c_chords.__getitem__ = MagicMock(side_effect=c_chord_getter)
    mock_d_chords.__getitem__ = MagicMock(side_effect=d_chord_getter)
    
    mock_c_major.DiatonicTriads = mock_c_chords
    mock_d_major.DiatonicTriads = mock_d_chords
    
    progressions = [KeyChordProgression(key=key, number_chord_sequence=(invalid_numeral,))]
    
    with pytest.raises(ValueError, match=expected_error):
        generate_number_chord_sequence(progressions)