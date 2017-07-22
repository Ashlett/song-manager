import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base, Favourite, Song


class SongList(object):

    def __init__(self, db_file):
        self.db_file = db_file
        engine = create_engine('sqlite:///' + db_file, echo=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def __iter__(self):
        query = self.session.query(Song)
        for obj in query:
            yield obj

    def __len__(self):
        return self.session.query(Song).count()

    def __contains__(self, song):
        return bool(self.find_song(song))

    def find_song(self, song):
        return self.filter_songs(artist=song.artist, title=song.title, album=song.album)

    def filter_songs(self, **kwargs):
        rows = self.session.query(Song).filter_by(**kwargs)
        return rows.all()

    def add_song(self, song, adding_date=None, removing_date=None):
        adding_date = adding_date or datetime.date.today()
        removing_date = removing_date or datetime.date.max
        songs = self.find_song(song)
        for existing in songs:
            if existing.is_favourite(adding_date):
                raise ValueError('Song {} by {} from {} already present'.format(song.title, song.artist, song.album))
        song.favourites.append(Favourite(from_date=adding_date, to_date=removing_date))
        self.session.add(song)
        self.session.commit()
