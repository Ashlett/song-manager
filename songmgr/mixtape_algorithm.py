import math
import random

MIXTAPE_MAX_DURATION = 79 * 60


def assemble_mixtapes_from(list_of_songs):
    total_length = sum(s.time_secs for s in list_of_songs)
    num_new_mixtapes = math.ceil(total_length / MIXTAPE_MAX_DURATION)

    by_artist = {}
    for s in list_of_songs:
        by_artist.setdefault(s.artist, []).append(s)
    by_artist = sorted(by_artist.items(), key=lambda x: len(x[1]), reverse=True)

    new_mixtapes = [[] for _ in range(num_new_mixtapes)]
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
                num_mixtape = (num_mixtape + 1) % num_new_mixtapes

    single_songs.sort(key=lambda x: x.time_secs, reverse=True)
    while single_songs:
        song = random.choice(single_songs[:10])
        by_len = sorted(new_mixtapes, key=lambda x: sum(s.time_secs for s in x))
        shortest = by_len[0]
        shortest.append(song)
        single_songs.remove(song)

    durations = [sum(s.time_secs for s in x) for x in new_mixtapes]
    if all(d < MIXTAPE_MAX_DURATION for d in durations):
        for mx in new_mixtapes:
            random.shuffle(mx)
        return new_mixtapes
