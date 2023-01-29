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


# Wanna add a fun weather? Add it here!
WEATHERS = {
    ("Thirty-three degrees. Clear blue skies despite the cold.", 15),
    ("Sixty-six degrees. Warm sunny day with a pleasant breeze.", 10),
    ("Fifty-nine degrees. Very warm day, partly cloudy.", 10),
    ("Negative Five degrees, all water has a sheet of ice on it. Make a fortitude save", 5),
    ("Heavy Fog rolls around you. Take a -1 on Perception checks. Ranged attacks incur a -2 penalty to hit", 8),
    ("Cold day. You see your breath as you exhale.", 7),
    ("The sky is dark and looks like a storm is coming as it blocks out the sun. Treat day encounters as if nighttime.", 10),
    ("Snowstorm, Treat all terrain as difficult terrain.", 8),
    ("Blizzard! Treat all terrain as difficult terrain. This snow is heavy and wet and soaks through your clothing. Roll a fortitude save", 5),
}

# Wanna add a new terrain? Add it here!
TERRAINS = {("STANDARD", 20),
            ("Forest", 10),
            ("Swamp/Marsh", 8),
            ("DIFFICULT TERRAIN", 8),
            ("Mountain", 8),
            ("Minor Point of Interest", 3),
            ("Secret", 3),
            ("Feature", 3)}


ENCOUNTER_TYPE = {
    ("Major Entity", 10),
    ("Nothing", 50),
    ("Faction/NonCombat Encounter", 10),
    ("Point of Interest", 10),
    ("Secret/Rumor", 5),
}

FACTION_TYPE = {
    ("Cult", 4),
    ("Bandits", 4),
    ("Inquisition", 4),
    ("Fey", 4),
    ("Imperial", 4),
    ("Wilderness", 4)
}

ENCOUNTER_DIFFICULTY = {
    ("Hard", 1),
    ("Medium", 1),
}

LEVEL_3_FIGHT_HARD_EPIC = {
    ("Troglodyte Champion", 1),
    ("Sinspawn, Roiling Oil, Nagaji", 1),
    ("2 Forsake Arbalesters, 2 Deinonychus", 1),
    ("Deinotherium, Reflavored as a Corrupted Unicorn", 1),
    ("Drider injured in a cave (no legs) and Bone Worm Swarm under her command", 1),
    ("Gorthek Rider x2. Reflavored as Sons of the Fjord", 1),
    ("Lizardfolk Stalker, Boreal Manticore, Lizardfolk Beserker", 1),
    ("2 Gnolls and 2 Blood Caterpillars [Slavers with worms]", 1),
    ("3 Medium Earth Elementals", 1),
    ("2 Large Earth Elementals", 1),
    ("2 Manticore, Mating pair.", 1),
    ("EPIC ENCOUNTER: Wraithwing, Tanuki Necromancer, Calathgarx2", 1),

}

LEVEL_3_FIGHT_MEDIUM = {
    ("Stymphalides Swarm", 1),
    ("Grizzled Rider", 1),
    ("Darkmantle, Bramblelash, Dark Dancerx2", 1),
    ("2 Unicorns, 2 Gnolls. Gnolls trying to tame the unicorns to convert into Deinotheriums. If Gnolls or Unicorn escape roll hard encounter following day.", 1),
    ("Juvenile Rukh, 2 Vampire Mist", 1),
    ("Oronci", 1),
    ("Gear Ghost", 1),
    ("Gorthek Rider", 1),
    ("Anhana, 2 Moose  CAN BE DIPLOMACY'D TO NOT FIGHT", 1),
    ("Orphne, 4 Dark Dancers dancing around the Orphne", 1),
    ("1 Mythic Ogre, 1 Carbuncle. Party finds them cooking a deer at the fire", 1),
    ("1 Manticore, Hunting", 1),
    ("2 Wikkawaks, followers of the Wendigo legend. Ambush at night", 1),
    ("2 Boggard Brute, Patrolling Kingsmen", 1),
    ("1 Flind, 6 Gnolls, Hunting Party", 1),
    ("1 Ettin", 1),
    ("1 Cave Giant", 1),
}

