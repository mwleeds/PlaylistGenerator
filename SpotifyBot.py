#!/usr/bin/python3

##################################################################
#
# File: SpotifyBot.py
# Last Edit:11.09.2014
# Author: Matthew Leeds
# Purpose: A web crawler to get a playlist from Spotify Radio 
# based on a list of seed artists. Unfortunately the Spotify 
# WebAPI doesn't have radio functionality as far as I can tell.
#
##################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import csv

class SpotifyBot(object):

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.playlistURL = ""

    # logs in to play.spotify.com using the given credentials
    def login(self, username, password):
        self.driver.get("https://play.spotify.com/")
        self.driver.find_element(By.ID, "has-account").click()
        sleep(0.5)
        self.driver.find_element(By.ID, "login-usr").send_keys(username)
        self.driver.find_element(By.ID, "login-pass").send_keys(password)
        input("Click Log in and press enter...")
        #loginbutton = self.driver.find_element(By.XPATH, "//*[@id='sp-login-form']/div[@class='inputs']/button")
        #loginbutton.click()
        #ActionChains(self.driver).move_to_element(loginbutton).click(loginbutton).perform()
        #self.driver.find_element(By.ID, "sp-login-form").submit()


    # creates a station with the seed artists found in the specified input file
    def addSeedArtists(self, filename):
        seedArtists = open(filename, 'r')
        seedArtistList = seedArtists.readlines()
        # create a new playlist
        self.driver.find_element(By.ID, "nav-collection").click() # go to "Your Music"
        self.driver.get("https://play.spotify.com/collection")
        theframe = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[4]/div[3]/div[1]/iframe")
        self.driver.switch_to.frame(theframe)
        self.driver.find_element(By.XPATH, "/html/body/div[4]/div/nav/div/div[1]").click() # click "New Playlist"
        sleep(0.5)
        self.driver.find_element(By.XPATH, "/html/body/div[4]/div/nav/div/div[3]/form/div[1]/input").send_keys("for radio")
        sleep(0.5)
        self.driver.find_element(By.XPATH, "/html/body/div[4]/div/nav/div/div[3]/form/div[2]/button").click()
        sleep(1)
        self.playlistURL = self.driver.current_url
        for i in range(len(seedArtistList)):
            self.driver.get("https://play.spotify.com/collection")
            currentArtist = seedArtistList[i][:len(seedArtistList[i]) - 1]
            print("Adding songs by " + currentArtist + " to the playlist")
            self.driver.find_element(By.XPATH, "//*[@id='nav-search']/span").click() # go to "Search"
            sleep(0.5)
            self.driver.switch_to.frame("suggest")
            self.driver.find_element(By.XPATH, "/html/body/div[1]/form/input").send_keys("artist:" + currentArtist)
            sleep(2)
            # see all results so there is consistent behavior on subsequent searches
            self.driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[1]/div[1]").click()
            sleep(4)
            self.driver.switch_to.default_content()
            theframe = self.driver.find_element(By.XPATH, "//div[@id='section-collection']/div[@class='front']/iframe")
            self.driver.switch_to.frame(theframe)
            # assume the top result is the right one
            self.driver.find_element(By.XPATH, "/html/body/div[1]/section[2]/section[1]/ul/li[1]/div/div/div[2]/div/a").click()
            for j in range(3): # grab their top three songs
                self.driver.switch_to.default_content()
                theframe = self.driver.find_element(By.XPATH, "//div[@id='section-collection']/div[@class='front']/iframe")
                self.driver.switch_to.frame(theframe)
                toplist = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[1]/div[1]/table/tbody")
                row = toplist.find_element(By.XPATH, "./*[@data-index='" + str(j) + "']")
                morebutton = row.find_element(By.CSS_SELECTOR, "td:nth-last-child(2) > button")
                # scroll down a bit so the top tracks are in view
                self.driver.find_element(By.XPATH, "//div[@class='container']").send_keys(Keys.ARROW_DOWN)
                self.driver.find_element(By.XPATH, "//div[@class='container']").send_keys(Keys.ARROW_DOWN)
                self.driver.find_element(By.XPATH, "//div[@class='container']").send_keys(Keys.ARROW_DOWN)
                ActionChains(self.driver).move_to_element(row).click(morebutton).perform()
                sleep(0.5)
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame("context-actions")
                self.driver.find_element(By.ID, "add-to").click()
                sleep(0.5)
                # assume the first playlist is the right one
                self.driver.find_element(By.XPATH, "//*[@id='playlist-list']/ul/li[3]/a").click()
                sleep(0.5)
                self.driver.switch_to.default_content()
        # now all the artists should have songs in the playlist "for radio"
        self.driver.switch_to.default_content()

    # records song and artist names and writes them to a file
    def getSongs(self, numSongs, filename):
        # qualify the filename so we don't overwrite data from another source
        filename = "Pandora_" + filename
        #self.playlistURL = "https://play.spotify.com/user/aoeuhtns4/playlist/7ku7pWfd9zvtNWabeQ54sE"
        '''
        self.driver.get("https://play.spotify.com/collection")
        theframe = self.driver.find_element(By.XPATH, "//div[@id='main']/div[@id='section-collection']/div[@class='root']/iframe")
        self.driver.switch_to.frame(theframe)
        playlists = self.driver.find_element(By.CSS_SELECTOR, "div.container > div.pf-app > nav > div.list-group")
        # assume the first playlist is the one
        playlists.find_element(By.XPATH, "./div[5]/a").click()
        '''
        self.driver.get(self.playlistURL)
        theframe = self.driver.find_element(By.XPATH, "//div[@id='main']/div[@id='section-collection']/div[@class='root']/iframe")
        self.driver.switch_to.frame(theframe)
        # click the "..." button
        self.driver.find_element(By.CSS_SELECTOR, "div.header-controllers > button.btn:nth-child(5)").click()
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame("context-actions")
        # start a radio station based on the playlist
        self.driver.find_element(By.ID, "start-radio").click()
        sleep(5)
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame("app-player")
        playList = []
        while len(playList) < numSongs:
            # check if it's an ad
            isAd = False
            try:
                isAd = (self.driver.find_element(By.XPATH, "//*[@id='track-name']/a").get_attribute("target") == "_blank")
            except: 
                pass # it's not an ad 
            if not isAd:
                songName = self.driver.find_element(By.ID, "track-name-wrapper").text
                artistName = self.driver.find_element(By.ID, "artist-name-wrapper").text
                print("Recorded: " + songName + " by " + artistName)
                playList.append(songName + " by " + artistName)
            sleep(5)
            playedTime = self.driver.find_element(By.ID, "track-current").text
            playedTimeSeconds = (int(playedTime.split(':')[0]) * 60) + int(playedTime.split(':')[1])
            trackLength = self.driver.find_element(By.ID, "track-length").text
            trackLengthSeconds = (int(trackLength.split(':')[0]) * 60) + int(trackLength.split(':')[1])
            remainingTime = trackLengthSeconds - playedTimeSeconds
            print("Saving to disk.")
            records = []
            for song in playList:
                records.append([song, "", "", ""])
            with open(filename, "w") as csvfile:
                writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                writer.writerow(["Song", "Like?", "Dislike?", "New?"])
                writer.writerows(records)
            print("Waiting " + str(remainingTime) + " seconds for the song to end.")
            sleep(remainingTime + 5)
        print(str(len(playList)) + " songs written to " + filename)

    # deletes the station so the next login will be the same
    def deleteStation(self):
        self.driver.get("https://play.spotify.com/radio")
        theframe = self.driver.find_element(By.XPATH, "//div[@id='section-radio']/div/iframe")
        self.driver.switch_to.frame(theframe)
        # assume the most recent station is the one we want to delete
        self.driver.find_element(By.ID, "recent").send_keys(Keys.ARROW_DOWN)
        self.driver.find_element(By.ID, "recent").send_keys(Keys.ARROW_DOWN)
        self.driver.find_element(By.ID, "recent").send_keys(Keys.ARROW_DOWN)
        self.driver.find_element(By.ID, "recent").send_keys(Keys.ARROW_DOWN)
        self.driver.find_element(By.ID, "recent").send_keys(Keys.ARROW_DOWN)
        deletebutton = self.driver.find_element(By.XPATH, "//div[@id='carousel-inner']/div[1]/div[1]/div[1]/button[1]")
        ActionChains(self.driver).move_to_element(deletebutton).click(deletebutton).perform()
        #deletebutton.click()
        
    # we don't need the playlist any more either
    def deletePlaylist(self):
        self.driver.get(self.playlistURL)
        theframe = self.driver.find_element(By.XPATH, "//div[@id='main']/div[@id='section-collection']/div[@class='root']/iframe")
        self.driver.switch_to.frame(theframe)
        self.driver.find_element(By.CSS_SELECTOR, "div.header-controllers > button.btn:nth-child(5)").click()
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame("context-actions")
        self.driver.find_element(By.ID, "delete-playlist").click()
        self.driver.find_element(By.ID, "playlist-delete-confirm-button").click()

    def __del__(self):
        self.driver.quit()
