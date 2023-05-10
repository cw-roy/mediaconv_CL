#!/usr/bin/env python3

"""Converts video files to .mp4 using FFmpeg."""

import os
import subprocess
import time
from pathlib import Path


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


def get_matching_files(directory):
    """
    Scans the specified directory for files with the supported file extensions.
    Returns a list of matching file paths.
    """
    matching_files = []
    log_messages = []

    for file_name in os.scandir(directory):
        if file_name.name.endswith(FILE_EXTENSIONS) and file_name.is_file():
            matching_files.append(file_name.path)
        else:
            log_messages.append(
                f'"{file_name.name}" does not match a supported file type.'
            )

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
    converted_folder = Path(__file__).parent / "converted_media"
    converted_folder.mkdir(exist_ok=True)

    for file_path in file_paths:
        try:
            file_name = Path(file_path).name
            file_prefix = Path(file_path).stem

            # Replace spaces with underscores in the file prefix
            file_prefix = file_prefix.replace(" ", "_")

            # Check if the output file already exists
            counter = 1
            output_file_path = converted_folder / f"{file_prefix}_converted.mp4"
            while output_file_path.exists():
                # Generate a new output filename with the counter
                output_file_path = (
                    converted_folder / f"{file_prefix}_converted_{counter}.mp4"
                )
                counter += 1

            start_time = time.time()

            subprocess.run(
                ["ffmpeg", "-i", file_path, "-q:v", "0", output_file_path],
                capture_output=True,
                text=True,
                check=True,
            )

            duration = time.time() - start_time
            minutes, seconds = divmod(duration, 60)

            log_messages.append(
                f'"{file_name}" was converted to "{output_file_path.name}" in {minutes:.0f}m{seconds:.0f}s.'
            )

        except subprocess.CalledProcessError as errors:
            log_messages.append(
                f'Error converting "{file_path}": {errors.stdout.strip()}'
            )

    # Write conversion log to the provided log file
    log_file.write("\n".join(log_messages))
    log_file.write("\n")


# def convert_files(file_paths, log_file):
#     """
#     Converts each file in the provided list to mp4 using FFmpeg.
#     Converted files are saved to the 'converted_media' folder in the same directory as the script.
#     """
#     log_messages = []
#     converted_folder = Path(__file__).parent / "converted_media"
#     converted_folder.mkdir(exist_ok=True)

#     for file_path in file_paths:
#         try:
#             file_name = Path(file_path).name
#             file_prefix = Path(file_path).stem

#             # Replace spaces with underscores in the file prefix
#             file_prefix = file_prefix.replace(" ", "_")

#             output_file_path = converted_folder / f"{file_prefix}_converted.mp4"

#             start_time = time.time()

#             subprocess.run(
#                 ["ffmpeg", "-i", file_path, "-q:v", "0", output_file_path],
#                 capture_output=True,
#                 text=True,
#                 check=True,
#             )

#             duration = time.time() - start_time
#             minutes, seconds = divmod(duration, 60)

#             log_messages.append(
#                 f'"{file_name}" was converted to "{output_file_path.name}" in {minutes:.0f}m{seconds:.0f}s.'
#             )

#         except subprocess.CalledProcessError as errors:
#             log_messages.append(
#                 f'Error converting "{file_path}": {errors.stdout.strip()}'
#             )

#     # Write conversion log to the provided log file
#     log_file.write("\n".join(log_messages))
#     log_file.write("\n")


def main():
    """
    Main function to run the program.
    """
    converted_folder = Path(__file__).parent / "converted_media"
    converted_folder.mkdir(exist_ok=True)

    log_file_name = (
        converted_folder / f'conversion_log_{time.strftime("%Y%m%d_%H%M%S")}.log'
    )

    with open(log_file_name, "w", encoding="utf-8") as log_file:
        matching_files, scan_log_messages = get_matching_files("convert_media")
        log_file.write("\n".join(scan_log_messages))
        log_file.write("\n\n")

        if not matching_files:
            return

        convert_files(matching_files, log_file)

    print(f'Conversion complete. Log file saved to "{log_file_name}".')


if __name__ == "__main__":
    main()
