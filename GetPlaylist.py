#!/usr/bin/python3

##################################################################
#
# File: GetPlaylist.py
# Last Edit: 9.21.14
# Author: Matthew Leeds
# Purpose: Use PandoraBot and SpotifyBot to scrape songs from
# their radio services.
#
##################################################################

from PandoraBot import PandoraBot
from SpotifyBot import SpotifyBot

def main():
    '''
    myPandora = PandoraBot()
    myPandora.login(USERNAME, PASSWORD)
    myPandora.addSeedArtists("testseeds.txt")
    myPandora.getSongs(23, "playlist.txt")
    myPandora.deleteStation()
    print("Done.")
    '''
    mySpotify = SpotifyBot()
    mySpotify.login(USERNAME, PASSWORD)
    #mySpotify.addSeedArtists("testseeds.txt")
    mySpotify.getSongs(23, "playlist.txt")
    input()

if __name__=="__main__":
    main()
