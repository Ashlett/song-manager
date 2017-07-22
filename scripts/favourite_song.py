#!/usr/bin/env python
# coding: utf-8

import os
from tkinter import Tk

from songmgr.config import DictConfig
from songmgr.song_adder import SongAdder
from songmgr.song_list import SongList
from songmgr.util import get_config_file_path
from songmgr.favourite_song_init import FavSongInit


config_file = get_config_file_path('favourite_song.cfg')
if not os.path.isfile(config_file):
    fsi = FavSongInit()
    fsi.mainloop()

config = DictConfig(config_file)
song_list = SongList(db_file=config['db_file'])

master = Tk()
master.wm_title('Favourite Song')
SongAdder(parent=master, song_list=song_list, music_dir=config['music_dir']).pack()
master.mainloop()
