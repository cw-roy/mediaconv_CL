#!/usr/bin/env python3

"""
mediaconv.py

This script converts video files in a specified input directory to the .mp4 format using FFmpeg.
It provides a command-line interface for specifying the input and output directories, and it
logs the conversion process, including detailed information about each conversion and a summary
of the entire process.

Usage:
    python3 mediaconv.py -input <input_directory> -output <output_directory> [-c]

Required Arguments:
    - input_directory: The path to the directory containing video files to be converted.
    - output_directory: The path to the directory where converted .mp4 files will be saved.

Optional Argument:
    - -c, --console: Enable console output for logging in addition to writing logs to a file.

Example:
    python3 mediaconv.py -input /path/to/input -output /path/to/output -c

Dependencies:
    - FFmpeg: Make sure FFmpeg is installed and available in your system's PATH.

Author: [Your Name]
Date: [Date]

For more information and updates, visit the project repository: [Link to Repository]
"""

import argparse
import logging
import os
import platform
import subprocess
import sys
import time
from pathlib import Path


def setup_logger(log_directory, enable_console=False):
    """Set up the logger to write logs to a file and optionally to the console."""
    current_time = time.strftime("%Y%m%d_%H%M%S")
    # Determine the log file extension based on the platform
    if sys.platform.startswith("win"):
        log_file_extension = ".log"
    else:
        log_file_extension = ".log"

    log_file_name = f"{current_time}_conversion_log{log_file_extension}"
    log_file_path = os.path.join(log_directory, log_file_name)

    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Check if console output should be enabled
    if enable_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(formatter)
        logger = logging.getLogger()
        logger.addHandler(console_handler)

    return log_file_path


def scan_directory(input_directory):
    """Scans the input directory for files to be converted to .mp4 using FFmpeg."""
    log_messages = []
    matching_files = []

    system_platform = platform.system()

    for file_name in os.scandir(input_directory):
        if file_name.is_dir():
            continue
        if file_name.is_file():
            result, log_message = check_file_convertibility(file_name.path)
            if result:
                matching_files.append(file_name.path)
            else:
                log_messages.append(log_message)
        else:
            log_messages.append(f'"{file_name.name}" is not a file.')

    if not matching_files:
        log_messages.append("No matching files found in directory.")
        return None, log_messages

    # Normalize file paths for Windows
    if system_platform == "Windows":
        matching_files = [os.path.abspath(file) for file in matching_files]

    return matching_files, log_messages


def check_file_convertibility(file_path):
    """
    Checks if a file can be converted to .mp4 using FFmpeg by probing its
    format with ffprobe. Returns a tuple (result, log_message) where result is
    True if the file is convertible, False otherwise, and log_message contains
    error or success message.
    """
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-hide_banner",
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

        if codec_name:
            return True, f'"{file_path}" can be converted to .mp4.'
        else:
            error_output = result.stderr.strip()
            return (
                False,
                f'Problem found in "{file_path}":\n{error_output}.\nFile will not be processed.\n',
            )

    except subprocess.CalledProcessError as errors:
        error_output = errors.stderr.strip()
        return (
            False,
            f'Error checking "{file_path}":\n{error_output}.\nFile will not be processed.\n',
        )


def get_file_size(file_size):
    """
    Converts the given file size in bytes to a human-readable format (e.g., KB, MB, GB).
    Returns a string representing the human-readable file size.
    """
    for unit in ["B", "KB", "MB", "GB"]:
        if file_size < 1024.0:
            return f"{file_size:.1f} {unit}"
        file_size /= 1024.0


