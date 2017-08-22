import os

from songmgr.database.models import Song
from songmgr.util.playlist import Playlist

from .helper import TestCaseWithTempFiles


class TestPlaylist(TestCaseWithTempFiles):

    def setUp(self):
        super().setUp()
        self.mp3_files = os.path.join(self.test_files, 'mp3')
        songs = [
            'Kinematic - Peyote.mp3',
            'Roller Genoa - Build My Gallows High.mp3',
            'Alex Cohen - Good Old Times.mp3',
        ]
        self.songs = [Song.from_filename(os.path.join(self.mp3_files, s), music_dir=self.mp3_files) for s in songs]

    def test_create_playlist(self):
        playlist = Playlist()
        self.assertEqual(len(playlist), 0)
        for song in self.songs:
            playlist.append(song)
        self.assertEqual(len(playlist), 3)
        playlist = Playlist(self.songs)
        self.assertEqual(len(playlist), 3)

    def test_playlist_string(self):
        playlist = Playlist(self.songs)
        expected = '1. Kinematic - Peyote\n2. Roller Genoa - Build My Gallows High\n3. Alex Cohen - Good Old Times'
        self.assertEqual(str(playlist), expected)

    def test_save_to_file(self):
        playlist = Playlist(self.songs)
        expected = '''#EXTM3U
#EXTINF:183,Kinematic - Peyote
mp3/Kinematic - Peyote.mp3
#EXTINF:202,Roller Genoa - Build My Gallows High
mp3/Roller Genoa - Build My Gallows High.mp3
#EXTINF:145,Alex Cohen - Good Old Times
mp3/Alex Cohen - Good Old Times.mp3
'''
        file_path = os.path.join(self.test_files, 'test.m3u')
        self.temp_files.append(file_path)
        playlist.save_to_file(file_path, music_dir=self.mp3_files)
        with open(file_path) as f:
            content = f.read()
        self.assertEqual(content, expected)

    def test_save_to_file_should_fail_when_exists(self):
        playlist = Playlist(self.songs)
        file_path = os.path.join(self.test_files, 'test.m3u')
        self.temp_files.append(file_path)
        playlist.save_to_file(file_path, music_dir=self.mp3_files)
        with self.assertRaises(IOError):
            playlist.save_to_file(file_path, music_dir=self.mp3_files)

    def test_save_to_file_wrong_format(self):
        playlist = Playlist(self.songs)
        file_path = os.path.join(self.test_files, 'test.xxx')
        self.temp_files.append(file_path)
        with self.assertRaises(ValueError):
            playlist.save_to_file(file_path, music_dir=self.mp3_files)
