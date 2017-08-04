'''
MIT License

Copyright (c) 2017 Kenth Fagerlund

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import os
import sys
import argparse
import re
import configparser


from guessit import guessit


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


ACCEPTED_EXTENTIONS = ['.mkv', '.mp4', '.avi', '.mov']


def isValidMovieFile(file):
    # Extract the extention of the file so we can pick the ones we want
    extension = os.path.splitext(file)[1].lower()
    fileguess = guessit(file)
    if extension in ACCEPTED_EXTENTIONS and ('title' in fileguess) and ('year' in fileguess):
        return True
    else:
        return False


def isValidMoviePath(path):
    pathguess = guessit(path)
    if re.match('^\W.*', path) is None and ('title' in pathguess) and ('year' in pathguess):
        return True
    else:
        return False


def renameFile(dir_path, file):
    # Extract the extention of the file so we can pick the ones we want
    extension = os.path.splitext(file)[1].lower()
    print('    ' + file + bcolors.OKGREEN + ' ==> ' + bcolors.ENDC + guessit(file)['title'] + ' (' + str(guessit(file)['year']) + ')' + extension)

    if not DRYRUN:
        new_name = guessit(file)['title'] + ' (' + str(guessit(file)['year']) + ')'
        src = dir_path + '/' + file
        dest = dir_path + '/' + new_name + extension
        os.rename(src, dest)


def renamePath(dir_path, path):
    new_name = guessit(path)['title'] + ' (' + str(guessit(path)['year']) + ')'
    src = dir_path + path
    dest = dir_path + new_name
    print('    ' + src + bcolors.OKGREEN + ' ==> ' + bcolors.ENDC + dest)

    if not DRYRUN:
        src = dir_path + path
        dest = dir_path + new_name
        os.rename(src, dest)


def main():

    # Setup the Argument Parser
    parser = argparse.ArgumentParser(description='Rename files and folders to fit Plex')
    parser.add_argument('media', help='Where your mediafiles are')
    parser.add_argument('-d', '--dryrun', action='store_true', help='Print out the changes without actually doing them')
    args = parser.parse_args()

    # Extract the rootpath
    rootdir = args.media

    global DRYRUN
    DRYRUN = args.dryrun

    # Warn the user if it's a dry run
    if DRYRUN:
        print('\n')
        print(bcolors.UNDERLINE + 'NOTE: This is a dry run!' + bcolors.ENDC)
        print('\n')

    # First pass. Rename files
    # We start from root and work ourself down the subdirectories.
    print(bcolors.BOLD + '= Working my way through the files =' + bcolors.ENDC)
    for dir_path, subpaths, files in os.walk(rootdir):
        for file in files:
            if isValidMovieFile(file):
                renameFile(dir_path, file)
            else:
                pass

    # Second pass, rename the folders
    print(bcolors.BOLD + '\n= Working my way through the folders =' + bcolors.ENDC)
    for dir_path, subpaths, files in os.walk(rootdir):
        for path in subpaths:
            # Only match on directories that start with a Word.
            # This to avoid some system directories (Like .git, @EAB and so on)
            if isValidMoviePath(path):
                renamePath(dir_path, path)
            else:
                # Let's assume this isn't a folder we are intrested in
                print(bcolors.FAIL + '    ' + path + bcolors.ENDC + ' <== What is this path? Really a Movie?')
