# Film Generator
# Created by Özgür Özdemir
# Uploaded /June 13 2017/
# version 1
# This version allows only one theater
# This program uses Cinemaximum website with non-commercial purposes

# Imported Libraries: BeautifulSoup and Request
import requests
from bs4 import BeautifulSoup
import json

# Reading data about users films, theaters and movie kinds from data.json
with open('data.json') as data_file:
    data = json.load(data_file)

class Film():
    # Getting kind of film in order to suggest to user same kind of films
    def getKind(self, url):
        # Getting HTML response to parse it and getting data
        r = requests.get(url)
        # BeautifulSoup makes our response more readible and parsable
        soup = BeautifulSoup(r.text, 'html.parser')
        film = soup.find('div', {"class": "table-container"})
        for kind in film.find_all('strong'):
            if kind.contents[0] == "Tür:":
                return kind.parent.contents[1][1:]

    # Getting URL of film in order to direct to the site that buy ticket
    def getURL(self, r):
        return "https://www.cinemaximum.com.tr" + r.find('a').get('href')

    # Getting available films list and earliest sessions
    def getFilmList(self, url):
        filmList = []
        r = requests.get(url)
        theater = url.split("/")[3]
        soup = BeautifulSoup(r.text, 'html.parser')
        # Getting one of the films divison
        for film in soup.find_all('div', {"class" : "sessions-display__movie"}):
            filmName = ""
            sessions = []
            #Getting the name of film
            for name in film.find_all('div', {"class" : "sessions-display__img"}):
                filmName = ""
                sessions = []
                temp = name.find('img')
                filmName = temp.get('alt')
                #Getting the url of film
                filmURL = self.getURL(name)
                #Getting the available sessions
                for session in film.find_all('a', {"class" : "nxm-session-btn"}):
                    # If button is inactive that means length of class list is 3
                    # elements, so we didn't need that information
                    if len(session['class']) > 2:
                        continue
                    sessionTime = ""
                    # Getting all sessions of film
                    for info in session.find_all('span'):
                        sessionTime += info.contents[0] + " "
                    sessions.append(sessionTime)
            #Getting the kind of film
            kind = self.getKind(filmURL)
            # We keep whole information in tuples in order to use easily
            if len(sessions) == 0:
                continue
            information = (filmName, sessions, filmURL, kind, theater)
            filmList.append(information)
        return filmList
filmList = []
film = Film()
url = 'https://www.cinemaximum.com.tr/' + data['theaters'][0] + '-sinema-salonu'
filmList = film.getFilmList(url)
