#!/usr/bin/env python3

"""Make a better docstring"""

import os
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

    if not matching_files:
        log_messages.append("No matching files found in directory.")
        return None, log_messages

    non_matching_files = [f for f in os.listdir("convert_media") if f not in matching_files]
    if non_matching_files:
        log_messages.append(
            f'The following files were found but not matched: {", ".join(non_matching_files)}'
        )

    return matching_files, log_messages


def convert_files(file_paths):
    """
    Converts each file in the provided list to mp4 using FFmpeg.
    Converted files are saved to a new 'converted' directory in the parent folder.
    """
    log_messages = []
    parent_folder = os.path.abspath(os.path.join(os.getcwd(), ".."))
    converted_folder = os.path.join(parent_folder, "converted")
    os.makedirs(converted_folder, exist_ok=True)

    for file_path in file_paths:
        try:
            file_name = os.path.basename(file_path)
            file_prefix, _ = os.path.splitext(file_name)
            output_file_path = os.path.join(converted_folder, file_prefix + ".mp4")

            subprocess.run(
                ["ffmpeg", "-i", file_path, "-q:v", "0", output_file_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )

            log_messages.append(
                f'"{file_name}" was converted to "{os.path.basename(output_file_path)}"'
            )

        except subprocess.CalledProcessError as e:
            log_messages.append(f'Error converting "{file_path}": {e.output.decode()}')

    return log_messages


def main():
    """
    Main function to run the program.
    """
    log_file_name = f'conversion_log_{time.strftime("%Y%m%d_%H%M%S")}.txt'

    with open(log_file_name, "w", encoding="utf-8") as log_file:
        matching_files, scan_log_messages = scan_directory()
        log_file.write("\n".join(scan_log_messages))
        log_file.write("\n\n")

        if not matching_files:
            return

        conversion_log_messages = convert_files(matching_files)
        log_file.write("\n".join(conversion_log_messages))

    print(f'Conversion complete. Log file saved to "{log_file_name}".')


if __name__ == "__main__":
    main()
