import pytest
import salmiak
import os


@pytest.mark.parametrize("test_file,expected", [
    ('Kimi.no.na.wa.aka.Your.Name.2016.JAPANESE.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1-FGT.mkv', True),
    ('Looney.Tunes.Volume.2.1936-1959.1080p.BluRay.REMUX.AVC.DD1.0-RARBG.mkv', True),
    ('The.Princess.And.The.Frog.2009.1080p.BluRay.AVC.DTS-HD.MA.5.1-FGT.mkv', True),
    ('Vaid.name.but.no.mkv.extention.2017', False),
    ('Random.Bullshit.without.year.mkv', False),
    ('.git.filename', False)
])


def test_valid_filename(test_file, expected, tmpdir):
    f1 = tmpdir.mkdir('download').join(test_file)
    f1.write('VideoContent')
    assert salmiak.isValidPath(str(f1)) == expected


@pytest.mark.parametrize("test_path, expected", [
    ('Name.2001', True),
    ('Looney.Tunes.Volume.2.1936-1959.1080p.BluRay.REMUX.AVC.DD1.0-RARBG', True),
    ('@download', False),
    ('Movie.Title', False),
    ('.ssh.2001', False),
    ('Brother.Where.Art.Thou.2000.1080p.BluRay.X264-AMIABLE', True),
    ('.Brother.Where.Art.Thou.2000.1080p.BluRay.X264-AMIABLE', False)
])


def test_valid_path(test_path, expected, tmpdir):
    f1 = tmpdir.mkdir(test_path)
    assert salmiak.isValidPath(str(f1)) == expected


@pytest.mark.parametrize("test_file, renamed_file", [
    ('Kimi.no.na.wa.aka.Your.Name.2016.JAPANESE.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1-FGT.mkv', 'Kimi no na wa aka Your Name (2016).mkv'),
    ('The.Princess.And.The.Frog.2009.1080p.BluRay.AVC.DTS-HD.MA.5.1-FGT.mkv', 'The Princess And The Frog (2009).mkv'),
])


def test_rename_file(test_file, renamed_file, tmpdir):
    ''' Testing that renaming a valid file actually moves it from one to the other.
    '''
    salmiak.DRYRUN = False
    f1 = tmpdir.mkdir('download').join(test_file)
    f1.write('VideoContent')
    salmiak.renameFile(str(tmpdir) + '/download', str(test_file))
    assert os.path.isfile(str(tmpdir) + '/download/' + renamed_file) is True
    assert os.path.isfile(str(tmpdir) + '/download/' + test_file) is False


@pytest.mark.parametrize("test_file, renamed_file", [
    ('Kimi.no.na.wa.aka.Your.Name.2016.JAPANESE.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1-FGT.mkv', 'Kimi no na wa aka Your Name (2016).mkv'),
    ('The.Princess.And.The.Frog.2009.1080p.BluRay.AVC.DTS-HD.MA.5.1-FGT.mkv', 'The Princess And The Frog (2009).mkv'),
])


def test_dryrun_rename_file(test_file, renamed_file, tmpdir):
    ''' Dry run should not move the files
    '''
    salmiak.DRYRUN = True
    f1 = tmpdir.mkdir('download').join(test_file)
    f1.write('VideoContent')
    salmiak.renameFile(str(tmpdir) + '/download', str(test_file))
    assert os.path.isfile(str(tmpdir) + '/download/' + renamed_file) is False
    assert os.path.isfile(str(tmpdir) + '/download/' + test_file) is True


@pytest.mark.parametrize("test_folder, renamed_folder", [
    ('Kimi.no.na.wa.aka.Your.Name.2016.JAPANESE.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1-FGT', 'Kimi no na wa aka Your Name (2016)'),
    ('The.Princess.And.The.Frog.2009.1080p.BluRay.AVC.DTS-HD.MA.5.1-FGT', 'The Princess And The Frog (2009)'),
])


