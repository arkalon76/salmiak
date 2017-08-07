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