MAJOR_RUMORS = {
    (("Reports of children being lured into the forest by short, goat-legged men have grown rampant. Any satyr questioned about this claims to not know about it and divination magic confirms they are telling the truth."), 1),

    (("A travelling circus has recently shown up in the town. Promising festivities for the locals but has caused increased suspicion from the local guard and town magistrate due to advertisements of dangerous beasts as one of the many attractions."), 1),

    (("Many creatures of the forest are being found petrified in stone. While mostly small animals like squirrels and beavers have been found, some elk have been found petrified, broken apart, and missing pieces."), 1),

    (("People traveling near the forest claim to see a unicorn galloping out near the tree line. However according to legends, unicorns died out centuries ago and these sightings are dismissed as wild horses."), 1),

    (("People trying to travel through the forest keep winding up turned around and back out where they started within minutes of entering. Their compasses and other navigation gear all spin around or otherwise go crazy inside."), 1),

    (("Lizardfolk have started to invade the forest and their shamans have begun corrupting the land. Wherever the lizardfolk go the ground becomes swampy and marshlike and the flora warps to match the landscape."), 1),

    (("A long-dormant treant of the forest has finally woken, speaking in an archaic language and heading out of the forest toward the nearest town. The other inhabitants of the forest have no idea where it is going or why."), 1),

    (("An ornate archway was found seemingly out of place in the middle of a clearing. Getting close to it makes images of a ruined city flicker inside, giving just enough of a glimpse to make out some details of the ruins."), 1),

    (("Legend says a hag lives deep in forest and will tell you your future in exchange for part of your soul. She apparently came to collect part of the local king’s son’s soul, leaving him in a coma and the king outraged."), 1),

    (("It was discovered taking a dip into a specific part of a river in the forest turns you into an animal temporarily causing people to flock and try it. The last few have yet to change back even days after they turned and people are beginning to panic."), 1),

    (("Occasionally fey versions of different creatures make their way out of the forest, and the latest to be spotted are fey goblins. They have wings made of spider silk, large sharp teeth, and the same anger that fuels their normal kin."), 1),

    (("A second moon is visible only to those standing in the forest. When the moons align, a large magic circle is visible in the main clearing, but no one know what it is for or how to activate it"), 1),

    (("Elves in the forest say they noticed a change in their archfey’s demeanor and they are concerned. Their previously benevolent patron has been commanding them to prepare for war and slaughter and intruders, though not many have complied with her wishes."), 1),

    (("The Earthstone, a magic artifact that provides magic to the forest, was stolen in the dead of night. Now the forest begins to wane in power and the need to recover the Earthstone is of dire importance to the forest’s inhabitants."), 1),

    (("Lycanthropes reside deep in the forest, protecting themselves and others with their seclusion. Recently a werewolf was accused of murder in a nearby town and the militia has begun invading the forest to find the lycanthrope village."), 1),

    (("The dryads of the forest are nowhere to be seen and the druids who visit them are losing power. The dryads were the source of the druids’ power and without them, the forest loses those who defend it."), 1),

    (("Crystalline fungus has started growing, releasing tiny crystals instead of spores. When these crystals attach to living creatures they sap the energy from and cover people all over until they fall into a coma."), 1),

    (("As a defensive measure, the pixies have caused their villages to go invisible to protect them against the invading orcs. However, they now ambush any who come near, friend or foe in fear of being discovered and attacked."), 1),

    (("All the lakes in the forest have frozen over despite the heat, and a mysterious cave has appeared in the center of the largest lake. Whispers of the “Frost Queen” echo throughout the forest, and slowly the rest of the forest begins to show signs of frost and the effects of cold weather."),  1),

    (("Harpies have recently moved into the forest and are killing too many local fauna to sustain themselves. This is disrupting the ecology of the forest and many other creatures are beginning to go hungry or leave the forest."), 1),

    (("After centuries of staying in and protecting the forest, the centaur tribes have finally resumed their nomadic patterns and are beginning to leave, leaving the other inhabitants of the forest susceptible to attack from hated foes."), 1),

    (("Oversized insects are running amok, leaving the forest and then returning to it after they wreak havoc all over. A fairy was seen riding an oversized wasp among the swarm of bugs."), 1),

    (("The underbrush grows around travelers, making travel difficult in the forest. Just last week someone was found dead, cocooned in flora, likely suffocated and crushed."), 1),

    (("An ancient elf welcomes all who make it to his shanty in the forest, happily selling and exchanging magic items with them. Part of the deal always includes the customer giving up something they love or there is no deal."), 1),

    (("The land throughout the forest rips and tears, revealing a river of lava that now flows through. Fire elementals make their way out attacking the forest and its inhabitant, but water, wind, and earth elementals fight back against their fiery kin."), 1),

    (("A man is seen gracefully dancing on water as though it were land. Suddenly, a clawed hand reaches up out of the water and grabs him down by the leg and he screams out in horror."), 1),
}
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
        print(exploredArt + "\n")
    # Iterate through all explored hex encounters first, then all unexplored
        while exploredCount > 0:
            Travel_Explored()
            exploredCount -= 1

    if(unknownHexCount != 0 or unknownHexCount < 0):
        print("---------------------------------------------------------------------------------------")
        print(unExploredArt + "\n")
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
    print(Weather[0])
    print(Terrain[0])
    Generate_Roll20_Macro_Complete(Weather[0], Terrain[0])
    if(Encounters != 0):
        print("ENCOUNTERS!")
        print(Encounters)
    print("\n")


