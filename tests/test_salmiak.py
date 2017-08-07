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
