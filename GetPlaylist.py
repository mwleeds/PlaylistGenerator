#!/usr/bin/python3

##################################################################
#
# File: GetPlaylist.py
# Last Edit: 9.19.14
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
    myPandora.login("aoeuhtns4@gmail.com", "jK6kTGWrJ")
    myPandora.addSeedArtists("testseeds.txt")
    myPandora.getSongs(23, "playlist.txt")
    myPandora.deleteStation()
    print("Done.")
    '''
    mySpotify = SpotifyBot()
    mySpotify.login("aoeuhtns4", "jK6kTGWrJ")
    mySpotify.addSeedArtists("testseeds.txt")
    input()

if __name__=="__main__":
    main()
