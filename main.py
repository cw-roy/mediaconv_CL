#!/usr/bin/env python3

"""Converts video files to .mp4 using FFmpeg."""

import os
import subprocess
import time
from pathlib import Path


def scan_directory():
    """
    Scans the "convert_media" directory for files to be converted to .mp4 using FFmpeg.
    Returns a list of matching file paths.
    """
    log_messages = []
    matching_files = []

    for file_name in os.scandir("convert_media"):
        if file_name.is_file():
            if check_file_convertibility(file_name.path):
                matching_files.append(file_name.path)
            else:
                log_messages.append(
                    f'"{file_name.name}" cannot be converted to .mp4.'
                )
        else:
            log_messages.append(f'"{file_name.name}" is not a file.')

    if not matching_files:
        log_messages.append("No matching files found in directory.")
        return None, log_messages

    return matching_files, log_messages


def check_file_convertibility(file_path):
    """
    Checks if a file can be converted to .mp4 using FFmpeg by probing its format.
    Returns True if the file is convertible, False otherwise.
    """
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream=codec_name",
                "-of",
                "csv=p=0",
                file_path,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        codec_name = result.stdout.strip()

        # FFmpeg can convert any file with a video codec to .mp4
        return codec_name != ""

    except subprocess.CalledProcessError:
        return False


def get_file_size(file_size):
    """
    Converts the given file size in bytes to a human-readable format (e.g., KB, MB, GB).
    Returns a string representing the human-readable file size.
    """
    for unit in ["B", "KB", "MB", "GB"]:
        if file_size < 1024.0:
            return f"{file_size:.1f} {unit}"
        file_size /= 1024.0


def convert_files(file_paths, log_file):
    """
    Converts each file in the provided list to mp4 using FFmpeg.
    Args:
        file_paths (list): A list of file paths to convert.
        log_file (file): The log file to write conversion logs to.
    """
    log_file.write("Conversion Log\n")
    log_file.write("-----------------\n\n")

    converted_folder = Path(__file__).parent / "converted_media"
    converted_folder.mkdir(exist_ok=True)

    start_time = time.time()  # Add start time for the entire conversion process

    original_total_size = 0
    final_total_size = 0

    for file_path in file_paths:
        try:
            file_name = Path(file_path).name
            file_prefix = Path(file_path).stem

            file_prefix = file_prefix.replace(" ", "_")

            original_file_size = os.path.getsize(file_path)
            original_total_size += original_file_size

            counter = 1
            output_file_path = converted_folder / f"{file_prefix}_converted.mp4"
            while output_file_path.exists():
                output_file_path = (
                    converted_folder / f"{file_prefix}_converted_{counter}.mp4"
                )
                counter += 1

            subprocess.run(
                ["ffmpeg", "-i", file_path, "-q:v", "0", output_file_path],
                capture_output=True,
                text=True,
                check=True,
            )

            new_file_size = os.path.getsize(output_file_path)
            final_total_size += new_file_size

            elapsed_time = time.time() - start_time  # Calculate the elapsed time
            minutes, seconds = divmod(elapsed_time, 60)

            log_message = (
                f'"{file_name}" ({get_file_size(original_file_size)}) was converted to "{output_file_path.name}" '
                f"({get_file_size(new_file_size)}) in {minutes:.0f}m{seconds:.0f}s."
            )
            log_file.write(log_message + "\n")

        except subprocess.CalledProcessError as errors:
            log_file.write(f'Error converting "{file_path}": {errors.stdout.strip()}\n')

    elapsed_time = time.time() - start_time  # Calculate the elapsed time
    minutes, seconds = divmod(elapsed_time, 60)

    log_file.write("\nSummary\n")
    log_file.write("-----------------\n")
    log_file.write(f"Start Time: {time.ctime(start_time)}\n")
    log_file.write(f"End Time: {time.ctime(time.time())}\n")
    log_file.write(f"Elapsed Time: {minutes:.0f}m{seconds:.0f}s\n")
    log_file.write(f"Original total file size: {get_file_size(original_total_size)}\n")
    log_file.write(f"Final total file size: {get_file_size(final_total_size)}\n")


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
        matching_files, scan_log_messages = scan_directory()
        log_file.write("Scan Log\n")
        log_file.write("-----------------\n")
        log_file.write("\n".join(scan_log_messages))
        log_file.write("\n\n")

        if not matching_files:
            return

        convert_files(matching_files, log_file)

    print(f'\nConversion complete. Log file saved to "{log_file_name}".\n')

    # Print log file contents to the console
    with open(log_file_name, "r", encoding="utf-8") as log_file:
        print(log_file.read())


if __name__ == "__main__":
    main()
