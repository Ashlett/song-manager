import os

from songmgr.database.models import Song
from songmgr.database.song_list import SongList

from .helper import TestCaseWithTempFiles


class TestSongList(TestCaseWithTempFiles):

    def setUp(self):
        super().setUp()
        self.mp3_files = os.path.join(self.test_files, 'mp3')
        self.empty_db = os.path.join(self.test_files, 'empty.db')
        self.temp_files.append(self.empty_db)

    def test_add_song(self):
        song_list = SongList(self.empty_db)
        file_path = os.path.join(self.mp3_files, 'Kinematic - Peyote.mp3')
        song = Song.from_filename(file_path, music_dir=self.mp3_files)
        self.assertEqual(len(song_list), 0)
        self.assertFalse(song in song_list)
        song_list.add_song(song)
        self.assertEqual(len(song_list), 1)
        self.assertTrue(song in song_list)
        self.assertTrue(Song(artist='Kinematic', title='Peyote', album='Kites') in song_list)
        with self.assertRaises(ValueError):
            song_list.add_song(song)
        print(song.as_dict())
