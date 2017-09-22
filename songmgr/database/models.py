import datetime
import os

from sqlalchemy import Column, Date, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from ..util.read_tags import read_tags

Base = declarative_base()


class Song(Base):

    __tablename__ = 'song'

    id = Column(Integer, primary_key=True)
    artist = Column(String)
    title = Column(String)
    album = Column(String)
    track_num = Column(Integer)
    year = Column(Integer)
    time_secs = Column(Float)
    mixtape_vol = Column(Integer, default=0)
    mixtape_item = Column(Integer, default=0)
    location = Column(String)
    favourites = relationship('Favourite')

    def is_favourite(self, date=None):
        date = date or datetime.date.today()
        for fav in self.favourites:
            if fav.is_current(date):
                return True
        return False

    @classmethod
    def from_filename(cls, location, music_dir):
        song_info = read_tags(location)
        song_info['location'] = os.path.relpath(os.path.realpath(location), music_dir).replace('\\', '/')
        return cls(**song_info)

    @property
    def time_secs_as_int(self):
        return int(self.time_secs)

    def as_dict(self):
        return {
            'album': self.album,
            'artist': self.artist,
            'location': self.location,
            'mixtape_vol': self.mixtape_vol,
            'mixtape_item': self.mixtape_item,
            'time_secs': self.time_secs,
            'title': self.title,
            'track_num': self.track_num,
            'year': self.year
        }

    def __eq__(self, other):
        return (
            type(self) == type(other) and
            self.as_dict() == other.as_dict()
        )

    def __str__(self):
        return '{} - {}'.format(self.artist, self.title)


class Favourite(Base):

    __tablename__ = 'favourite'

    id = Column(Integer, primary_key=True)
    from_date = Column(Date)
    to_date = Column(Date)
    song_id = Column(Integer, ForeignKey('song.id'))
    song = relationship('Song', back_populates='favourites')

    def is_current(self, date=None):
        date = date or datetime.date.today()
        if self.from_date <= date <= self.to_date:
            return True
        else:
            return False

    def __str__(self):
        return '{} - {} | {}'.format(self.from_date, self.to_date, self.song)
