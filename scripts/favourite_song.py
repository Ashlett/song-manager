#!/usr/bin/env python
# coding: utf-8

import os

from songmgr.database.song_list import SongList
from songmgr.gui.favourite_song_init import FavSongInit
from songmgr.gui.favourite_song_main import FavouriteSong
from songmgr.util.util import get_config_file_path
from songmgr.util.config import DictConfig

config_file = get_config_file_path('favourite_song.cfg')
if not os.path.isfile(config_file):
    fsi = FavSongInit()
    fsi.mainloop()

config = DictConfig(config_file)
song_list = SongList(db_file=config['db_file'])

FavouriteSong(song_list, config).mainloop()
