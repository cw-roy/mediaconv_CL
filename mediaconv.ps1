# Rebuild mediaconv.py in PowerShell

<# Test-DirectoryExistence function:

.SYNOPSIS
This function validates the existence of input and output directories.

.DESCRIPTION
The Test-DirectoryExistence function checks whether the specified input and output directories exist. If either directory does not exist, it raises a System.IO.FileNotFoundException with a custom error message.

.PARAMETER inputDirectory
The path to the input directory that you want to validate.

.PARAMETER outputDirectory
The path to the output directory that you want to validate.

.EXAMPLE
Test-DirectoryExistence -inputDirectory "C:\Input" -outputDirectory "D:\Output"

This example validates the existence of "C:\Input" and "D:\Output" directories. If either directory does not exist, an exception is raised.

#>

function Test-DirectoryExistence {
    param (
        [string] $inputDirectory,
        [string] $outputDirectory
    )

    if (-not (Test-Path -Path $inputDirectory -PathType Container)) {
        throw [System.IO.FileNotFoundException]::new("Input directory '$inputDirectory' not found.")
    }

    if (-not (Test-Path -Path $outputDirectory -PathType Container)) {
        throw [System.IO.FileNotFoundException]::new("Output directory '$outputDirectory' not found.")
    }
}
