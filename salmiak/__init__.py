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
    """ Allows for us to give some colour to the output text
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


ACCEPTED_EXTENTIONS = ['.mkv', '.mp4', '.avi', '.mov']


def printInfoMessage(message):
    """ Prints out a information message for the user

        Parameters:
        -----------
        message: Message to be displayed to the user
    """
    print(bcolors.HEADER + message + bcolors.ENDC)


def printFailureMessage(message):
    """ Prints out a error message for the user

        Parameters:
        -----------
        message: Message to be displayed to the user
    """
    print(bcolors.FAIL + '    ' + 'Warning: ' + bcolors.ENDC + message)


def parseFiles(rootdir):
    """ Will walk all the files under rootdir and, if valid, rename them.
        If Dry run flag is set then we will only print out, not actually rename.

        Parameters:
        -----------
        rootdir: The directory from where we start the walk.
    """
    # First pass. Rename files
    # We start from root and work ourself down the subdirectories.
    printInfoMessage('= Working my way through the files =')
    for dir_path, subpaths, files in os.walk(rootdir):
        for file in files:
            if isValidPath(dir_path + '/' + file):
                renameFile(dir_path, file)
            else:
                # Let's assume this isn't a folder we are intrested in
                printFailureMessage(file + ' <== What is this file? Is it really a movie?')

    printInfoMessage('\n= Working my way through the folders =')
    for dir_path, subpaths, files in os.walk(rootdir):
        for path in subpaths:
            # Only match on directories that start with a Word.
            # This to avoid some system directories (Like .git, @EAB and so on)
            if isValidPath(path):
                renamePath(dir_path, path)
            else:
                # Let's assume this isn't a folder we are intrested in
                printFailureMessage(file + ' <== Is this really a movie folder?')


def isValidPath(path):
    """ Validates a path to make sure that it can be converted to a Title (year) format.

        Parameters:
        -----------
        path: The full path to the folder or file
    """
    if os.path.isfile(path):
        # Extract the filename from the path
        filename = os.path.basename(path)
        # Extract the extention from the filename
        extension = os.path.splitext(filename)[1].lower()
        # Let's see if we can get the title and year from the filename
        fileguess = guessit(filename)
        if extension in ACCEPTED_EXTENTIONS and ('title' in fileguess) and ('year' in fileguess):
            return True
        else:
            return False
    else:
        foldername = os.path.basename(path)
        pathguess = guessit(foldername)
        if re.match('^\W.*', foldername) is None and ('title' in pathguess) and ('year' in pathguess):
            return True
        else:
            return False


def buildPlexMovieName(guessDict):
    return guessDict['title'] + ' (' + str(guessDict['year']) + ')'

#  Stephen.Colbert.2017.04.21.Rosario.Dawson.720p.HDTV.x264-SORNY[rarbg].mkv
def buildPlexTVShowName(guessDict):
    if 'season' in guessDict:
        return guessDict['title'] + ' - ' + 'S' + str(guessDict['season']) + 'E' + str(guessDict['episode'])
    elif 'year' in guessDict:
        title = guessDict['title']
        year = ' (' + str(guessDict['year']) + ') - '
        season = 'S' + str(guessDict['season']) if 'season' in guessDict else ''
        episode = 'E' + str(guessDict['episode']) if 'episode' in guessDict else ''
        ep_title = ' - ' + guessDict['episode_title'] if 'episode_title' in guessDict  else ''
        return title + year + season + episode + ep_title
    elif 'date' in guessDict:
        title = guessDict['title'] + ' - '
        date = str(guessDict['date'])
        season = ' - ' + 'S' + str(guessDict['season']) if 'season' in guessDict else ''
        episode = 'E' + str(guessDict['episode']) if 'episode' in guessDict else ''
        ep_title = ' - ' + guessDict['episode_title'] if 'episode_title' in guessDict  else ''
        return title + date + season + episode + ep_title
    else:
        printFailureMessage('Hmm. This show format is unknown to me. Report to https://github.com/arkalon76/salmiak/issues')


namebuilder = {
        'movie': buildPlexMovieName,
        'episode': buildPlexTVShowName,
}


def renameFile(dir_path, file):
    """ Renames a file to match a standard Plex format { Title (year) }.
        If the Dry run flag is set then we will just print the text but not make the move.

        Parameters:
        -----------
        dir_path: Full path to the file
        file:     File name
    """

    # Extract the extention of the file so we can pick the ones we want
    extension = os.path.splitext(file)[1].lower()
    myguess = guessit(file)
    print('    ' + file + bcolors.OKGREEN + ' ==> ' + bcolors.ENDC + namebuilder[myguess['type']](myguess) + extension)
    if not DRYRUN:
        new_name = namebuilder[myguess['type']](myguess)
        src = dir_path + '/' + file
        dest = dir_path + '/' + new_name + extension
        os.rename(src, dest)


def renamePath(dir_path, path):
    """ Renames a folder to match a standard Plex format { Title (year) }.
        If the Dry run flag is set then we will just print the text but not make the move.

        Parameters:
        -----------
        dir_path: Full path to the related folder
        path:     Folder name
    """
    new_name = guessit(path)['title'] + ' (' + str(guessit(path)['year']) + ')'
    src = dir_path + '/' + path
    dest = dir_path + '/' + new_name
    print('    ' + src + bcolors.OKGREEN + ' ==> ' + bcolors.ENDC + dest)

    if not DRYRUN:
        os.rename(src, dest)


def main():
    """ Here is where the magic happens
    """

    # Setup the Argument Parser
    parser = argparse.ArgumentParser(description='Rename files and folders to fit Plex')
    parser.add_argument('media', help='Where your mediafiles are')
    parser.add_argument('-d', '--dryrun', action='store_true', help='Print out the changes without actually doing them')
    args = parser.parse_args()

    # Extract the rootpath
    rootdir = args.media

    # Set if we are doing a dry run our not
    global DRYRUN
    DRYRUN = args.dryrun

    # Warn the user if it's a dry run
    if DRYRUN:
        print('\n')
        print(bcolors.UNDERLINE + 'NOTE: This is a dry run!' + bcolors.ENDC)
        print('\n')

    # Walk through the root dir and look at all the files
    parseFiles(rootdir)
    # Walk through the root dir and look at all the folders
    # parseFolders(rootdir)
