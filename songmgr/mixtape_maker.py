from tkinter import Button, Checkbutton, Entry, Frame, IntVar, Label, StringVar
from tkinter import messagebox, filedialog
import os

from .playlist import Playlist, playlist_formats


class MixtapeMaker(Frame):

    def __init__(self, parent, song_list, config):
        parent.minsize(height=200, width=400)
        super().__init__(parent)
        self.song_list = song_list
        self.new_mixtapes = []
        self.config = config
        self.master.title('Make mixtapes')
        self.show_initial_screen()

    def get_suggestion(self):
        num_new_mixtapes, fullness = self.song_list.get_mixtape_fullness()
        if fullness <= 0.97:
            text = 'Not enough songs for {} mixtapes'
            color = 'blue'
        elif 0.97 < fullness <= 0.976:
            text = 'This is a good time to make {} mixtapes'
            color = 'green'
        elif 0.976 < fullness <= 0.982:
            text = 'It\'s high time to make {} mixtapes!'
            color = 'yellow'
        else:
            text = 'Probably too many songs to make {} mixtapes'
            color = 'red'
        text += ' ({:.2f} % full)'
        return text.format(num_new_mixtapes, fullness * 100), color

    def show_initial_screen(self):
        page = self._new_page()
        text, color = self.get_suggestion()
        Label(page, text=text, foreground=color).pack()
        Button(page, text='Make mixtapes', command=self.make_mixtapes).pack()

    def make_mixtapes(self):
        try:
            self.new_mixtapes = self.song_list.get_new_mixtapes()
            # self.song_list.save_new_mixtapes(self.new_mixtapes)
            self.mixtape_success()
        except Exception as e:
            self.mixtape_failure(e)

    def mixtape_success(self):
        page = self._new_page()
        Label(page, text='Mixtapes successfully done!', foreground='green').pack()
        Button(page, text='Save playlists', command=self.show_playlist_settings).pack()

    def mixtape_failure(self, exception):
        page = self._new_page()
        Label(page, text=str(exception), foreground='red').pack()
        Button(page, text='Try again', command=self.make_mixtapes).pack()

    def show_playlist_settings(self):
        page = self._new_page()

        Label(page, text='format:').grid(column=0, row=0)
        vars = {}
        row = 0
        for pf in playlist_formats:
            var = IntVar()
            check = Checkbutton(page, text=pf, variable=var)
            check.grid(column=1, row=row)
            check.select()
            vars[pf] = var
            row += 1

        Label(page, text='name:').grid(column=0, row=row)
        name = StringVar()
        if 'mixtape_name' in self.config:
            name.set(self.config['mixtape_name'])
        Entry(page, textvariable=name).grid(column=1, row=row)
        row += 1

        Label(page, text='folder:').grid(column=0, row=row)
        folder = StringVar(value=self.config['music_dir'])
        Button(page, text='Choose', command=lambda: self.choose_folder(var=folder)).grid(column=1, row=row)
        row += 1
        Label(page, textvariable=folder).grid(column=1, row=row)
        row += 1

        def _check_and_go():
            formats = [v for v in vars if vars[v].get()]
            if not formats:
                messagebox.showerror(title='Error', message='At lest one playlist format must be selected')
            else:
                self.config['mixtape_name'] = name.get()
                self.config.save()
                self.save_playlists(formats=formats, mixtape_name=name.get(), directory=folder.get())

        Button(page, text='OK', command=_check_and_go).grid(column=0, row=row, columnspan=2)

    def choose_folder(self, var):
        folder = filedialog.askdirectory(initialdir=self.config['music_dir'])
        var.set(folder)

    def save_playlists(self, formats, mixtape_name, directory):
        for mx in self.new_mixtapes:
            vol = mx[0].mixtape_vol
            pl = Playlist(mx)
            print(pl)
            for f in formats:
                mixtape_file_name = '{} vol.{}.{}'.format(mixtape_name, vol, f)
                mixtape_path = os.path.join(os.path.realpath(directory), mixtape_file_name)
                # pl.save_to_file(mixtape_path, f)
                print(mixtape_path)
        self.show_end_screen()

    def show_end_screen(self):
        page = self._new_page()
        Label(page, text='DONE!', foreground='green').pack()
        Button(page, text='OK', command=self.master.destroy).pack()

    def _new_page(self):
        frame = Frame(self)
        frame.grid(column=0, row=0, sticky='nsew')
        frame.tkraise()
        return frame
