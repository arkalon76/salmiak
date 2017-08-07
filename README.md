# Salmiak
Salmiak is the Nokia 3310 of file renaming apps.

A very VERY simple tool to rename all files and folders so that they play nice with Plex. There are many tools like this, however, Salmiak tries to remove complexity by just offering the basics.

## Status
![Build Status](https://travis-ci.org/arkalon76/salmiak.svg?branch=master)
[![Code Climate](https://codeclimate.com/github/arkalon76/salmiak/badges/gpa.svg)](https://codeclimate.com/github/arkalon76/salmiak)
[![Coverage Status](https://coveralls.io/repos/github/arkalon76/salmiak/badge.svg?branch=master)](https://coveralls.io/github/arkalon76/salmiak?branch=master)


## How to install
```
$ pip install salmiak
```
If you get a permissions error then run the following command instead
```
$ sudo -H pip install salmiak
```

## How to use?

### Dry run (Don't change the files)
```
$ salmiak -d /path/to/media_files
```

### Rename the files
```
$ salmiak /path/to/media_files
```
### Limitations
TV Shows are still in somewhat of a beta. I've not tested this very well so please submit any filenames that you would like to add to my test for support.
__Note:
I only support TV Show files right now. Folders are bit tricky so I need to give that a bit more thought before I can support it__

### Help!
```
$ python salmiak.py -h
usage: salmiak.py [-h] [-d] media

Rename files and folders to fit Plex

positional arguments:
  media         Where your mediafiles are

optional arguments:
  -h, --help    show this help message and exit
  -d, --dryrun  Print out the changes without actually doing them
```
