import os

from tkinter import Button, Entry, Tk, Label, END
from tkinter.filedialog import askdirectory

from .config import DictConfig
from .util import get_config_file_path


class FavSongInit(Tk):

    def __init__(self):
        super().__init__()
        intro = 'This seems to be your first time using Favourite Song.\nPlease use this setup.'
        Label(self, text=intro).grid(row=0, column=0)

        Label(self, text='Root directory holding all your music:').grid(row=1, column=0)
        self.root_dir = Entry(self)
        self.root_dir.grid(row=2, column=0)
        Button(self, text='Choose', command=lambda: self.choose_directory(self.root_dir)).grid(row=2, column=1)

        Label(self, text='Where to store database file:').grid(row=3, column=0)
        self.db_dir = Entry(self)
        self.db_dir.grid(row=4, column=0)
        Button(self, text='Choose', command=lambda: self.choose_directory(self.db_dir)).grid(row=4, column=1)

        Button(self, text='OK', command=self.ok).grid(row=5, column=0)
        self.title('Favourite Song - Configuration')

    def choose_directory(self, entry):
        location = askdirectory(initialdir=os.environ['HOME'])
        if location:
            entry.delete(0, END)
            entry.insert(0, location)

    def save_config(self):
        config = DictConfig(get_config_file_path('favourite_song.cfg'))
        config['db_file'] = os.path.join(os.path.realpath(self.db_dir.get()), 'favsong.db')
        config['music_dir'] = os.path.realpath(self.root_dir.get())
        config.save()

    def ok(self):
        self.save_config()
        self.destroy()
