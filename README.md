# Video File Converter using FFmpeg

This Python script allows you to convert video files to the .mp4 format using FFmpeg. It scans a specified directory for video files, checks their convertibility using FFmpeg, and converts them to .mp4 format if possible.

## Prerequisites

- **Python 3.x**
  - I have only tested on **_Linux_** with Python 3.9.5.  (I will eventually test on Windows and later versions of Python.  Feedback welcome.)
  - In this iteration, only Python built-ins are required.  
- **FFmpeg**
  - Tested using FFmpeg 4.2.7-0ubuntu0.1
- **venv**
  - I recommend running this in a Python virtual enviroment.  See [Python3 'venv' documentation](https://docs.python.org/3.9/library/venv.html#module-venv) for instructions.

## Setup

1. Clone this repository

2. Make sure you have Python 3.x installed. (`python --version`)

3. Make sure FFmpeg is installed and accessible via the command line. You can install it using the package manager of your operating system or visit <https://ffmpeg.org/>

## Usage

1. Place the video files you want to convert into a directory named `convert_media` in the same directory as the `main.py` script.

2. Open a terminal and navigate to the directory containing the script.

3. Run the following command to start the conversion process:

   ```bash
   #!/bin/bash
   python3 main.py
   ```

4. The script will scan the `convert_media` directory for video files. It will check each file's convertibility and convert eligible files to .mp4 format using FFmpeg.

5. After the conversion process is complete, a log file named `conversion_log_<timestamp>.log` will be created in the `converted_media` directory. The log file contains information about the conversion process, including any errors encountered.

6. The converted video files will be saved in the `converted_media` directory.

7. You can review the log file to check the status of each conversion.

Note: If the `convert_media` directory does not exist or no eligible video files are found, the script will exit without performing any conversions.

## License

This project is licensed under the MIT License. Feel free to modify and use it according to your needs.

Please note that FFmpeg is a separate software and follows its own licensing terms. Make sure to comply with FFmpeg's licensing when using it for video conversion.

## Acknowledgments

This script was created using Python 3.x and relies on the FFmpeg tool for video conversion. Thanks to the developers of Python and FFmpeg for their fantastic work.

## Disclaimer

The script is provided as-is without any warranty. Use it at your own risk. Make sure to test it thoroughly and backup your data before performing any conversions. The author is not responsible for any loss or damage caused by the usage of this script.
