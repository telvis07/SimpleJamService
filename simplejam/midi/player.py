import pygame
import time
import os
import argparse


def play_midi_file__pygame(filepath: str, wait_for_completion: bool = True) -> None:
    """
    Play a MIDI file using pygame mixer.

    Args:
        filepath: Path to the MIDI file to play
        wait_for_completion: If True, wait for the file to finish playing
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"MIDI file not found: {filepath}")

    # Initialize pygame mixer
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

    try:
        # Load and play the MIDI file
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()

        if wait_for_completion:
            # Wait for the music to finish playing
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

    except pygame.error as e:
        raise RuntimeError(f"Error playing MIDI file: {e}")

    finally:
        pygame.mixer.quit()


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Play MIDI files using pygame")
    parser.add_argument("file_path", help="Path to the MIDI file to play")
    return parser.parse_args()


def run() -> None:
    """
    Convenience function to play the output from generate_example_chords_file.

    Args:
        input_file: Name of the MIDI file to play (should match generate_example_chords_file output)
    """
    args = parse_args()
    input_file = os.path.realpath(args.file_path)
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"MIDI file not found: {input_file}")

    try:
        play_midi_file__pygame(input_file)
        print(f"Finished playing: {input_file}")
    except (FileNotFoundError, RuntimeError) as e:
        print(f"Error: {e}")
