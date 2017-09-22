from mutagen.easyid3 import EasyID3
from mutagen import File


class TagReadingError(Exception):
    pass


def read_tags(file_path):
    try:
        tags = EasyID3(file_path)
        f = File(file_path)
        data = {
            'artist': tags['artist'][0] if 'artist' in tags else tags['albumartist'][0],
            'title': tags['title'][0],
            'album': tags['album'][0] if 'album' in tags else None,
            'track_num': int(tags['tracknumber'][0].split('/')[0]) if 'tracknumber' in tags else None,
            'year': int(tags['date'][0].split('-')[0]) if 'date' in tags else None,
            'time_secs': f.info.length,
        }
        return data
    except KeyboardInterrupt:
        raise
    except Exception as e:
        message = 'Error occurred during reading tags from file {}: {}: {}'
        raise TagReadingError(message.format(file_path, type(e).__name__, e))
