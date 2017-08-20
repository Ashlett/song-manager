import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func

from .models import Base, Favourite, Song
from ..util.mixtape_algorithm import assemble_mixtapes_from, MixtapeAnalysis


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

    def get_mixtape_fullness(self):
        no_mixtape = self.filter_songs(mixtape_vol=0)
        analysis = MixtapeAnalysis(no_mixtape)
        return analysis.num_new_mixtapes, analysis.fullness

    def get_new_mixtapes(self):
        no_mixtape = self.filter_songs(mixtape_vol=0)
        for x in range(10):
            mixtapes = assemble_mixtapes_from(no_mixtape)
            if mixtapes:
                return mixtapes
        raise Exception('Unable to assemble mixtapes in 10 tries')

    def save_new_mixtapes(self, new_mixtapes):
        mixtape_num = self.session.query(func.max(Song.mixtape_vol)).one()[0]
        for mx in new_mixtapes:
            mixtape_num += 1
            for num, song in enumerate(mx):
                song.mixtape_vol = mixtape_num
                song.mixtape_item = num + 1
        self.session.commit()
