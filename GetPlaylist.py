#!/usr/bin/python3

#######################################################################
#
# File: GetPlaylist.py
# Last Edit: 11.10.2014
# Author: Matthew Leeds
# Purpose: Use PandoraBot and SpotifyBot to scrape songs from
# their radio services. To use, run something like:
# $ python3 GetPlaylist.py Pandora email pass seed.txt 20 playlist.csv
#
#######################################################################

import sys
import traceback
from PandoraBot import PandoraBot
from SpotifyBot import SpotifyBot

def main():
    if len(sys.argv) < 7:
        print("Too few arguments given. Syntax:")
        print("python3 GetPlaylist.py SERVICENAME USERNAME PASSWORD SEEDFILENAME NUMSONGS OUTFILENAME")
        return
    else:
        NSERVICE = sys.argv[1]
        USERNAME = sys.argv[2]
        PASSWORD = sys.argv[3]
        SEEDFILE = sys.argv[4]
        NUMSONGS = sys.argv[5]
        SONGFILE = sys.argv[6]
    if NSERVICE == "Pandora": 
        myPandora = PandoraBot()
        myPandora.login(USERNAME, PASSWORD)
        myPandora.addSeedArtists(SEEDFILE)
        try:
            myPandora.getSongs(int(NUMSONGS), SONGFILE)
        except:
            traceback.print_exc(file=sys.stdout)
        myPandora.deleteStation()
    elif NSERVICE == "Spotify":
        mySpotify = SpotifyBot()
        mySpotify.login(USERNAME, PASSWORD)
        mySpotify.addSeedArtists(SEEDFILE)
        mySpotify.getSongs(int(NUMSONGS), SONGFILE)
        #mySpotify.deleteStation()
        #mySpotify.deletePlaylist()

if __name__=="__main__":
    main()