def test_rename_folder(test_folder, renamed_folder, tmpdir):
    ''' Testing that renaming a valid file actually moves it from one to the other.
    '''
    salmiak.DRYRUN = False
    f1 = tmpdir.mkdir(test_folder)
    salmiak.renamePath(str(tmpdir), str(test_folder))
    assert os.path.isdir(str(tmpdir) + '/' + renamed_folder) is True
    assert os.path.isdir(str(tmpdir) + '/' + test_folder) is False


@pytest.mark.parametrize("test_folder, renamed_folder", [
    ('Kimi.no.na.wa.aka.Your.Name.2016.JAPANESE.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1-FGT', 'Kimi no na wa aka Your Name (2016)'),
    ('The.Princess.And.The.Frog.2009.1080p.BluRay.AVC.DTS-HD.MA.5.1-FGT', 'The Princess And The Frog (2009)'),
])


def test_dryrun_rename_folder(test_folder, renamed_folder, tmpdir):
    ''' Testing that renaming a valid file actually moves it from one to the other.
    '''
    salmiak.DRYRUN = True
    f1 = tmpdir.mkdir(test_folder)
    salmiak.renamePath(str(tmpdir), str(test_folder))
    assert os.path.isdir(str(tmpdir) + '/' + renamed_folder) is False
    assert os.path.isdir(str(tmpdir) + '/' + test_folder) is True


################
# Test TVShows #
################


@pytest.mark.parametrize("test_tvshow_file, renamed_file", [
    ('Last.Week.Tonight.with.John.Oliver.S04E13.720p.HBO.WEBRip.AAC2.0.H264-monkee[rarbg].mkv', 'Last Week Tonight with John Oliver - S4E13.mkv'),
    ('Married With Children - 0106 - Sixteen Years and What Do You Get.mkv', 'Married With Children - S1E6.mkv'),
    ('BBC.Life.2009.E02.Reptiles.and.Amphibians.1080p.BluRay.Remux.VC1.-HDME.mkv', 'BBC Life (2009) - E2 - Reptiles and Amphibians.mkv'),
    ('Stephen.Colbert.2017.04.21.Rosario.Dawson.720p.HDTV.x264-SORNY[rarbg].mkv', 'Stephen Colbert - 2017-04-21 - Rosario Dawson.mkv'),
    ('Westworld.S01E04.1080p.AMZN.WEBRip.DD5.1.x264-FGT.mkv', 'Westworld - S1E4.mkv'),
    ('My.Show.2023.The.Christmas.Special.1080p.mkv', 'My Show (2023) -  - The Christmas Special.mkv'), # For year+episode_title, no episode number
    ('Daily.Show.2023-10-26.Special.Guest.720p.mkv', 'Daily Show - 2023-10-26 - Special Guest.mkv') # For date-based episode
])


def test_rename_tvshows(test_tvshow_file, renamed_file, tmpdir):
    ''' Testing that renaming a valid file actually moves it from one to the other.
    '''
    salmiak.DRYRUN = False
    f1 = tmpdir.mkdir('download').join(test_tvshow_file)
    f1.write('VideoContent')
    salmiak.renameFile(str(tmpdir) + '/download', str(test_tvshow_file))
    assert os.path.isfile(str(tmpdir) + '/download/' + renamed_file) is True
    assert os.path.isfile(str(tmpdir) + '/download/' + test_tvshow_file) is False


@pytest.mark.parametrize("test_tvshow_file, renamed_file", [
    ('Last.Week.Tonight.with.John.Oliver.S04E13.720p.HBO.WEBRip.AAC2.0.H264-monkee[rarbg].mkv', 'Last Week Tonight with John Oliver - S4E13.mkv'),
    ('Married With Children - 0106 - Sixteen Years and What Do You Get.mkv', 'Married With Children - S1E6.mkv'),
    ('BBC.Life.2009.E02.Reptiles.and.Amphibians.1080p.BluRay.Remux.VC1.-HDME.mkv', 'BBC Life (2009) - E2 - Reptiles and Amphibians.mkv'),
    ('Stephen.Colbert.2017.04.21.Rosario.Dawson.720p.HDTV.x264-SORNY[rarbg].mkv', 'Stephen Colbert - 2017-04-21 - Rosario Dawson.mkv'),
    ('Westworld.S01E04.1080p.AMZN.WEBRip.DD5.1.x264-FGT.mkv', 'Westworld - S1E4.mkv'),
    ('My.Show.2023.The.Christmas.Special.1080p.mkv', 'My Show (2023) -  - The Christmas Special.mkv'), # For year+episode_title, no episode number
    ('Daily.Show.2023-10-26.Special.Guest.720p.mkv', 'Daily Show - 2023-10-26 - Special Guest.mkv') # For date-based episode
])


