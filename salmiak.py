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


def renameFiles(rootdir, dryrun=False):
    ''' Will traverse the directory and find all folders and files that can be
        renamed to a movie name.

        Parameters
        ----------
        rootdir : Where to start the search
        dryrun  : If True, do not execute. Just scan and show what the expected
                  result would be

    '''
    # First pass. Rename files
    # We start from root and work ourself down the subdirectories.
    for dir_path, subpaths, files in os.walk(rootdir):
        for file in files:
            # Extract the extention of the file so we can pick the ones we want
            extension = os.path.splitext(file)[1].lower()
            # Select the files we are intrested in
            if extension in ['.mkv', '.mp4', '.avi', '.mov']:
                # Check if we are doing a dry run
                if dryrun:
                    # Dry run. Only print out the result. DON'T rename
                    print('Decoding: ' + file)
                    print(guessit(file)['title'] + ' (' + str(guessit(file)['year']) + ')')
                else:
                    # We can rename. Guess the name and rename.
                    new_name = guessit(file)['title'] + ' (' + str(guessit(file)['year']) + ')'
                    src = dir_path + '/' + file
                    dest = dir_path + '/' + new_name+extension
                    os.rename(src, dest)

    # Second pass, rename the folders
    for dir_path, subpaths, files in os.walk(rootdir):
        for path in subpaths:
            # Only match on directories that start with a Word.
            # This to avoid some system directories (Like .git, @EAB and so on)
            if re.match('^\W.*', path) is None:
                # Dry run or not?
                if dryrun:
                    print('Decoding: ' + path)
                    new_name = guessit(path)['title'] + ' (' + str(guessit(path)['year']) + ')'
                    src = dir_path + path
                    dest = dir_path + new_name
                    print('Path source: ' + src)
                    print('Path destination: ' + dest)
                else:
                    new_name = guessit(path)['title'] + ' (' + str(guessit(path)['year']) + ')'
                    src = dir_path + '/' + path
                    dest = dir_path + '/' + new_name
                    os.rename(src, dest)
            else:
                # Let's assume this isn't a folder we are intrested in
                print('This folder is not a movie folder, I guess.. : ' + path)


if __name__ == "__main__":

    # Setup the Argument Parser
    parser = argparse.ArgumentParser(description='Rename files and folders to fit Plex')
    parser.add_argument('media', help='Where your mediafiles are')
    parser.add_argument('-d', '--dryrun', action='store_true', help='Print out the changes without actually doing them')
    args = parser.parse_args()
    renameFiles(rootdir=args.media, dryrun=args.dryrun)
