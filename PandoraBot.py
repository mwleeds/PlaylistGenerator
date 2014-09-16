#!/usr/bin/python3

##################################################################
#
# File: PandoraBot.py
# Last Edit: 9.11.14
# Author: Matthew Leeds
# Purpose: A web crawler to get a playlist from pandora based on 
# a list of seed artists.
#
##################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

class PandoraBot(object):

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)

    # logs in to pandora.com using the given credentials
    def login(self, username, password):
        self.driver.get("http://www.pandora.com")
        self.driver.find_element(By.CSS_SELECTOR, "div.message:nth-child(1) > a:nth-child(1)").click()
        self.driver.find_element(By.CSS_SELECTOR, "div.formField:nth-child(1) > input:nth-child(1)").send_keys(username)
        self.driver.find_element(By.CSS_SELECTOR, "div.formField:nth-child(2) > input:nth-child(1)").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "input.btn_bg").click()

    # creates a station with the seed artists found in the specified input file
    def addSeedArtists(self, filename):
        seedArtists = open(filename, 'r')
        seedArtistList = seedArtists.readlines()
        firstArtist = seedArtistList[0][:len(seedArtistList[0]) - 1]
        sleep(5)
        self.driver.get("http://www.pandora.com/profile")
        sleep(5)
        createStation = self.driver.find_element(By.CSS_SELECTOR, "#playerBar > div.highlight > div.columns > div.leftcolumn > div > input")
        createStation.click()
        print("Adding station for " + firstArtist)
        for letter in firstArtist:
            createStation.send_keys(letter)
            sleep(0.1)
        sleep(3)
        createStation.send_keys(Keys.ENTER)
        sleep(1)
        self.driver.get("http://www.pandora.com/")
        sleep(5)
        for i in range(1, len(seedArtistList)):
            currentArtist = seedArtistList[i][:len(seedArtistList[i]) - 1]
            print("Adding " + currentArtist)
            addVariety = self.driver.find_element(By.XPATH, "//*[@id='stationList']/div[2]/div[1]/div[2]")
            addVariety.click()
            inputBox = self.driver.find_element(By.XPATH, "//*[@id='body']/div[88]/div/div/div/div[3]/div[1]/div[2]/form/input")
            for letter in currentArtist:
                inputBox.send_keys(letter)
                sleep(0.1)
            sleep(2)
            inputBox.send_keys(Keys.ENTER)
            sleep(2)
        seedArtists.close()
        sleep(2)

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
        self.driver.find_element(By.XPATH, "//*[@id='stationList']/div[2]/div[1]/div[1]").click()
        sleep(0.5)
        self.driver.find_element(By.XPATH, "//*[@id='station_menu_dd']/ul/li[5]/a").click()
        sleep(1)

    def __del__(self):
        self.driver.quit()
