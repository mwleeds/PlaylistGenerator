PlaylistGenerator
=================

The purpose of these scripts is to generate playlists (as text files)
automatically from different sources using a list of seed artists. Right now 
it only pulls from Pandora.

Dependencies
============

- Firefox 28
- Selenium 2.42
- Python 3

Usage
=====

First, make sure you have Firefox 28 installed and Selenium webdriver for python
either installed or in the same directory, and PandoraBot.py and GetPlaylist.py
in the same directory.

Now, for Pandora:
Edit "GetPlaylist.py" to have the number of songs and the names of the input
and output files how you want them, then just run "python3 GetPlaylist.py" 
in a terminal.
