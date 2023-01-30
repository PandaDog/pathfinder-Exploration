#!/usr/bin/python
__author__ = "Panda-Dog"
__version__ = 0.1
__copyright__ = "All Rights Reserved"
__email__ = "rgmckay@nevada.unr.edu"

# TODO
# 1. Change lists to a txt file to ease editing
# 2  Create output macro to insert Roll20 of the events (Excluding encounters)
# 3  Enable unique party support, user supplies list of party names so output is more streamlined
# 4  Develop the Dark Souls experience

##IMPORTS##
import sys
import random
import math
import pprint
import sys
import os
import random
import math
import pprint
import json
import easygui
import UnweightedTables
import WeightedTables
import printart


# Main Function


def main():
    MainFunc()


def MainFunc():
    Bulk_Adventure()
    input("Press Enter to Exit")


## HELPER FUNCTIONS ####### HELPER FUNCTIONS ####### HELPER FUNCTIONS ####### HELPER FUNCTIONS ####### HELPER FUNCTIONS ####### HELPER FUNCTIONS ####### HELPER FUNCTIONS ####### HELPER FUNCTIONS ####### HELPER FUNCTIONS ####### HELPER FUNCTIONS #####

# MODES
def Bulk_Adventure():
    exploredCount = int(input("Input number of explored hexes: "))
    unknownHexCount = int(input("Input number of unexplored hexes: "))

    if(exploredCount != 0 or exploredCount < 0):
        print(printart.exploredArt + "\n")
    # Iterate through all explored hex encounters first, then all unexplored
        while exploredCount > 0:
            Travel_Explored()
            exploredCount -= 1

    if(unknownHexCount != 0 or unknownHexCount < 0):
        print("---------------------------------------------------------------------------------------")
        print(printart.unExploredArt + "\n")
        print("---------------------------------------------------------------------------------------\n\n")

        while unknownHexCount > 0:
            Travel_UnExplored()
            unknownHexCount -= 1

    print("ADVENTURE COMPLETE")


def Travel_Explored():
    weather = Handle_Weather()
    encounters = Handle_Encounters(3, "Standard")
    Create_Day_Writeup_Explored(weather, encounters)


def Travel_UnExplored():
    weather = Handle_Weather()
    terrain = Handle_Unexplored()
    encounters = Handle_Encounters(8, terrain)
    Create_Day_Writeup_Unexplored(weather, terrain, encounters)


def Create_Day_Writeup_Unexplored(Weather, Terrain, Encounters):
    print("---------------------------------------------------------------------------------------")
    dayWeather = Weather[0]
    dayTerrain = Terrain[0]
    print(dayWeather)
    print(dayTerrain)
    Generate_Roll20_Macro_Complete(dayWeather, dayTerrain)
    if(Encounters != 0):
        print("ENCOUNTERS!")
        print(Encounters)
    print("\n")


def Create_Day_Writeup_Explored(Weather, Encounters):
    print("---------------------------------------------------------------------------------------")
    dayWeather = Weather[0]
    print(dayWeather)
    Generate_Roll20_Macro_Complete(dayWeather, "Explored")
    if(Encounters != 0):
        print("ENCOUNTERS!")
        print(Encounters)
    print("\n")


def Handle_Encounters(NumberOfEncounters, terrain):
    random.seed
    Encounters = []
    actualEncounters = 0
    encounterThreshold = 1
    unfavorableConditions = True

    if(terrain == "Mountain" or terrain == "Swamp/Marsh" or terrain == "Forest"):
        encounterThreshold = 5

    while NumberOfEncounters > 0:

        EncounterVal = random.randint(1, 20)

        # If we don't get any rolls above 10, add unfavorable conditions
        if(EncounterVal >= 10):
            unfavorableConditions = False

        if(EncounterVal <= encounterThreshold):
            actualEncounters += 1
        NumberOfEncounters -= 1

    if actualEncounters > 0:
        while(actualEncounters != 0):

            monster = Handle_Encounter_Monsters()
            Encounters += (monster, unfavorableConditions)
            actualEncounters -= 1

        return Encounters

    else:
        NonComboEvent = Select_Event(WeightedTables.ENCOUNTER_TYPE)

        eventType = NonComboEvent[0]
        if(eventType == "Secret/Rumor" or terrain == "Forest"):
            NonComboEvent = Select_Event(WeightedTables.MAJOR_RUMORS)

        return NonComboEvent


def Handle_Unexplored():
    # Take players, run watches, handle encounters if need be
    selectedTerrain = Select_Event(WeightedTables.TERRAINS)
    return selectedTerrain


def Handle_Weather():
    selectedWeather = Select_Event(WeightedTables.WEATHERS)
    return selectedWeather


def Handle_Encounter_Monsters():
    EncounterDiff = Select_Event(WeightedTables.ENCOUNTER_DIFFICULTY)
    if(EncounterDiff == "Hard"):
        return Select_Event(WeightedTables.LEVEL_3_FIGHT_HARD_EPIC)
    elif(EncounterDiff == "Medium"):
        return Select_Event(WeightedTables.LEVEL_3_FIGHT_MEDIUM)
    else:
        return Select_Event(WeightedTables.LEVEL_3_FIGHT_HARD_EPIC)


def Get_Weight(Elements=()):
    totalWeight = 0
    for i in Elements:
        totalWeight += i[1]
    return totalWeight

# Select Event helper func
# Return selected element


def Select_Event(Elements=[]):
    # We generate
    weight = Get_Weight(Elements)
    # Init and trigger rng
    random.seed()
    selectedValue = random.randint(0, weight-1)
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

# Example Macro &{template:default} {{name=Yharmem swings a rusty blade!}} {{Falchion:=[[d20cs>15+8]] vs AC}}  {{Damage:=[[2d4+11]]}}


def Generate_Roll20_Macro(message):
    print("&{template:default} {{" + message + "}}" + '\n')


def Generate_Roll20_Macro_Complete(Weather, Terrain=None):
    if(Terrain != None):
        print("&{template:default} {{name=Hvitfjord Travel}}{{" +
              Weather+"}}{{"+Terrain+"}}" + '\n')
    else:
        print(
            "&{template:default} {{name=Hvitfjord Travel}}{{"+Weather+"}}" + '\n')

###################################################################################


if __name__ == '__main__':
    main()
