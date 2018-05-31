#!/usr/bin/python
__author__ = "Panda-Dog"
__version__ = 0.1
__copyright__ = "All Rights Reserved"
__email__ = "rgmckay@nevada.unr.edu"


#TODO
#1. Change lists to a txt file to ease editing
#2  Create output macro to insert Roll20 of the events (Excluding encounters)
#3  Enable unique party support, user supplies list of party names so output is more streamlined
#4  Develop the Dark Souls experience

##IMPORTS##
import sys, random, math

##GLOBALS##
DAYS_TRAVELLED = 30
THISISDARKSOULS = False

##Wanna add a fun weather? Add it here!
WEATHERS = { ("Seventy degrees. The perfect day dawns accompanied by the most breathtaking sunrise you have ever seen. There is low humidity, clear blue skies with a cool island breeze. +2 morale bonus to all saving throws today!", 2), 
                 ("Seventy-three degrees. A very nice day with clear blue skies and low humidity. +1 on all perception checks today!", 7),  
                 ("Seventy-six degrees. Warm sunny day with a pleasant breeze. +1 hp regained from rest last night!", 8),
                 ("Seventy-nine degrees. Very warm day, partly cloudy and stiff breeze", 8),
                 ("Eighty-two degrees. Warm and overcast. There is no breeze today.", 20),
                 ("Eighty-five degrees. Very warm and humid, and the sun is hidden behind a thick layer of clouds, and its foggy. -1 on all perception checks today.", 3),
                 ("Ninety-one degrees. Very hot and sticky. The air is stagnant and you're sweating your ass off. Fortitude save required.", 7),
                 ("Ninety-four degrees. Very hot and nearly 100% humidity.  Your clothes are drenched in sweat and even walking is a chore. Fortitude save required.", 7),
                 ("Ninety-seven degrees. Opressively hot. The air is wet and heavy and  breathing is difficult and there is no relief even in the shade. Fortitude save required", 6),
                 ("One hundred degrees. This is about as miserable of a day as you can get on the island.  It was difficult to sleep last night being so stiflingly hot.  The humidity index is so high it feels as if you are under water. You are sticky, sweaty and itchy.  Fortitude save required.", 5),
                 ("Today is stagnant and wet.  Greasy drizzle rains from the sky mixed with light volcanic ash. Fortitude save required for those who have lethal damage injuries.", 10),
                 ("The sky is dark and heavy with clouds.  The downpour is almost torrential and everything is soaked and saturated with water.  Leaches and tropical flies crawl everywhere, sticking to your skin and spreading diseases.  Fortitude save required for those who have lethal damage injuries", 5),
                 ("Tropical Thunderstorm! The wind whips and tears at you as heavy drops of rain pelt you and leave welts and bruises. Lightning strobes across the sky with a neverending rumble of thunder. It is impossible to move and you desperately seek shelter. Reflex save required.", 8),
                 ("Hurricane!!! Tornadic winds blow across the island ripping up trees and hurtling rocks and earth across the decimated landscape. Lightning strikes all around you, defening  you with the sharp crack of thunder. It is nearly impossible to see in the torrential downpour, and you are pinned down as you suffer under a hail of deadly debris.  Reflex save required.", 2)
                 }

##Wanna add a new terrain? Add it here!
TERRAINS = { ("STANDARD", 80),
                 ("DIFFICULT TERRAIN", 8),
                 ("Hunting Ground", 8), 
                 ("Resource", 1), 
                 ("Secret", 1), 
                 ("Feature", 2) }

##Main Function
def main():
    MainFunc(THISISDARKSOULS)

def MainFunc(IsThisDarkSouls):
    print("Hello welcome to the Tibaeria Random DC Explorer, Please plot your course carefully as to not cause any issues. Another suggestion is to only pre-roll their intended undiscovered")
    print("Have an adventuring idea for a party to encounter? Wanna set the mood? Try altering weights of these events! Ex. Near a everlasting storm, have the party encounter increased hurricane chances.")
    playerCount = int(input("Please Input Number of Players: "))
    exploredCount = int(input("Input number of explored hexes: "))
    unknownHexCount = int(input("Input number of unexplored hexes: "))

    print("Outputting Explored Hex Encounters \n")
    #Iterate through all explored hex encounters first, then all unexplored
    while exploredCount > 0:
        Travel_Explored(playerCount)
        exploredCount -= 1

    print("Outputting Unexplored Hex Encounters \n")
    while unknownHexCount > 0:
        Travel_UnExplored(playerCount)
        unknownHexCount -= 1

    print("ADVENTURE COMPLETE")
    playerCount = input("Press any key to exit. . .")

## HELPER FUNCTIONS ####### HELPER FUNCTIONS ####### HELPER FUNCTIONS ####### HELPER FUNCTIONS ####### HELPER FUNCTIONS ####### HELPER FUNCTIONS ####### HELPER FUNCTIONS ####### HELPER FUNCTIONS ####### HELPER FUNCTIONS ####### HELPER FUNCTIONS #####

def Travel_Explored(NumOfPlayers):
    weather = Handle_Weather()
    encounters = Handle_Encounters(3, NumOfPlayers)
    Create_Day_Writeup_Explored(weather, encounters)

def Travel_UnExplored(NumOfPlayers):
    weather = Handle_Weather()
    terrain = Handle_Unexplored()
    encounters = Handle_Encounters(6, NumOfPlayers)
    Create_Day_Writeup_Unexplored(weather, terrain, encounters)

def Create_Day_Writeup_Unexplored(Weather, Terrain, Encounters):
    print(Weather)
    print(Terrain)
    if(Encounters != 0):
        print("ENCOUNTERS!")
        print("P/D/C")
        print(Encounters)
    print("\n")

def Create_Day_Writeup_Explored(Weather, Encounters):
    print(Weather)
    if(Encounters != 0):
        print("ENCOUNTERS!")
        print("P/D/C")
        print(Encounters)
    print("\n")

def Handle_Encounters(NumberOfEncounters, numOfPlayers):
    random.seed
    Encounters = []
    actualEncounters = 0
    while NumberOfEncounters > 0:
        EncounterVal = random.randint(1, 20)
        if(EncounterVal <= 2):
            actualEncounters +=  1
        NumberOfEncounters -= 1
    if actualEncounters > 0:
        while(actualEncounters != 0):
            ##We create our encounters here, select a player that is on watch
            triggerPlayer = random.randint(1, numOfPlayers)
            difficulty = random.randint(1,20)
            creature = random.randint(1,100)
            Encounters += (triggerPlayer, difficulty, creature)
            actualEncounters -= 1
        return Encounters
    else:
        return 0

def Handle_Unexplored():
    ##Take players, run watches, handle encounters if need be
    selectedTerrain = Select_Event(TERRAINS)
    return selectedTerrain

def Handle_Weather():
    selectedWeather = Select_Event(WEATHERS)
    return selectedWeather

#Get the weight of any standard element
def Get_Weight(Elements = ()):
    totalWeight = 0
    for i in Elements:
        totalWeight += i[1]
    return totalWeight

#Select Event helper func
#Return selected element
def Select_Event(Elements = []):
    #We generate
    weight = Get_Weight(Elements)
    #Init and trigger rng
    random.seed()    
    selectedValue = random.randint(0, weight)
    currValue = 0
    returnElement = 0

    for element in Elements:
       minValue = currValue
       currValue = currValue + element[1]
       maxValue = currValue - 1
       if selectedValue >= minValue and selectedValue <= maxValue:
           returnElement = element
           break
    return returnElement

if __name__ == '__main__':
  main()






