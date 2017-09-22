from tkinter import Frame, Label, Entry


class SongWidget(Frame, object):

    def __init__(self, parent, song):
        super(SongWidget, self).__init__(parent)
        self.song = song.as_dict()

        for row, text in enumerate(['artist', 'title']):
            self.make_entry(row, 0, text)

        for row, text in enumerate(['album', 'track_num']):
            self.make_entry(row, 2, text)

        for row, text in enumerate(['year', 'time_secs']):
            self.make_entry(row, 4, text)

        Label(self, text='location').grid(row=3, column=0, padx=10, pady=1)
        e = Entry(self)
        e.grid(row=3, column=1, columnspan=5, sticky='ew')
        e.insert(0, self.song['location'])
        e.configure(state='readonly')

    def make_entry(self, row, column, text):
        Label(self, text=text).grid(row=row, column=column, padx=10, pady=1)
        e = Entry(self)
        e.grid(row=row, column=column + 1)
        e.insert(0, str(self.song[text]))
        e.configure(state='readonly')
