# Film Generator
# Created by Özgür Özdemir
# Uploaded /June 13 2017/
# version 1
# This version allows only one theater
# This program uses Cinemaximum website with non-commercial purposes

# Imported Libraries
import json
import datetime
from film import filmList
import time
import webbrowser
import random

with open('data.json') as data_file:
    data = json.load(data_file)

# Getting hours in order to choose greeting message
now = datetime.datetime.now()

class Main():
    # Addding film
    def addFilm(self,str):
        # Index set as -1 in order to decide if user give a proper answer or not
        index = -1
        for _ in filmList:
            # Check users' input is in list or not
            if _[0] == str:
                index = filmList.index(_)
        # If users' input is in the list then program write that film to json film
        if index != -1:
            temp = data["kind"][filmList[index][3]] + 1
            data["kind"][filmList[index][3]] = temp
            data["watched"].append(str)
            with open('data.json', 'w') as data_file:
                json.dump(data, data_file)
            print("Your Film is Added")
        else:
            print("Please be sure you write the film name correctly...")
        # Giving a breathe time to understand what is done for users
        time.sleep(1)
    # Getting Available films
    def availableFilm(self, str):
        # Check users' input is in list or not
        index = -1
        for _ in filmList:
            if _[0] == str:
                index = filmList.index(_)
        if index != -1:
            answer = input("Do you want to go this movie? [Y/N]\n")
            if answer == "Y":
                webbrowser.open(filmList[index][2])
        else:
            print("Please be sure you write the film name correctly...")
        time.sleep(1)
    # Giving a suggestion based on what films that user watched
    def suggestion(self):
        # Creating temp list in order to sort films according to their points
        temp = []
        for _ in filmList:
            # Giving random point based on how times user watched that kind of films
            # Giving random point is also solves the problem if user watched same times
            # of different kinds, it has got a little point difference for avoiding the program
            # decide how to choose suggestion movie
            point = data["kind"][_[3]] * random.uniform(0.1, 0.5)
            information = (_[0], point, _[1], _[4])
            temp.append(information)
        temp.sort(key=lambda tup: tup[1])
        suggested = temp[len(temp)-1]
        print(suggested[0] + (" "*(5-len(suggested))) + suggested[2][0] + suggested[3])
        return suggested[0]

client = Main()
# If users first login program will ask users' name to recognize
if not data['name']:
    data['name'] = input("Welcome to FilmGenerator\nWhat is your name?\n")
    with open('data.json', 'w') as data_file:
        json.dump(data, data_file)
    time.sleep(1)
# Greeting message based on whenever user use the program
if now.hour < 13 and now.hour >= 8:
    print("Good Morning " + data["name"])
elif now.hour >= 13 and now.hour <= 19:
    print("Good Afternoon " + data["name"])
else:
    print("Good Evening " + data["name"])
print("----")
print("Today's Suggestion")
suggested = client.suggestion()
print("You Liked Our [S]uggestion?")
print("----")

# Menu

while True:
    print("")
    print("Menu:")
    print("----")
    print("Add [T]heater To Theaters List")
    print("----")
    print("[A]dd Movie To Watched List")
    print("----")
    print("Your [F]avorite Theaters")
    print("----")
    print("Your Watched [M]ovies")
    print("----")
    print("What Movies Are In Theaters [N]ow?")
    print("----")
    print("[Q]uit")
    print("----")
    clientInput = input("Please type the letter that you choose and press ENTER\n")
    if clientInput == "A":
        print("---")
        print("Available Films:")
        for _ in filmList:
            print(_[0])
        print("[B]ack")
        print("---")
        menuInput = input("Please type full name of film that you want to add...\n")
        if menuInput == "B":
            continue
        else:
            client.addFilm(menuInput)
    elif clientInput == "M":
        print("---")
        print("Your Watched Movies:")
        for _ in data["watched"]:
            print(_)
        print("---")
        time.sleep(2)
    elif clientInput == "F":
        print("---")
        print("Your Favourite Theaters:")
        for _ in data["theaters"]:
            print(_)
        print("Your theater limit: " + str(len(data["theaters"])) + "/ 1")
        print("---")
        time.sleep(2)
    elif clientInput == "N":
        print("---")
        print("Available Films:")
        for _ in filmList:
            print (_[0] + (" "*(30-len(_[0]))) + _[1][0] + (" "*(30-len(_[1][0]))) +_[4])
        print("[B]ack")
        print("---")
        filmInput = input("Please type full name of film that you want to watch...\n")
        if filmInput == "B":
            continue
        else:
            client.availableFilm(filmInput)
    elif clientInput == "S":
         client.availableFilm(suggested)
    elif clientInput == "T":
        print("It's under the construction")
        time.sleep(2)
    elif clientInput == "Q":
        quit(0)
