# File-Utility-Scripts
A collection of small cross platform scripts for various file handling tasks.

## datetime-filenames
```
usage: datetime-filenames.py [-h] [-n] [--offset OFFSET] [--allfiles] path

Rename JPEG picture files to their internal EXIF date/time

positional arguments:
  path             Relative or full path to a folder with picture files

optional arguments:
  -h, --help       show this help message and exit
  -n, --rename     Rename files instead of showing filenames
  --offset OFFSET  Offset in minutes (positive or negative) that will be added
                   to date/time found in files
  --allfiles       Include all files instead of only files with JPEG extension
```

## find-file-doublets
```
usage: find-file-doublets.py [-h] [-r] [-v] [--match PATTERN] [--matchnot]
                             [--matchout STRING]
                             path [path ...]

Searches a number of paths for multiple occurrences of the same files

positional arguments:
  path               A number of paths to search for doublet files

optional arguments:
  -h, --help         show this help message and exit
  -r, --recursive    Include subdirectories
  -v, --verbose      Output all directory names for progress purpose
  --match PATTERN    Output a list of doublet files matching shell style
                     wildcards in PATTERN
  --matchnot         Change the output of match list to doublet files not
                     matching PATTERN
  --matchout STRING  Format output of match list. Include FILENAME as
                     placeholder for doublet file in STRING
```

## verify-backup
```
usage: verify-backup.py [-h] [-r] [-t] [-v] [-x pattern]
                        original_dir backup_dir

This utility will read all files from a backup and compare them to the
original files. Non-identical, missing or excess files will be reported. A
successful run will verify that all files are in a readable condition. File
system errors will be reported. All filename comparisons are case sensitive.

positional arguments:
  original_dir     Original directory
  backup_dir       Backup directory

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Include subdirectories
  -t, --timediff   Report if modification time differs for identical files
  -v, --verbose    Output all directory names for progress purpose
  -x pattern       Quoted wildcards for file or directory exclusion
```
