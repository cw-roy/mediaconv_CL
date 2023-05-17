#!/usr/bin/env python3

"""Converts video files to .mp4 using FFmpeg."""

import os
import subprocess
import time
import asyncio
import concurrent.futures
from pathlib import Path


async def scan_directory(queue):
    """
    Scans the "convert_media" directory for files to be converted to .mp4 using FFmpeg.
    Adds matching file paths to the conversion queue.
    """
    for file_name in os.scandir("convert_media"):
        if file_name.is_file() and check_file_convertibility(file_name.path):
            await queue.put(file_name.path)


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


async def convert_file(file_path, log_file_name):
    """
    Converts a single file to mp4 using FFmpeg.
    Returns the log message for the conversion.
    """
    try:
        file_name = Path(file_path).name
        file_prefix = Path(file_path).stem.replace(" ", "_")

        converted_folder = Path(__file__).parent / "converted_media"
        converted_folder.mkdir(exist_ok=True)

        counter = 1
        output_file_path = converted_folder / f"{file_prefix}_converted.mp4"
        while output_file_path.exists():
            output_file_path = (
                converted_folder / f"{file_prefix}_converted_{counter}.mp4"
            )
            counter += 1

        start_time = time.time()

        await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-i",
            file_path,
            "-q:v",
            "0",
            output_file_path,
        ).communicate()

        duration = time.time() - start_time
        minutes, seconds = divmod(duration, 60)

        log_message = (
            f'"{file_name}" was converted to "{output_file_path.name}" '
            f"in {minutes:.0f}m{seconds:.0f}s."
        )

        # Write log message to the file
        async with await asyncio.to_thread(open, log_file_name, "a", encoding="utf-8"):
            await log_file.write(log_message + "\n")

    except subprocess.CalledProcessError as errors:
        log_message = f'Error converting "{file_path}": {errors.stdout.strip()}'
        # Write log message to the file
        async with await asyncio.to_thread(open, log_file_name, "a", encoding="utf-8"):
            await log_file.write(log_message + "\n")


async def process_conversion_queue(queue, log_file_name):
    """
    Processes the conversion queue using multiprocessing.
    """
    with concurrent.futures.ProcessPoolExecutor() as executor:
        loop = asyncio.get_event_loop()

        while not queue.empty():
            file_path = await queue.get()
            await loop.run_in_executor(
                executor, convert_file, file_path, log_file_name
            )
            queue.task_done()

async def main():
    """
    Main function to run the program.
    """
    converted_folder = Path(__file__).parent / "converted_media"
    converted_folder.mkdir(exist_ok=True)

    log_file_name = (
        converted_folder / f'conversion_log_{time.strftime("%Y%m%d_%H%M%S")}.log'
    )

    # Open the log file in the main process
    log_file = await asyncio.to_thread(open, log_file_name, "w", encoding="utf-8")

    queue = asyncio.Queue()

    # Start the conversion queue processing
    conversion_task = asyncio.create_task(process_conversion_queue(queue, log_file_name))

    # Scan the directory and add files to the conversion queue
    await scan_directory(queue)

    # Wait for all conversions to complete
    await queue.join()

    # Close the log file in the main process
    await asyncio.to_thread(log_file.close)

    print(f'Conversion complete. Log file saved to "{log_file_name}".')


if __name__ == "__main__":
    asyncio.run(main())
