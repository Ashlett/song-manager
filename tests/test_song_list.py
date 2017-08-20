import os
from unittest import mock, TestCase

from songmgr.database.models import Song
from songmgr.database.song_list import SongList


class MyTestCase(TestCase):

    def setUp(self):
        folder = os.path.dirname(__file__)
        self.test_files = os.path.join(folder, 'test_files')
        self.mp3_files = os.path.join(self.test_files, 'mp3')
        self.empty_db = os.path.join(self.test_files, 'empty.db')
        mock_config = {'music_dir': self.mp3_files}
        patcher = mock.patch('songmgr.util.util.get_config', return_value=mock_config)
        self.addCleanup(patcher.stop)
        patcher.start()

    def tearDown(self):
        if os.path.exists(self.empty_db):
            os.remove(self.empty_db)

    def test_add_song(self):
        song_list = SongList(self.empty_db)
        file_path = os.path.join(self.mp3_files, 'Kinematic - Peyote.mp3')
        song = Song.from_filename(file_path)
        self.assertEqual(len(song_list), 0)
        self.assertFalse(song in song_list)
        song_list.add_song(song)
        self.assertEqual(len(song_list), 1)
        self.assertTrue(song in song_list)
        self.assertTrue(Song(artist='Kinematic', title='Peyote', album='Kites') in song_list)
        with self.assertRaises(ValueError):
            song_list.add_song(song)
        print(song.as_dict())
