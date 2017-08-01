import pytest
import salmiak


@pytest.mark.parametrize("test_file,expected", [
    ('Kimi.no.na.wa.aka.Your.Name.2016.JAPANESE.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1-FGT.mkv', True),
    ('Looney.Tunes.Volume.2.1936-1959.1080p.BluRay.REMUX.AVC.DD1.0-RARBG.mkv', True),
    ('The.Princess.And.The.Frog.2009.1080p.BluRay.AVC.DTS-HD.MA.5.1-FGT.mkv', True),
    ('Vaid.name.but.no.mkv.extention.2017', False),
    ('Random.Bullshit.without.year.mkv', False),
    ('.git.filename', False)
])


def test_valid_filename(test_file, expected):
    assert salmiak.isValidMovieFile(test_file) == expected

@pytest.mark.parametrize("test_path,expected", [
    ('Kimi.no.na.wa.aka.Your.Name.2016.JAPANESE.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1-FGT', True),
    ('Looney.Tunes.Volume.2.1936-1959.1080p.BluRay.REMUX.AVC.DD1.0-RARBG', True),
    ('.git', False),
    ('@download', False),
])


def test_valid_path(test_path, expected):
    assert salmiak.isValidMoviePath(test_path) == expected
