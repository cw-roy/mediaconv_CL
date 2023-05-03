#!/usr/bin/env python3

""" Converts video files to .mp4 using FFMpeg."""

import os
from pathlib import Path
import subprocess
import time


FILE_EXTENSIONS = (
    ".mp4",
    ".mkv",
    ".mov",
    ".avi",
    ".3gp",
    ".flv",
    ".mk4",
    ".mpg",
)


def scan_directory():
    """
    Scans the "convert_media" directory for files with the specified file extensions.
    Returns a list of matching file paths.
    """
    log_messages = []
    matching_files = []

    for file_name in os.listdir("convert_media"):
        if file_name.endswith(FILE_EXTENSIONS):
            matching_files.append(os.path.join("convert_media", file_name))
        else:
            log_messages.append(f'"{file_name}" does not match a supported file type.')

    if not matching_files:
        log_messages.append("No matching files found in directory.")
        return None, log_messages

    return matching_files, log_messages


def convert_files(file_paths, log_file):
    """
    Converts each file in the provided list to mp4 using FFmpeg.
    Converted files are saved to the 'converted_media' folder in the same directory as the script.
    """
    log_messages = []
    converted_folder = Path(os.path.dirname(__file__)) / "converted_media"
    converted_folder.mkdir(exist_ok=True)

    for file_path in file_paths:
        try:
            file_name = Path(file_path).name
            file_prefix = Path(file_path).stem
            output_file_path = converted_folder / f"{file_prefix}_converted.mp4"

            start_time = time.time()

            subprocess.run(
                ["ffmpeg", "-i", file_path, "-q:v", "0", output_file_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )

            duration = time.time() - start_time
            minutes = int(duration // 60)
            seconds = int(duration % 60)

            log_messages.append(
                f'"{file_name}" was converted to "{output_file_path.name}" in {minutes}m{seconds}s.'
            )

        except subprocess.CalledProcessError as errors:
            log_messages.append(
                f'Error converting "{file_path}": {errors.output.decode()}'
            )

    # Write conversion log to the provided log file
    log_file.write("\n".join(log_messages))
    log_file.write("\n")


def main():
    """
    Main function to run the program.
    """
    converted_folder = os.path.join(os.path.dirname(__file__), "converted_media")
    os.makedirs(converted_folder, exist_ok=True)

    log_file_name = os.path.join(
        converted_folder, f'conversion_log_{time.strftime("%Y%m%d_%H%M%S")}.log'
    )

    with open(log_file_name, "w", encoding="utf-8") as log_file:
        matching_files, scan_log_messages = scan_directory()
        log_file.write("\n".join(scan_log_messages))
        log_file.write("\n\n")

        if not matching_files:
            return

        convert_files(matching_files, log_file)

    print(f'Conversion complete. Log file saved to "{log_file_name}".')


if __name__ == "__main__":
    main()
