PlaylistGenerator
=================

The purpose of these scripts is to generate playlists (as text files)
automatically from different sources using a list of seed artists. Right now 
it only pulls from Pandora and Spotify Radio.

Dependencies
============

- Firefox 33
- Selenium 2.44
- Python 3

Usage
=====

First, make sure you have Firefox installed and Selenium webdriver for python
either installed or in the same directory, and PandoraBot.py and GetPlaylist.py
in the same directory.

Now, for Pandora:
Edit "GetPlaylist.py" to have the number of songs and the names of the input
and output files how you want them, then just run "python3 GetPlaylist.py" 
in a terminal.

The process for using Spotify is very similar. Just edit the appropriate section
of "GetPlaylist.py".
