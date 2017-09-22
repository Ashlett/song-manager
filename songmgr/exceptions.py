class SongmgrException(Exception):
    pass


class NoSongsFoxMixtape(SongmgrException):
    pass


class TagReadingError(SongmgrException):
    pass
