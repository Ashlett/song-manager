from collections import namedtuple
import os


PlaylistFormat = namedtuple('PlaylistFormat', 'header footer item_format')

playlist_formats = {
    'm3u': PlaylistFormat(
        header='#EXTM3U\n',
        footer='',
        item_format='#EXTINF:{song.time_secs_as_int},{song.artist} - {song.title}\n{location}\n'
    ),
    'wpl': PlaylistFormat(
        header='<?wpl version="1.0"?>\n<smil>\n    <head>\n    </head>\n    <body>\n        <seq>\n',
        footer='        </seq>\n    </body>\n</smil>\n',
        item_format='            <media src="{location}"/>\n'
    )
}


class Playlist(list):

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, list.__repr__(self))

    def __str__(self):
        return '\n'.join('{}. {}'.format(i + 1, x) for i, x in enumerate(self))

    def save_to_file(self, file_path, music_dir, playlist_format=None):
        if os.path.exists(file_path):
            raise IOError('File exists: ' + file_path)
        playlist_format = playlist_format or file_path.rsplit('.', 1)[1].lower()
        try:
            pf = playlist_formats[playlist_format]
        except KeyError:
            raise ValueError('Unknown playlist format: {}. Available formats are: {}'.format(
                playlist_format, ', '.join(playlist_formats.keys())
            ))

        playlist_dir = os.path.dirname(os.path.realpath(file_path))
        with open(file_path, 'w') as f:
            f.write(pf.header)
            for item in self:
                location = os.path.relpath(os.path.join(music_dir, item.location), playlist_dir)
                f.write(pf.item_format.format(song=item, location=location))
            f.write(pf.footer)
