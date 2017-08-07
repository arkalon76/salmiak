# Salmiak
A very VERY simple tool to rename all files and folders so that they play nice with Plex.

## Status
[![Build Status](https://travis-ci.org/arkalon76/salmiak.svg?branch=master)](https://travis-ci.org/arkalon76/salmiak)
[![Code Climate](https://codeclimate.com/github/arkalon76/salmiak/badges/gpa.svg)](https://codeclimate.com/github/arkalon76/salmiak)
[![Test Coverage](https://codeclimate.com/github/arkalon76/salmiak/badges/coverage.svg)](https://codeclimate.com/github/arkalon76/salmiak/coverage)


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
$ salmiak -d /path/to/movies
```

### Rename the files
```
$ salmiak /path/to/movies
```

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