def convert_log_setup(output_directory):
    """Set up the logger for the conversion process and return the log file path."""
    log_file_name = (
        f'{output_directory}/conversion_log_{time.strftime("%Y%m%d_%H%M%S")}.log'
    )

    logging.basicConfig(
        filename=log_file_name,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    log_file = logging.getLogger()
    log_file.info("Conversion Log")
    log_file.info("==============================================")

    return log_file_name


def output_path(converted_folder, file_prefix):
    """Calculate the output file path based on the given file prefix and converted folder."""
    counter = 1
    output_file_path = f"{converted_folder}/{file_prefix}_converted_{counter}.mp4"
    while os.path.exists(output_file_path):
        output_file_path = f"{converted_folder}/{file_prefix}_converted_{counter}.mp4"
        counter += 1
    return output_file_path


def execute_ffmpeg(input_file, output_file):
    """Run FFmpeg to convert an input file to .mp4 format."""
    system_platform = platform.system()

    # Use platform-specific FFmpeg executable name
    ffmpeg_executable = "ffmpeg.exe" if system_platform == "Windows" else "ffmpeg"

    try:
        subprocess.run(
            [ffmpeg_executable, "-i", input_file, "-q:v", "0", output_file],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as errors:
        log_file = logging.getLogger()  # Get the logger again
        log_file.info('Error converting "%s": %s\n', input_file, errors.stdout.strip())


def log_info(
    file_name, original_file_size, output_file_path, new_file_size, start_time
):
    """Log information about each conversion, such as file names, sizes, and conversion time."""
    elapsed_time = time.time() - start_time  # Calculate the elapsed time
    minutes, seconds = divmod(elapsed_time, 60)

    log_file = logging.getLogger()  # Get the logger

    log_file.info(
        '"%s" (%s) was converted to "%s" (%s) in %.0fm%.0fs.\n',
        file_name,
        get_file_size(original_file_size),
        Path(output_file_path).name,
        get_file_size(new_file_size),
        minutes,
        seconds,
    )


def summary_info(start_time, original_total_size, final_total_size):
    """Log summary information about the entire conversion process."""
    elapsed_time = time.time() - start_time  # Calculate the elapsed time
    minutes, seconds = divmod(elapsed_time, 60)

    log_file = logging.getLogger()  # Get the logger

    log_file.info("Summary")
    log_file.info("================================================")
    log_file.info("Start Time: %s", time.ctime(start_time))
    log_file.info("End Time: %s", time.ctime(time.time()))
    log_file.info("Elapsed Time: %dm%ds", minutes, seconds)
    log_file.info("Original total file size: %s", get_file_size(original_total_size))
    log_file.info("Final total file size: %s", get_file_size(final_total_size))


def convert_files(file_paths, output_directory):
    """Converts each file in the input directory to .mp4, using FFmpeg."""
    converted_folder = output_directory

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

            output_file_path = output_path(converted_folder, file_prefix)

            execute_ffmpeg(file_path, output_file_path)

            new_file_size = os.path.getsize(output_file_path)
            final_total_size += new_file_size

            # Call log_info to log information about this conversion
            log_info(
                file_name,
                original_file_size,
                output_file_path,
                new_file_size,
                start_time,
            )

        except FileNotFoundError:
            log_file = logging.getLogger()  # Get the logger again
            log_file.error('File not found: "%s"\n', file_path)
        except subprocess.CalledProcessError as err:
            log_file = logging.getLogger()  # Get the logger again
            log_file.error('Error converting "%s": %s\n', file_path, err)

    # After processing all files, log the summary
    summary_info(start_time, original_total_size, final_total_size)


def main():
    """Main function to run the program."""
    parser = argparse.ArgumentParser(
        description="Convert video files to .mp4 using FFmpeg."
    )
    parser.add_argument("-input", required=True, help="Path to the input directory")
    parser.add_argument("-output", required=True, help="Path to the output directory")
    parser.add_argument(
        "-c",
        "--console",
        action="store_true",
        help="Enable console output",
        default=False,
    )
    args = parser.parse_args()

    input_directory = args.input
    output_directory = args.output

    # Call setup_logger with the log directory path and the enable_console flag
    log_file_name = setup_logger(output_directory, enable_console=args.console)

    matching_files, scan_log_messages = scan_directory(input_directory)

    log_file_name = os.path.join(output_directory, "conversion_log.log")
    log_file = logging.getLogger("mediaconv")
    log_file.info("Scan Log")
    log_file.info("================================================")
    log_file.info("\n".join(scan_log_messages))
    log_file.info("\n")

    if not matching_files:
        return

    convert_files(matching_files, output_directory)

    print(f'\nConversion complete. Log file saved to "{log_file_name}".\n')


if __name__ == "__main__":
    main()
