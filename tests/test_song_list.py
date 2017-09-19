import os
import shutil

from songmgr.database.models import Song
from songmgr.database.song_list import SongList

from .helper import TestCaseWithTempFiles


class TestSongList(TestCaseWithTempFiles):

    def setUp(self):
        super().setUp()
        self.mp3_files = os.path.join(self.test_files, 'mp3')
        self.empty_db = os.path.join(self.test_files, 'empty.db')
        self.temp_files.append(self.empty_db)
        self.non_empty_db = os.path.join(self.test_files, 'test.db')

    def test_add_song(self):
        song_list = SongList(self.empty_db)
        song = Song(artist='Artist', title='Title', album='Album')
        self.assertEqual(len(song_list), 0)
        self.assertFalse(song in song_list)
        song_list.add_song(song)
        self.assertEqual(len(song_list), 1)
        self.assertTrue(song in song_list)
        self.assertTrue(Song(artist='Artist', title='Title', album='Album') in song_list)
        with self.assertRaises(ValueError):
            song_list.add_song(song)

    def test_mixtape_fullness(self):
        song_list = SongList(self.non_empty_db)
        self.assertEqual(song_list.get_mixtape_fullness(), (2, 0.9729090347144487))

    def test_get_new_mixtapes(self):
        song_list = SongList(self.non_empty_db)
        new_mixtapes = song_list.get_new_mixtapes()
        self.assertEqual(len(new_mixtapes[0] + new_mixtapes[1]), len(song_list))

    def test_save_new_mixtapes(self):
        copy_of_db = os.path.join(self.test_files, 'copy.db')
        self.temp_files.append(copy_of_db)
        shutil.copy(self.non_empty_db, copy_of_db)
        song_list = SongList(copy_of_db)

        new_mixtapes = song_list.get_new_mixtapes()
        for song in song_list:
            self.assertEqual(song.mixtape_vol, 0)
            self.assertEqual(song.mixtape_item, 0)

        song_list.save_new_mixtapes(new_mixtapes)
        for song in song_list:
            self.assertNotEqual(song.mixtape_vol, 0)
            self.assertNotEqual(song.mixtape_item, 0)
        for song in new_mixtapes[1]:
            self.assertEqual(song.mixtape_vol, 2)

    def test_add_song_from_filename(self):
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
