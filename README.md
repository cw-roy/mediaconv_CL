# Video File Converter using FFmpeg

`mediaconv.py` is a Python script that converts video files to the .mp4 format using FFmpeg. It's a command-line tool designed to simplify the conversion process. Below are instructions on how to use it effectively.

## Prerequisites

- **Python 3.x**
  - Tested on **_Linux_** with Python 3.9.5, but it should work on Windows and MacOS with later Python versions.
  - In this iteration, only Python built-ins are required - no additional modules needed.
- **FFmpeg**
  - Tested using FFmpeg 4.2.7-0ubuntu0.1
- **venv**
  - I recommend running this in a Python virtual environment. See [Python3 'venv' documentation](https://docs.python.org/3.9/library/venv.html#module-venv) for instructions.

## Setup

1. Clone this repository

2. Make sure you have Python 3.x installed. (`python --version`)

3. Make sure FFmpeg is installed and accessible via the command line. You can install it using the package manager of your operating system or visit [FFmpeg's official website](https://ffmpeg.org/).

## Usage

### Windows

1. Open Command Prompt (CMD).

2. Navigate to the directory where you saved `mediaconv.py`.

3. To convert video files in an input directory to `.mp4` format in an output directory, use the following command:

   ```bash
   python mediaconv.py -input INPUT_DIRECTORY -output OUTPUT_DIRECTORY
   ```

   Replace `INPUT_DIRECTORY` with the path to the directory containing your video files and `OUTPUT_DIRECTORY` with the path where you want to save the converted files.

4. To enable console output in addition to log files, use the `-c` flag:

   ```bash
   python mediaconv.py -input INPUT_DIRECTORY -output OUTPUT_DIRECTORY -c
   ```

### Linux and MacOS

1. Open a terminal.

2. Navigate to the directory where you saved `mediaconv.py`.

3. To convert video files in an input directory to `.mp4` format in an output directory, use the following command:

   ```bash
   python3 mediaconv.py -input INPUT_DIRECTORY -output OUTPUT_DIRECTORY
   ```

   Replace `INPUT_DIRECTORY` with the path to the directory containing your video files and `OUTPUT_DIRECTORY` with the path where you want to save the converted files.

4. To enable console output in addition to log files, use the `-c` flag:

   ```bash
   python3 mediaconv.py -input INPUT_DIRECTORY -output OUTPUT_DIRECTORY -c
   ```

#### Example

Here's an example of how to use the script:

```bash
python3 mediaconv.py -input /path/to/input/videos -output /path/to/output/videos -c
```

### Viewing Logs

After the conversion process is complete, you can find a log file named `conversion_log_<timestamp>.log` in your output directory. You can open this file to review conversion details and any error messages.

### Troubleshooting

If you encounter any issues or errors during the conversion process, check the log file for error messages. Common issues may include missing FFmpeg installation or unsupported video formats.

## License

This project is licensed under the MIT License. Feel free to modify and use it according to your needs.

Please note that FFmpeg is a separate software and follows its own licensing terms. Make sure to comply with FFmpeg's licensing when using it for video conversion.

## Acknowledgments

This script was created using Python 3.x and relies on the FFmpeg tool for video conversion. Thanks to the developers of Python and FFmpeg for their fantastic work.

## Disclaimer

The script is provided as-is without any warranty. Use it at your own risk. Make sure to test it thoroughly and backup your data before performing any conversions. The author is not responsible for any loss or damage caused by the usage of this script.

Feel free to copy and paste this updated README.md into your project's documentation.