def test_dryrun_rename_tvshows(test_tvshow_file, renamed_file, tmpdir):
    ''' Testing that renaming a valid file actually moves it from one to the other.
    '''
    salmiak.DRYRUN = True
    f1 = tmpdir.mkdir('download').join(test_tvshow_file)
    f1.write('VideoContent')
    salmiak.renameFile(str(tmpdir) + '/download', str(test_tvshow_file))
    assert os.path.isfile(str(tmpdir) + '/download/' + renamed_file) is False
    assert os.path.isfile(str(tmpdir) + '/download/' + test_tvshow_file) is True


####################
# Test main() function #
####################

# We need argparse and patch from unittest.mock, or use mocker from pytest-mock
import argparse
from unittest.mock import patch

def test_main_parses_media_argument(mocker):
    """Test that main() correctly parses the 'media' argument."""
    # Mock sys.argv
    mocker.patch('sys.argv', ['salmiak', 'test_media_path'])
    # Mock salmiak.parseFiles to prevent it from actually running
    mocked_parse_files = mocker.patch('salmiak.parseFiles')
    
    salmiak.main()
    
    # Assert parseFiles was called with the media argument
    mocked_parse_files.assert_called_once_with('test_media_path')

def test_main_sets_dryrun_false_by_default(mocker):
    """Test that main() sets DRYRUN to False when --dryrun is not passed."""
    mocker.patch('sys.argv', ['salmiak', 'some_path'])
    mocker.patch('salmiak.parseFiles') # We don't care about its execution here
    
    # Ensure DRYRUN is not True before the call (e.g. from a previous test)
    salmiak.DRYRUN = None 
    
    salmiak.main()
    
    assert salmiak.DRYRUN is False

def test_main_sets_dryrun_true_with_argument(mocker):
    """Test that main() sets DRYRUN to True when --dryrun is passed."""
    mocker.patch('sys.argv', ['salmiak', 'some_path', '--dryrun'])
    mocker.patch('salmiak.parseFiles')
    
    salmiak.DRYRUN = None # Reset
    
    salmiak.main()
    
    assert salmiak.DRYRUN is True

def test_main_prints_dryrun_message(mocker, capsys):
    """Test that main() prints the dry run message when --dryrun is active."""
    mocker.patch('sys.argv', ['salmiak', 'some_path', '--dryrun'])
    mocker.patch('salmiak.parseFiles')
    
    salmiak.main()
    
    captured = capsys.readouterr()
    # bcolors.UNDERLINE + 'NOTE: This is a dry run!' + bcolors.ENDC
    # \033[4mNOTE: This is a dry run!\033[0m
    assert '\033[4mNOTE: This is a dry run!\033[0m' in captured.out

def test_main_calls_parsefiles(mocker):
    """Test that main() calls salmiak.parseFiles with the correct media argument."""
    test_media_dir = "/test/media/dir"
    mocker.patch('sys.argv', ['salmiak', test_media_dir])
    mock_parse_files = mocker.patch('salmiak.parseFiles')
    
    salmiak.main()
    
    mock_parse_files.assert_called_once_with(test_media_dir)

def test_main_no_dryrun_message_when_not_dryrun(mocker, capsys):
    """Test that main() does not print the dry run message when --dryrun is not active."""
    mocker.patch('sys.argv', ['salmiak', 'some_path'])
    mocker.patch('salmiak.parseFiles')

    salmiak.main()

    captured = capsys.readouterr()
    assert 'NOTE: This is a dry run!' not in captured.out


