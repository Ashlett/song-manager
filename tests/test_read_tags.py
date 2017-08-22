import os
from songmgr.util.read_tags import read_tags


def test_read_tags():
    mp3_dir = os.path.join(os.path.dirname(__file__), 'test_files', 'mp3')
    file_path = os.path.join(mp3_dir, 'Alex Cohen - Good Old Times.mp3')
    tags = read_tags(file_path)
    expected = {
        'album': None,
        'artist': 'Alex Cohen',
        'time_secs': 145.13632653061225,
        'title': 'Good Old Times',
        'track_num': 4,
        'year': None
    }
    assert tags == expected