def Create_Day_Writeup_Explored(Weather, Encounters):
    print("---------------------------------------------------------------------------------------")
    print(Weather[0])
    Generate_Roll20_Macro_Complete(Weather[0], "Explored")
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

    if(terrain == "Mountain"):
        encounterThreshold = 4

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
        NonComboEvent = Select_Event(ENCOUNTER_TYPE)
        if(NonComboEvent[0] == "Secret/Rumor"):
            NonComboEvent = Select_Event(MAJOR_RUMORS)
        return NonComboEvent


def Handle_Unexplored():
    # Take players, run watches, handle encounters if need be
    selectedTerrain = Select_Event(TERRAINS)
    return selectedTerrain


def Handle_Weather():
    selectedWeather = Select_Event(WEATHERS)
    return selectedWeather


def Handle_Encounter_Monsters():
    EncounterDiff = Select_Event(ENCOUNTER_DIFFICULTY)
    if(EncounterDiff == "Hard"):
        return Select_Event(LEVEL_3_FIGHT_HARD_EPIC)
    elif(EncounterDiff == "Medium"):
        return Select_Event(LEVEL_3_FIGHT_HARD_EPIC)
    else:
        return Select_Event(LEVEL_3_FIGHT_HARD_EPIC)


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


def loadJson(filepath):
    with open(filepath, 'r') as json_file:
        tmp = json_file.read()
        table = json.loads(tmp)
        return table
        # Example Macro &{template:default} {{name=Shift fires his gun!}} {{Laser Pistol:=[[d20+4]] vs AC}}  {{Damage:=[[1d6+1]]}}


def printJsonTable(table):
    print(json.dumps(table, indent=1))


def Generate_Roll20_Macro(message):
    print("&{template:default} {{" + message + "}}" + '\n')


def generateProblem():
    return grabSimpleData('problem', problems)


def generatePatron():
    return grabSimpleData('patron', patrons)


