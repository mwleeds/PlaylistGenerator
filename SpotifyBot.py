#!/usr/bin/python3

##################################################################
#
# File: SpotifyBot.py
# Last Edit: 9.19.14
# Author: Matthew Leeds
# Purpose: A web crawler to get a playlist from Spotify Radio 
# based on a list of seed artists. Unfortunately the Spotify 
# WebAPI doesn't have radio functionality as far as I can tell.
#
##################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

class SpotifyBot(object):

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)

    # logs in to spotify.com using the given credentials
    def login(self, username, password):
        self.driver.get("https://play.spotify.com/")
        self.driver.find_element(By.ID, "has-account").click()
        self.driver.find_element(By.ID, "login-usr").send_keys(username)
        self.driver.find_element(By.ID, "login-pass").send_keys(password)
        self.driver.find_element(By.XPATH, "//*[@id='sp-login-form']/div/button").click()

    # creates a station with the seed artists found in the specified input file
    def addSeedArtists(self, filename):
        seedArtists = open(filename, 'r')
        seedArtistList = seedArtists.readlines()
        firstArtist = seedArtistList[0][:len(seedArtistList[0]) - 1]
        self.driver.find_element(By.ID, "nav-collection").click() # go to "Your Music"
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//@id='main'/div[3]/div[1]/iframe"))
        self.driver.find_element(By.XPATH, "/html/body/div[4]/div/nav/div/div[1]").click() # click "New Playlist"
        sleep(0.5)
        self.driver.find_element(By.XPATH, "/html/body/div[4]/div/nav/div/div[3]/form/div[1]/input").send_keys("for radio")
        sleep(0.5)
        self.driver.find_element(By.XPATH, "/html/body/div[4]/div/nav/div/div[3]/form/div[2]/button").click()
        sleep(1)
        playlistURL = self.driver.current_url
        for i in range(1, len(seedArtistList)):
            currentArtist = seedArtistList[i][:len(seedArtistList[i]) - 1]
            print("Adding songs by " + currentArtist + " to the playlist")
            self.driver.switch_to.default_content()
            self.driver.find_element(By.ID, "nav-search").click() # go to "Search"
            sleep(0.5)
            self.driver.switch_to.frame("suggest")
            self.driver.find_element(By.XPATH, "/html/body/div[1]/form/input").send_keys(currentArtist)
            sleep(2)
            # assume the top result is the right one
            self.driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[1]/ul[1]/li/a").click()
            sleep(2)
            for j in range(5): # grab their top five songs
                self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//@id='main'/div[3]/div[2]/iframe"))
                toplist = self.driver.find_element(By.XPATH, "//*[@id='toplist-row']/div[1]/table/tbody")
                toplist.find_element(By.XPATH, "./@data-index='" + str(j) + "'/td[5]/button").click()
                sleep(0.5)
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame("context-actions")
                self.driver.find_element(By.ID, "add-to").click()
                sleep(0.5)
                # assume the first playlist is the right one
                self.driver.find_element(By.XPATH, "//*[@id='playlist-list']/ul/li[3]/a").click()
                sleep(0.5)
        # now all the artists should have songs in the playlist "for radio"
        self.driver.switch_to.default_content()

    # records song and artist names and writes them to a file
    def getSongs(self, numSongs, filename):
        playList = []
        while len(playList) < numSongs:
            songName = self.driver.find_element(By.XPATH, "//*[@id='trackInfo']/div/div[2]/div/div[1]/a").text
            artistName = self.driver.find_element(By.XPATH, "//*[@id='trackInfo']/div/div[2]/div/div[2]/a").text
            if len(songName) > 0:
                print("Recorded: " + songName + " by " + artistName)
                playList.append(songName + " by " + artistName)
            remainingTime = self.driver.find_element(By.XPATH, "//*[@id='playbackControl']/div[2]/div[1]").text
            remainingTime = remainingTime[1:]
            remainingSeconds = (int(remainingTime.split(':')[0]) * 60) + int(remainingTime.split(':')[1])
            print("Waiting " + str(remainingSeconds) + " seconds for the song to end.")
            sleep(remainingSeconds + 5)
        print("Writing " + str(len(playList)) + " songs to " + filename)
        playlistFile = open(filename, 'w')
        for song in playList:
            playlistFile.write(song + "\n")
        playlistFile.close()

    # deletes a station so the next time the script runs it can assume there are none
    def deleteStation(self):
        pass

    def __del__(self):
        self.driver.quit()
