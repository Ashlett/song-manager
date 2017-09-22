import math
import random

from ..exceptions import NoSongsFoxMixtape

MIXTAPE_MAX_DURATION = 79 * 60


class MixtapeAnalysis(object):

    def __init__(self, list_of_songs):
        if not list_of_songs:
            raise NoSongsFoxMixtape('Cannot create mixtapes from an empty list of songs')
        self.list_of_songs = list_of_songs
        self.total_length = sum(s.time_secs for s in list_of_songs)
        self.num_new_mixtapes = math.ceil(self.total_length / MIXTAPE_MAX_DURATION)
        self.fullness = self.total_length / (self.num_new_mixtapes * MIXTAPE_MAX_DURATION)


def assemble_mixtapes_from(list_of_songs):
    analysis = MixtapeAnalysis(list_of_songs)

    by_artist = {}
    for s in list_of_songs:
        by_artist.setdefault(s.artist, []).append(s)
    by_artist = sorted(by_artist.items(), key=lambda x: len(x[1]), reverse=True)

    new_mixtapes = [[] for _ in range(analysis.num_new_mixtapes)]
    num_mixtape = 0
    single_songs = []

    for artist, songs in by_artist:
        if len(songs) == 1:
            single_songs.append(songs[0])
        else:
            while songs:
                song = random.choice(songs)
                new_mixtapes[num_mixtape].append(song)
                songs.remove(song)
                num_mixtape = (num_mixtape + 1) % analysis.num_new_mixtapes

    single_songs.sort(key=lambda x: x.time_secs)
    while single_songs:
        song = single_songs.pop()
        by_len = sorted(new_mixtapes, key=lambda x: sum(s.time_secs for s in x))
        shortest = by_len[0]
        shortest.append(song)

    durations = [sum(s.time_secs for s in x) for x in new_mixtapes]
    if all(d < MIXTAPE_MAX_DURATION for d in durations):
        for mx in new_mixtapes:
            random.shuffle(mx)
        random.shuffle(new_mixtapes)
        return new_mixtapes
