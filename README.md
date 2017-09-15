# Favourite Song Manager

Desktop application for keeping a database of favourite songs and creating CD-length playlists from them.


## Installation

1. Download the project or clone it:
`git clone https://github.com/Ashlett/song-manager.git`

2. Create virtual environment (optional, but recommended; you need to have virtualenvwrapper installed):
`mkvirtualenv --python=/usr/bin/python3 songmgr`

3. Install requirements:
`pip install -r requirements.txt`

4. Install the package:
`python setup.py install` (normal installation) or
`python setup.py develop` (for developers)


## Running tests

1. Install pytest: `pip install pytest pytest-cov`

2. In the project directory, run: `pytest`


## Usage

Activate virtual environment (if not already in it): `workon songmgr` and run the main script: `favourite_song.py`

### Initial configuration

On the first use, you will be prompted to choose directory storing all your music and where to store the database file:

![Initial config screen](docs/screenshots/init_dirs_chosen.png?raw=true)

After clikcing **OK**, you will see the main window:

![Main window](docs/screenshots/main.png?raw=true)

### Adding songs

In the main window,click **Add new song** to add a song to favourites:

![Add song](docs/screenshots/song_adder.png?raw=true)

Select an MP3 using **Choose file**. You will see song details:

![Song details](docs/screenshots/song_widget.png?raw=true)

After clicking **OK** the song will be added to your list.

### Creating playlists

When you have some songs in your collection, you can make mixtape playlists.
In the main window, click **Make mixtapes**:

![Make mixtapes](docs/screenshots/mixtape_maker.png?raw=true)

Click **Make mixtapes** again:

![Mixtape success](docs/screenshots/mixtape_success.png?raw=true)

Mixtape information has been written to the database. Now click **Save playlists**:

![Save playlists](docs/screenshots/save_playlists.png?raw=true)

Choose where to save playlists, in which formats and how their filenames should start and click **OK**:

![Mixtapes done](docs/screenshots/mixtapes_done.png?raw=true)

Playlists are now saved to disk:

![Playlists on disk](docs/screenshots/playlists_on_disk.png?raw=true)
