import os
import datetime

from unittest import TestCase

from songmgr.database.models import Favourite, Song


class TestSong(TestCase):

    def setUp(self):
        self.song = Song(artist='Artist', title='Title', time_secs=207.75)

    def test_attributes(self):
        self.assertEqual(self.song.artist, 'Artist')
        self.assertEqual(self.song.title, 'Title')
        self.assertEqual(self.song.album, None)

    def test_str(self):
        self.assertEqual(str(self.song), 'Artist - Title')

    def test_is_favourite(self):
        self.assertFalse(self.song.is_favourite())

    def test_as_dict(self):
        expected = {
            'album': None,
            'artist': 'Artist',
            'location': None,
            'mixtape_vol': None,
            'mixtape_item': None,
            'time_secs': 207.75,
            'title': 'Title',
            'track_num': None,
            'year': None
        }
        self.assertEqual(self.song.as_dict(), expected)

    def test_equality(self):
        song2 = Song(artist='Artist', title='Title', time_secs=207.75)
        self.assertEqual(self.song, song2)
        song3 = Song(artist='Artist', title='Another Title', time_secs=207.75)
        self.assertNotEqual(self.song, song3)

    def test_time_secs_as_int(self):
        self.assertEqual(self.song.time_secs_as_int, 207)

    def test_from_filename(self):
        curdir = os.path.dirname(__file__)
        mp3_file = os.path.join(curdir, 'test_files', 'mp3', 'Kinematic - Peyote.mp3')
        song = Song.from_filename(mp3_file, curdir)
        expected = {
            'album': 'Kites',
            'artist': 'Kinematic',
            'location': 'test_files/mp3/Kinematic - Peyote.mp3',
            'mixtape_vol': None,
            'mixtape_item': None,
            'time_secs': 183.51020408163265,
            'title': 'Peyote',
            'track_num': 5,
            'year': None
        }
        self.assertEqual(song.as_dict(), expected)


class TestFavourite(TestCase):

    def test_added_today(self):
        favourite = Favourite(from_date=datetime.date.today(), to_date=datetime.date.max)
        self.assertTrue(favourite.is_current())

    def test_from_given_date(self):
        favourite = Favourite(from_date=datetime.date(2010, 10, 10), to_date=datetime.date.max)
        self.assertTrue(favourite.is_current())
        self.assertEqual(str(favourite), '2010-10-10 - 9999-12-31 | None')

    def test_not_current(self):
        favourite = Favourite(from_date=datetime.date(2008, 8, 8), to_date=datetime.date(2011, 11, 11))
        self.assertFalse(favourite.is_current())
        self.assertEqual(str(favourite), '2008-08-08 - 2011-11-11 | None')


class TestSongWithFavourite(TestCase):

    def test_song_currently_favourite(self):
        song = Song(artist='Artist', title='Title')
        favourite = Favourite(from_date=datetime.date(2010, 10, 10), to_date=datetime.date.max, song=song)
        self.assertTrue(song.is_favourite())
        self.assertEqual(str(favourite), '2010-10-10 - 9999-12-31 | Artist - Title')

    def test_song_favourite_in_the_past(self):
        song = Song(artist='Artist', title='Title')
        favourite = Favourite(from_date=datetime.date(2008, 8, 8), to_date=datetime.date(2011, 11, 11), song=song)
        self.assertFalse(song.is_favourite())
        self.assertEqual(str(favourite), '2008-08-08 - 2011-11-11 | Artist - Title')