def generatePlace(isWild=False):
    reward = random.choice(places["places"]["rewards"])

    if isWild == False:
        civilizedOngoings = random.choice(
            places["places"]["civilizedOngoings"])
        wildernessOngoings = ''
    else:
        wildernessOngoings = random.choice(
            places["places"]["wildernessOngoings"])
        civilizedOngoings = ''

    hazardCategory = random.randint(0, len(places["places"]["hazard"]))

    hazardExample = random.choice(
        places["places"]["hazard"][hazardList[hazardCategory]]["specificExample"])

    hazardPotDanger = random.choice(
        places["places"]["hazard"][hazardList[hazardCategory]]["possibleDanger"])

    print(civilizedOngoings + wildernessOngoings + ' ' +
          hazardCategory + ' ' + hazardExample + ' ' + hazardPotDanger + reward)


def generateUrbanEncounter():
    return grabSimpleData("urbanEncounters", urbanEncounters)


def generateWildEncounter():
    return grabSimpleData("wildernessEncounters", wildEncounters)


def generateConflict():
    conflictCategory = random.choice(conflictList)

    conflictSituation = random.choice(
        conflictTypes['conflictType'][conflictCategory]['overallSituation'])

    conflictFocus = random.choice(
        conflictTypes['conflictType'][conflictCategory]['specificFocus'])

    print(conflictCategory + ': ' + conflictSituation + ' ' + conflictFocus)


def generateNPC():
    return grabSimpleData('npc', NPC)


def generateSimpleNPC():
    return grabSimpleData("onerollNPC", simpleNPC)


def grabSimpleData(firstElement, table, noParent=False):
    returnVal = []

    if noParent == False:
        for x in table[firstElement]:
            returnVal.append(random.choice(table[firstElement][str(x)]))
        return returnVal
    else:
        for x in table:
            returnVal.append(random.choice(table[x]))


###JSON DECLARATIONS##########################################################################################################
conflictList = ['money', 'revenge', 'power', 'naturalDanger',
                'religion', 'ideology', 'ethnicity', 'resources']

hazardList = ['social', 'legal', 'environmental',
              'trap', 'animal', 'sentient', 'decay', 'PC-induced']

problems = loadJson("problem.json")
patrons = loadJson("patrons.json")
places = loadJson("places.json")
NPC = loadJson("npc.json")
wildEncounters = loadJson("wildernessEncounters.json")
urbanEncounters = loadJson("urbanEncounters.json")
conflictTypes = loadJson("conflictType.json")
simpleNPC = loadJson("onerollNPC.json")
adventureSeeds = loadJson("adventureSeeds.json")

#############################################################################################################

exploredArt = """
  ________   _______  _      ____  _____  ______ _____    _    _ ________   __
 |  ____\ \ / /  __ \| |    / __ \|  __ \|  ____|  __ \  | |  | |  ____\ \ / /
 | |__   \ V /| |__) | |   | |  | | |__) | |__  | |  | | | |__| | |__   \ V / 
 |  __|   > < |  ___/| |   | |  | |  _  /|  __| | |  | | |  __  |  __|   > <  
 | |____ / . \| |    | |___| |__| | | \ \| |____| |__| | | |  | | |____ / . \ 
 |______/_/ \_\_|    |______\____/|_|  \_\______|_____/  |_|  |_|______/_/ \_\ 
                                                                              
                                                                              
"""

unExploredArt = """
  _    _ _   _ ________   _______  _      ____  _____  ______ _____    _    _ ________   __
 | |  | | \ | |  ____\ \ / /  __ \| |    / __ \|  __ \|  ____|  __ \  | |  | |  ____\ \ / /
 | |  | |  \| | |__   \ V /| |__) | |   | |  | | |__) | |__  | |  | | | |__| | |__   \ V / 
 | |  | | . ` |  __|   > < |  ___/| |   | |  | |  _  /|  __| | |  | | |  __  |  __|   > <  
 | |__| | |\  | |____ / . \| |    | |___| |__| | | \ \| |____| |__| | | |  | | |____ / . \ 
  \____/|_| \_|______/_/ \_\_|    |______\____/|_|  \_\______|_____/  |_|  |_|______/_/ \_\ 
                                                                                           
                                                                                           
"""

###################################################################################


if __name__ == '__main__':
    main()
