from datetime import date
from tkinter import Frame, Label, Button, Entry, Toplevel
from tkinter.filedialog import askopenfilename

import os

from ..database.models import Song
from ..util.util import str_to_date
from .song_widget import SongWidget


class SongAdder(Frame):

    def __init__(self, parent, song_list, config):
        super().__init__(parent)
        self.song_list = song_list
        self.config = config
        self.start_dir = config['music_dir']

        Label(self, text="Date added").grid(row=0, column=0)
        self.date_added = Entry(self)
        self.date_added.grid(row=1, column=0)
        self.date_added.insert(0, date.today())

        self.master.title('Add song')
        Label(self, text="Location").grid(row=0, column=1)
        Button(self, text="Choose file", command=self.choose_location).grid(row=1, column=1)

    def choose_location(self):
        location = askopenfilename(initialdir=self.start_dir)
        if location:
            song = Song.from_filename(location, self.config['music_dir'])
            self.start_dir = os.path.dirname(location)

            top = Toplevel()

            def ok():
                top.destroy()
                self.master.grab_set()
                try:
                    self.song_list.add_song(song, adding_date=str_to_date(self.date_added.get()))
                except ValueError as e:
                    print(e)

            top.title("Song")
            button = Button(top, text="OK", command=ok)
            button.pack()
            SongWidget(parent=top, song=song).pack()
            top.grab_set()
            top.mainloop()
