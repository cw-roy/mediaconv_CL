# mediaconv_CL:  Command line version of Python FFMpeg media converter

## Basic instructions

* Gather files to be converted and load into the 'convert_media' folder
* 'main.py' will scan that folder for compatible file types and begin the process.
* The .mp4 version of the file will be written to 'converted_media', with '_converted' appended to the file prefix.
* A timestamped log file detailing files found, files converted, and duration of each conversion will be saved with the files.

## Note

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
