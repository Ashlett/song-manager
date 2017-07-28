import os
from datetime import date
from tkinter.filedialog import askopenfilename
from tkinter import Frame, Label, Button, Entry, Toplevel

from .models import Song
from .song_widget import SongWidget
from .util import str_to_date


class SongAdder(Frame):

    def __init__(self, parent, song_list, music_dir):
        super().__init__(parent)
        self.song_list = song_list
        self.music_dir = music_dir

        Label(self, text="Date added").grid(row=0, column=0)
        self.date_added = Entry(self)
        self.date_added.grid(row=1, column=0)
        self.date_added.insert(0, date.today())

        self.master.title('Add song')
        Label(self, text="Location").grid(row=0, column=1)
        Button(self, text="Choose file", command=self.choose_location).grid(row=1, column=1)

    def choose_location(self):
        location = askopenfilename(initialdir=self.music_dir)
        if location:
            song = Song.from_filename(location)
            self.music_dir = os.path.dirname(location)

            top = Toplevel()

            def ok():
                top.destroy()
                try:
                    self.song_list.add_song(song, adding_date=str_to_date(self.date_added.get()))
                except ValueError as e:
                    print(e)

            top.title("Song")
            button = Button(top, text="OK", command=ok)
            button.pack()
            SongWidget(parent=top, song=song).pack()
            top.mainloop()
