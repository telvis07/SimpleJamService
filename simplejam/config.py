from environs import env

env.read_env()  # read .env file, if it exists

# Read OUTPUT_FILES_DIRECTORY from .env file
OUTPUT_FILES_DIRECTORY = env("OUTPUT_FILES_DIRECTORY")
