# mediaconv_CL:  Command line version of Python FFMpeg media converter

**Video File Conversion Script**

The video file conversion script is a tool that allows you to convert various video file formats into the popular .mp4 format using the FFmpeg library. It simplifies the process of converting multiple video files in a directory and keeps track of the conversion progress.

**How it works:**

1. The script scans a specified directory called "convert_media" and identifies video files with supported formats such as .mp4, .mkv, .mov, .avi, and more.

2. Once the video files are identified, the script utilizes the FFmpeg library to convert each video file to the .mp4 format. The converted files are saved in a new folder named "converted_media," located in the same directory as the script.

3. During the conversion process, the script records important information such as the original file name, the converted file name, and the time taken for each conversion.

4. Additionally, the script generates a log file named "conversion_log_<timestamp>.log" in the "converted_media" folder. The log file contains details about the conversion process, including any errors that occurred during conversion.

**Usage:**

1. Place the video files you want to convert into the "convert_media" folder.

2. Run the script, and it will automatically convert the video files to the .mp4 format using FFmpeg.

3. After the conversion process is complete, a log file will be generated in the "converted_media" folder. This log file contains information about each conversion, including any errors encountered.

4. The converted video files will be available in the "converted_media" folder for further use.

---

## Notes

* Tested on Linux only, up to this point.
* Written in Python 3.9

### Currently supported file types are

* ".mp4",
* ".mkv",
* ".mov",
* ".avi",
* ".3gp",
* ".flv",
* ".mk4",
* ".mpg",