#################################
# Test printMessage functions #
#################################

def test_printInfoMessage(capsys):
    """Test that printInfoMessage prints the message with correct colors."""
    test_message = "Sample Info"
    salmiak.printInfoMessage(test_message)
    captured = capsys.readouterr()
    expected_output = salmiak.bcolors.HEADER + test_message + salmiak.bcolors.ENDC + "\n"
    assert captured.out == expected_output

def test_printFailureMessage(capsys):
    """Test that printFailureMessage prints the message with correct colors and formatting."""
    test_message = "Sample Error"
    salmiak.printFailureMessage(test_message)
    captured = capsys.readouterr()
    expected_output = salmiak.bcolors.FAIL + '    ' + 'Warning: ' + salmiak.bcolors.ENDC + test_message + "\n"
    assert captured.out == expected_output


############################
# Test parseFiles function #
############################

def test_parseFiles_invalid_subfolder_name(tmpdir, capsys):
    """Test parseFiles with an invalid subfolder name."""
    invalid_folder_name = "@@invalid_folder"
    tmpdir.mkdir(invalid_folder_name)
    
    salmiak.parseFiles(str(tmpdir))
    
    captured = capsys.readouterr()
    expected_message = salmiak.bcolors.FAIL + '    ' + 'Warning: ' + salmiak.bcolors.ENDC + invalid_folder_name + " <== Is this really a movie folder?\n"
    # Check if the specific failure message for the folder is in the output
    # The output will also contain "= Working my way through the files =" and "\n= Working my way through the folders ="
    # and potentially messages about files if any were implicitly created/found.
    # For this test, we are primarily concerned with the folder message.
    assert expected_message in captured.out

def test_parseFiles_empty_root_directory(tmpdir, capsys):
    """Test parseFiles with an empty root directory."""
    salmiak.parseFiles(str(tmpdir))
    captured = capsys.readouterr()
    
    expected_info_files = salmiak.bcolors.HEADER + "= Working my way through the files =" + salmiak.bcolors.ENDC + "\n"
    expected_info_folders = salmiak.bcolors.HEADER + "\n= Working my way through the folders =" + salmiak.bcolors.ENDC + "\n"
    
    assert expected_info_files in captured.out
    assert expected_info_folders in captured.out
    # Assert that no failure messages are present if the directory is truly empty
    assert salmiak.bcolors.FAIL not in captured.out

def test_parseFiles_non_accepted_extension(tmpdir, capsys):
    """Test parseFiles with a file having a non-accepted extension."""
    test_filename = "Movie.Title.2023.txt"
    file_path = tmpdir.join(test_filename)
    file_path.write("some text content")
    
    salmiak.parseFiles(str(tmpdir))
    
    captured = capsys.readouterr()
    expected_message = salmiak.bcolors.FAIL + '    ' + 'Warning: ' + salmiak.bcolors.ENDC + test_filename + " <== What is this file? Is it really a movie?\n"
    assert expected_message in captured.out

def test_parseFiles_file_not_movie_or_episode_type_by_guessit(tmpdir, capsys):
    """
    Test parseFiles with a file that isValidPath would reject.
    This covers cases where guessit might not find title/year, or ext is wrong.
    """
    # This filename is unlikely to be guessed as a valid movie/episode by isValidPath
    # because it lacks a year in a typical format recognised by guessit for movies/episodes
    # and .log is not an accepted extension.
    test_filename = "system_log_archive.log" 
    file_path = tmpdir.join(test_filename)
    file_path.write("system data")

    salmiak.parseFiles(str(tmpdir))

    captured = capsys.readouterr()
    expected_message = salmiak.bcolors.FAIL + '    ' + 'Warning: ' + salmiak.bcolors.ENDC + test_filename + " <== What is this file? Is it really a movie?\n"
    assert expected_message in captured.out
