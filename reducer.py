import os
import subprocess


def reduce_video_size(input_file, output_file, max_file_size_mb):
    """
    Reduce the size of a video file to meet a specified maximum file size.

    Parameters:
    - input_file (str): Path to the input video file.
    - output_file (str): Path to the output video file.
    - max_file_size_mb (int): Desired maximum file size in megabytes.
    """
    # Get current video file size and resolution
    current_file_size_mb = get_file_size_mb(input_file)
    original_resolution = get_video_resolution(input_file)

    # Check if resolution is higher than 720p, reduce to 720p if needed
    if original_resolution[0] > 1280 or original_resolution[1] > 720:
        output_resolution = (1280, 720)  # Set the desired resolution
    else:
        output_resolution = original_resolution

    # Calculate the target bitrate to achieve the desired file size
    target_bitrate = calculate_target_bitrate(
        current_file_size_mb, max_file_size_mb, input_file, output_resolution
    )

    # Run FFMpeg command to reduce file size
    ffmpeg_command = f"ffmpeg -i {input_file} -s {output_resolution[0]}x{output_resolution[1]} -b:v {target_bitrate}k {output_file}"
    subprocess.run(ffmpeg_command, shell=True)


def get_file_size_mb(file_path):
    """
    Get the file size of a given file in megabytes.

    Parameters:
    - file_path (str): Path to the file.

    Returns:
    - float: File size in megabytes.
    """
    return os.path.getsize(file_path) / (1024 * 1024)


def get_video_resolution(file_path):
    """
    Get the resolution of a video file using ffprobe.

    Parameters:
    - file_path (str): Path to the video file.

    Returns:
    - tuple: Width and height of the video resolution.
    """
    ffprobe_command = f"ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 {file_path}"
    result = subprocess.run(
        ffprobe_command, stdout=subprocess.PIPE, shell=True, text=True
    )
    width, height = map(int, result.stdout.strip().split("x"))
    return width, height


def calculate_target_bitrate(
    current_size_mb, target_size_mb, input_file, output_resolution
):
    """
    Calculate the target bitrate to achieve a desired file size.

    Parameters:
    - current_size_mb (float): Current file size in megabytes.
    - target_size_mb (int): Desired file size in megabytes.
    - input_file (str): Path to the input video file.
    - output_resolution (tuple): Desired output resolution (width, height).

    Returns:
    - int: Target bitrate.
    """
    bitrate_reduction_factor = target_size_mb / current_size_mb
    return int(
        bitrate_reduction_factor
        * get_video_bitrate(input_file)
        * (output_resolution[0] * output_resolution[1])
        / (1280 * 720)
    )


def get_video_bitrate(file_path):
    """
    Get the video bitrate of a video file using ffprobe.

    Parameters:
    - file_path (str): Path to the video file.

    Returns:
    - int: Video bitrate.
    """
    ffprobe_command = f"ffprobe -v error -select_streams v:0 -show_entries stream=bit_rate -of default=noprint_wrappers=1 {file_path}"
    result = subprocess.run(
        ffprobe_command, stdout=subprocess.PIPE, shell=True, text=True
    )
    return int(result.stdout.strip())


# Example usage
input_video = "input_video.mp4"
output_video = "output_video.mp4"
max_file_size_mb = 50  # Set your desired maximum file size in megabytes

reduce_video_size(input_video, output_video, max_file_size_mb)
