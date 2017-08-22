from tkinter import Button, Tk, Toplevel

from .mixtape_maker import MixtapeMaker
from .song_adder import SongAdder


class FavouriteSong(Tk):

    def __init__(self, song_list, config):
        super().__init__()
        self.wm_title('Favourite Song')
        self.minsize(height=80, width=300)
        self.song_list = song_list
        self.config = config
        Button(text='Add new song', command=self.song_adder).pack()
        Button(text='Make mixtapes', command=self.mixtape_maker).pack()

    def song_adder(self):
        self.switch_to_window(SongAdder)

    def mixtape_maker(self):
        self.switch_to_window(MixtapeMaker)

    def switch_to_window(self, window_class):
        top = Toplevel(self)
        window_class(parent=top, song_list=self.song_list, config=self.config).pack()
        top.grab_set()
        top.mainloop()
