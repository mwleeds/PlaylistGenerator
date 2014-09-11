#!/usr/bin/python3

##################################################################
#
# File: GetPlaylist.py
# Last Edit: 9.10.14
# Author: Matthew Leeds
# Purpose: Use the PandoraBot class to get scrape songs from there.
#
##################################################################

from PandoraBot import PandoraBot

def main():
    myPandora = PandoraBot()
    myPandora.login("aoeuhtns4@gmail.com", "jK6kTGWrJ")
    myPandora.addSeedArtists("testseeds.txt")
    myPandora.getSongs(20, "playlist.txt")
    myPandora.deleteStation()
    print("Done.")

if __name__=="__main__":
    main()
