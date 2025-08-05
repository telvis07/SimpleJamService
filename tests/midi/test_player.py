import pytest
from unittest.mock import patch, MagicMock, call
from simplejam.midi import player


@pytest.mark.parametrize("filepath,wait_for_completion", [
    pytest.param(
        "/path/to/valid/file.mid",
        True,
        id="valid_file_wait_completion"
    ),
    pytest.param(
        "/path/to/another/file.mid", 
        False,
        id="valid_file_no_wait"
    )
])
@patch('simplejam.midi.player.pygame')
@patch('simplejam.midi.player.time')
@patch('simplejam.midi.player.os.path.exists')
def test_play_midi_file__pygame_success(mock_exists, mock_time, mock_pygame, filepath, wait_for_completion):
    # Setup mocks
    mock_exists.return_value = True
    mock_pygame.mixer.music.get_busy.side_effect = [True, True, False]  # Busy for 2 iterations, then done
    
    player.play_midi_file__pygame(filepath, wait_for_completion)
    
    # Verify pygame initialization and file operations
    mock_pygame.mixer.init.assert_called_once_with(frequency=22050, size=-16, channels=2, buffer=512)
    mock_pygame.mixer.music.load.assert_called_once_with(filepath)
    mock_pygame.mixer.music.play.assert_called_once()
    mock_pygame.mixer.quit.assert_called_once()
    
    if wait_for_completion:
        # Should call get_busy until it returns False
        assert mock_pygame.mixer.music.get_busy.call_count == 3
        assert mock_time.sleep.call_count == 2
        mock_time.sleep.assert_has_calls([call(0.1), call(0.1)])
    else:
        # Should not wait, no calls to get_busy or sleep
        mock_pygame.mixer.music.get_busy.assert_not_called()
        mock_time.sleep.assert_not_called()


@pytest.mark.parametrize("filepath", [
    pytest.param("/nonexistent/file.mid", id="nonexistent_file"),
    pytest.param("/invalid/path/file.mid", id="invalid_path")
])
@patch('simplejam.midi.player.os.path.exists')
def test_play_midi_file__pygame_file_not_found(mock_exists, filepath):
    mock_exists.return_value = False
    
    with pytest.raises(FileNotFoundError, match=f"MIDI file not found: {filepath}"):
        player.play_midi_file__pygame(filepath)


@pytest.mark.parametrize("pygame_error_msg", [
    pytest.param("Unable to load MIDI file", id="load_error"),
    pytest.param("Audio device not available", id="audio_error")
])
@patch('simplejam.midi.player.pygame')
@patch('simplejam.midi.player.os.path.exists')
def test_play_midi_file__pygame_runtime_error(mock_exists, mock_pygame, pygame_error_msg):
    mock_exists.return_value = True
    mock_pygame.error = Exception  # Mock pygame.error as base Exception
    mock_pygame.mixer.music.load.side_effect = mock_pygame.error(pygame_error_msg)
    
    with pytest.raises(RuntimeError, match=f"Error playing MIDI file: {pygame_error_msg}"):
        player.play_midi_file__pygame("/valid/file.mid")
    
    # Ensure cleanup still happens
    mock_pygame.mixer.quit.assert_called_once()


@pytest.mark.parametrize("file_path_arg", [
    pytest.param("test.mid", id="simple_filename"),
    pytest.param("/path/to/song.mid", id="full_path")
])
@patch('simplejam.midi.player.argparse.ArgumentParser')
def test_parse_args(mock_argument_parser, file_path_arg):
    mock_parser = MagicMock()
    mock_argument_parser.return_value = mock_parser
    mock_args = MagicMock()
    mock_args.file_path = file_path_arg
    mock_parser.parse_args.return_value = mock_args
    
    result = player.parse_args()
    
    mock_argument_parser.assert_called_once_with(description="Play MIDI files using pygame")
    mock_parser.add_argument.assert_called_once_with("file_path", help="Path to the MIDI file to play")
    mock_parser.parse_args.assert_called_once()
    assert result.file_path == file_path_arg


@pytest.mark.parametrize("file_path,file_exists,should_raise", [
    pytest.param(
        "existing_file.mid",
        True,
        False,
        id="valid_existing_file"
    ),
    pytest.param(
        "nonexistent_file.mid",
        False,
        True,
        id="nonexistent_file_error"
    )
])
@patch('simplejam.midi.player.play_midi_file__pygame')
@patch('simplejam.midi.player.parse_args')
@patch('simplejam.midi.player.os.path.realpath')
@patch('simplejam.midi.player.os.path.isfile')
@patch('builtins.print')
def test_run(mock_print, mock_isfile, mock_realpath, mock_parse_args, mock_play_midi, file_path, file_exists, should_raise):
    # Setup mocks
    mock_args = MagicMock()
    mock_args.file_path = file_path
    mock_parse_args.return_value = mock_args
    mock_realpath.return_value = f"/absolute/path/{file_path}"
    mock_isfile.return_value = file_exists
    
    if should_raise:
        # Test file not found case
        with pytest.raises(FileNotFoundError, match=f"MIDI file not found: /absolute/path/{file_path}"):
            player.run()
        mock_play_midi.assert_not_called()
        mock_print.assert_not_called()
    else:
        # Test successful case
        player.run()
        mock_play_midi.assert_called_once_with(f"/absolute/path/{file_path}")
        mock_print.assert_called_once_with(f"Finished playing: /absolute/path/{file_path}")
    
    mock_parse_args.assert_called_once()
    mock_realpath.assert_called_once_with(file_path)
    mock_isfile.assert_called_once_with(f"/absolute/path/{file_path}")


@pytest.mark.parametrize("exception_type,exception_msg", [
    pytest.param(
        FileNotFoundError,
        "File not found",
        id="file_not_found_exception"
    ),
    pytest.param(
        RuntimeError,
        "Audio system error",
        id="runtime_exception"
    )
])
@patch('simplejam.midi.player.play_midi_file__pygame')
@patch('simplejam.midi.player.parse_args')
@patch('simplejam.midi.player.os.path.realpath')
@patch('simplejam.midi.player.os.path.isfile')
@patch('builtins.print')
def test_run_exception_handling(mock_print, mock_isfile, mock_realpath, mock_parse_args, mock_play_midi, exception_type, exception_msg):
    # Setup mocks
    mock_args = MagicMock()
    mock_args.file_path = "test.mid"
    mock_parse_args.return_value = mock_args
    mock_realpath.return_value = "/absolute/path/test.mid"
    mock_isfile.return_value = True
    mock_play_midi.side_effect = exception_type(exception_msg)
    
    player.run()
    
    mock_play_midi.assert_called_once_with("/absolute/path/test.mid")
    mock_print.assert_called_once_with(f"Error: {exception_msg}")