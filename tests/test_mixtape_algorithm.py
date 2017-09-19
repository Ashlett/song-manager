import os

from songmgr.database.song_list import SongList
from songmgr.util.mixtape_algorithm import assemble_mixtapes_from, MixtapeAnalysis, MIXTAPE_MAX_DURATION

from .helper import TestCaseWithTempDir


class TestMixtape(TestCaseWithTempDir):

    def setUp(self):
        super().setUp()
        test_db = os.path.join(self.test_files, 'test.db')
        song_list = SongList(test_db)
        self.list_of_songs = list(song_list)

    def test_mixtape_analysis(self):
        analysis = MixtapeAnalysis(self.list_of_songs)
        self.assertAlmostEqual(analysis.total_length, 9223.177649092973)
        self.assertEqual(analysis.num_new_mixtapes, 2)
        self.assertAlmostEqual(analysis.fullness, 0.9729090347144487)

    def test_mixtape_algorithm(self):
        mixtapes = assemble_mixtapes_from(self.list_of_songs)
        self.assertEqual(len(mixtapes), 2)
        on_mixtapes = mixtapes[0] + mixtapes[1]
        for song in self.list_of_songs:
            self.assertIn(song, on_mixtapes)
        for mx in mixtapes:
            duration = sum(s.time_secs for s in mx)
            self.assertLess(duration, MIXTAPE_MAX_DURATION)
            artists = [s.artist for s in mx]
            self.assertEqual(len(artists), len(set(artists)))
