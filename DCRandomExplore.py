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
    ("Nothing", 30),
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
    (("Lycanthropes reside deep in the forest, protecting themselves and others with their seclusion. Recently a werewolf was accused of murder in a nearby town and the militia has begun invading the forest to find the lycanthrope village."), 1),
    (("The dryads of the forest are nowhere to be seen and the druids who visit them are losing power. The dryads were the source of the druids’ power and without them, the forest loses those who defend it."), 1),
    (("Crystalline fungus has started growing, releasing tiny crystals instead of spores. When these crystals attach to living creatures they sap the energy from and cover people all over until they fall into a coma."), 1),
    (("As a defensive measure, the pixies have caused their villages to go invisible to protect them against the invading orcs. However, they now ambush any who come near, friend or foe in fear of being discovered and attacked."), 1),
    (("Harpies have recently moved into the forest and are killing too many local fauna to sustain themselves. This is disrupting the ecology of the forest and many other creatures are beginning to go hungry or leave the forest."), 1),
    (("After centuries of staying in and protecting the forest, the centaur tribes have finally resumed their nomadic patterns and are beginning to leave, leaving the other inhabitants of the forest susceptible to attack from hated foes."), 1),
    (("Oversized insects are running amok, leaving the forest and then returning to it after they wreak havoc all over. A fairy was seen riding an oversized wasp among the swarm of bugs."), 1),
    (("The underbrush grows around travelers, making travel difficult in the forest. Just last week someone was found dead, cocooned in flora, likely suffocated and crushed."), 1),
    (("An ancient elf welcomes all who make it to his shanty in the forest, happily selling and exchanging magic items with them. Part of the deal always includes the customer giving up something they love or there is no deal."), 1),
    (("The land throughout the forest rips and tears, revealing a river of lava that now flows through. Fire elementals make their way out attacking the forest and its inhabitant, but water, wind, and earth elementals fight back against their fiery kin."), 1),
    (("A man is seen gracefully dancing on water as though it were land. Suddenly, a clawed hand reaches up out of the water and grabs him down by the leg and he screams out in horror."), 1),
    (("A flutter of crimson butterflies blocks the dirt path to the creek, going into a maddening frenzy whenever someone approaches. Suddenly, the butterflies then open and close their wings, spelling out the word “Teeth” before flying away."), 2),
    (("The local alchemist has been discarding expired potion bottles by mixing them into his garden compost and dumping them into the stagnant pond behind his house. Not only are the crops gigantic, but the pond’s surface is a thick sludge. Now a large bubble is rising to the surface…"), 2),
    (("in the middle of a deep forest, a well sits among what appears to have once been a lovely glade. Now, the trees around it are dying and rotting on the spot, and light appears to struggle to reach the glade."), 2),
    (("local children have been going missing. They’re found wandering on the edge of the woods. They seem altered somehow and they tell stories of a witch who has been using them in her strange magics."), 2),
    (("A bounty hunter tracks his target."), 2),
    (("A homestead has delicious apples drooping just over a fence. The house is protected by a magical ward, but what is triggered when a single apple is taken?"), 2),
    (("A monstrous mount lumbers across the trail. It is ridden by a gnome."), 2),
    (("The local potentate has declared a hunting contest. There is a rare elusive creature inhabiting the local forest. They offer a reward for proof of its destruction. However, a mysterious visitor to the area is offering an equal reward for keeping it safe."), 2),
    (("A smiling stranger roasts rats, frogs, and squirrels on sticks. He offers a bite to the PCs."), 2),
    (("A chatty bard runs across the party. Time for an exposition dump!"), 2),
    (("There have been threats against a local noble. They require an escort to get them safely through the mysterious forest to the next larger town."), 2),
    (("Goblin hovels are popping up throughout the woods. Investigation yields that they’re all interconnected with a complex network of tunnels, and one tunnel goes much deeper underground than the rest…"), 2),
    (("A naked bard asks for directions to the nearest inn where he left his clothes and money."), 2),
    (("A mischievous Boggle has taken up residence in a small valley where locals pick herbs and plants for potions and magical components. Though the pranks the Boggle has been employing have been mostly harmless, things are changing…"), 2),
    (("Lizardfolk have been seen carving strange runes into the trees of the forest. No one has been able to decipher their meaning."), 2),
    (("An old man from a local village recently murdered his wife in cold blood, screaming that, “The trees told me to do it. The trees!” Three days later, a young farm girl whispers, “The trees speak and I listen.”"), 2),
    (("A door has appeared in the base of a mighty willow tree. The door has been locked for centuries, but one morning the door is wide open. Is it an invitation to enter? Or did something exit?"), 2),
    (("The PCs feel like they are being followed as they stroll through the woods. Who is hunting them?"), 2),
    (("A small village has reported that small fissures have opened up in the ground in the local forest. Stories of Drow patrols at night, once used to frighten children, now give all ages pause. A brash, famed spelunker left ten days ago to explore one of the new caves, but has not returned."), 2),
    (("A pile of brush covers a sinkhole that chutes the party on a slalom slide down into old pirate’s tunnels."), 2),
    (("As you walk down a forest trail, you hear whistles that repeat throughout the trees. When a member of your party steps off the trail, the whistling stops."), 2),
    (("There is a traveling caravan of halflings making its way through the valley. They sell trinkets, put on plays, and tell delightful stories and sing songs for a small fee. It’s really quite fun. And yet, there’s something odd about their impromptu camp at night."), 2),
    (("A shopping list for potions lies on the forest floor."), 2),
    (("A mysterious bench has appeared on the edge of the forest, pointing towards the trees. A small box rests on top of the bench, filled with deliciously sweet confections and a note that reads: “Life.” Eating one provides a random magical effect–who put these here?"), 2),
    (("An arrow strikes a tree trunk just above you, a message wrapped around the shaft."), 2),
    (("Autumn arrives, but none of the leaves have changed color. In fact, new shoots and buds are growing from the branches. The increased foliage becomes thick enough to allow walking on the canopy, leading to some people setting up residence atop the trees. What will happen when winter arrives?"), 2),
    (("The local forest beekeeper is searching for some rare hybrids that lie deeper within the forest. Rumor has it that they will make the best honey in all the land, but they are incredibly poisonous."), 2),
    ((" As the party walks down a rather wide trail, they are suddenly struck by the overall quiet. Then they look back, and realize that the path behind them has been covered by near impenetrable Forest growth. It was seemingly instantaneous, and what’s worse is that the path seems to be narrowing. Ahead, you see a strange, green fire."), 2),
    (("An owlbear makes its nest in the brambles. It’s only trying to protect its eggs."), 2),
    (("Foragers from a secluded village found human remains in a nearby swamp a few weeks ago. The villagers buried the remains following their funeral rites and customs. However, they now report that the spirit of a young lady haunts the village. It doesn’t appear to be malevolent, but the villagers are frightened and unnerved by her presence."), 2),
    (("The Burned Path is only ‘ablaze’ for three days in the year. During that time, dozens of hopefuls attempt to traverse the intensely blazing leaves. At the end of the path is a hot springs occupied by a powerful Efreeti named Iripir. Would you seek her blessings?"), 2),
    (("The Emerald Wall seems to be endless. Fog covers the end on the horizon but never subsides. What could possibly be contained behind its foliage?"), 2),
    (("There is a forest where few dare to tread. People leave its borders feeling weak and sapped of strength, while the trees appear more vibrant. During the autumn, the leaves have such a concentrated blood-red hue…"), 2),
    (("We woke up one day and the world was different. Vibrant. Surreal. Like everything was painted with an intricate brush. And the sky…blazing. The color of an overripe melon. What happens when the stars have no need of sleep?"), 2),
    (("As the war raged, it became difficult for Sersia to find a safe haven. Her resources were running low, especially with the horse. But her cargo was precious, and nobody could find out that she was bringing it to the revolutionaries."), 2),
    (("There is a mighty oak known as the Sacred Eye. People from all over the world make pilgrimages to have their future told by the wise tree. The prophecies always come true, just not always for the person asking."), 2),
    (("The forest has crept and expanded, consuming all nearby structures except one. A deep thrumming can be heard as you approach, and the vines struggle to maintain their grip on the loose stones."), 2),
    (("At the peak of the World’s Palm, the rock stretches upwards like a sprawling tree, melding into the heavens. Nobody has dared climb into the swirling branches, but the potential for great power beckons."), 2),
    (("In the middle of a forest, it is said, stands a man made of Stone. Carved from Nature’s Cradle, he watches in silent vigil and guards the birthplace of the natural spirits."), 2),
    (("The Fractal Woods are a kaleidoscope of chromatic reflections, but after the sun sets, the only thing reflected is the darkness…"), 2),
    (("Just outside town, the ground has sprouted an endless sea of purple flowers that ripple in the breeze. When you investigate, however, you realize that these aren’t blossoms; they are millions of tiny, floral creatures huddled in unison."), 2),
    (("Legend tells of the Tarnished Tree, a towering spruce encased perfectly in gold. Metal rusts when it gets too close, and many have died attempting to claim its riches…"), 2),
    (("You see a man-sized shadow just up the trail waving its arms at you. “Over here, quickly, I’ve caught one!”"), 2),
    (("Deep within the forest, legend tells of a beast that rules with an iron hoof. It is said that when the time comes, he shall lead the wilderness in an uprising against hunters, trappers, and all who invade the woods. Several people are missing."), 2),
    (("When a strange fruit grows on a nearby tree, the town is torn between eating it or burning it. You feel an unnatural craving for the colorful flesh…"), 2),
    (("Every seed that is planted grows into corn. Tomatoes, beans, strawberries – no matter how close an eye is kept on the ground, only corn emerges. It’s exceptionally delicious, but it is a curious thing."), 2),
    (("Strange vines have begun constricting the foliage at the oasis, and the plants begin to wither. Voices are coming from within, whispering words about broken promises and false friends."), 2),
    (("There is a place where two roads meet and everything is just a little more pale on one side versus the other. Greener grass, bluer skies, and clearer streams. What could be causing such a vast vibrancy difference?"), 2),
    (("An ancient tree once stood next to the smithy, but overnight it was sucked into a giant sinkhole."), 2),
    (("A local lumberjack started chopping down a new area of forest. Every tree is completely hollow."), 2),
    (("This is the mysterious Tanglewood, a place inhabited by fae and ruled by their Queen, Ilysare. She is a prolific expert in dreamweaving and the subtle art of suggestion."), 2),
    (("There’s a witch living in an edible house in the middle of the woods. Further investigation reveals the house to be alive, and she’s merely a prisoner."), 2),
    (("A voice whispers softly next to your ear, “The Great Slumber shall soon be upon us.” You look around, but the only living thing nearby is a tiny butterfly, fluttering lightly on the breeze."), 2),
    (("All of the tree limbs are growing straight vertically towards the sky. Sunlight pierces the canopy, creating thick columns between the trunks."), 2),
    (("Alleged bandits have created a small community of tents in the forest. They have very low internal crime, and the mayor wants you to learn their secrets."), 2),
    (("Rumor is spreading of a huge centipede that’s been devouring wolves and deer. It hides in the forest, sleeping by day."), 2),
    (("Instead of yielding abundant crops, a varying assortment of flowers blanket the farmers’ fields. When burned, they regrow overnight."), 2),
    (("There’s an invisible wall on the forest path. Once you pass through it, you can’t seem to go back – some kind of curse. People on the original side can’t see or hear you. Better find a way to break this barrier!"), 2),
    (("Don’t go into the woods alone. There are stories…people see things in the birch trees. Their trunks shift and sway; it’s not natural. And sometimes…sometimes the people don’t return. All that’s left is the chattering of teeth…"), 2),
    (("Every year the animals migrate. Not because of climate or predators, but for an annual meeting in the mountains. They always follow the same path, a bright orange trail that cuts through the tall grass."), 2),
    (("A tree trunk blocks the forest path. Its diameter isn’t wide, but it’s unnaturally heavy and hard to move."), 2),
    (("An intelligent group of squirrels have learned how to use slings and they’re throwing stones at anyone entering their domain without permission."), 2),
    (("Harvesting season for the apple grove is full swing. Workers from all over have come to get their seasonal coin before the chill of late fall turns into winter. Peaceful Kobolds and Goblins are not uncommon among the workforce. However, a group of local ruffians are threatening to ransack their camp because they don’t want “their kind” here"), 2),
    (("A faction of dryads is in the middle of a war, making the forests extremely dangerous and stifling trade routes."), 2),
    (("A human druid Alic Hokkland died in a mysterious alchemical fire in the swamp a couple of years ago. Since then, strange rumors throughout the forest suggest a woodland swamp creature protects, or haunts as some suggest, the bog where Hokkland met his demise. A local logger has put out a bounty, for killing the creature."), 2),
    (("Rainclouds are perpetually located over a section of the forest, but the raindrops never reach the forest floor. The local wizard, Quinnup assumes portal hi-jinx, but is too afraid to investigate."), 2),
    (("The great oak has blossomed leaves of tremendous color. Magenta, azure, and puce adorn its branches. Which would be great, except birds refuse to roost among the leaves, and it’s giving off a foul odor."), 2),
    (("A young boy has gone missing from his farm. Everyone assumes him dead, except his mother swears she can still hear him. Turns out, there’s a tunnel system under the farm where a creature is holding him hostage."), 2),
    (("The nearby forest has begun to glow. Oddly enough, the blacksmith’s forge is filled with sap. And is that…syrup you smell?"), 2),
    (("When an ancient jade mask is excavated from a long-forgotten burial site, the archaeologists are perplexed. Everyone who has held it up to their face has been plagued with bouts of delirium and memory loss."), 2),
    (("A pack of wolves has taken in a young girl to raise as one of their own. They’re highly sophisticated, using silverware and everything."), 2),
    (("The swamps have begun bubbling incessantly, and the waters are warm to the touch. It’s driving the frogs and dragonflies away, but something peculiar lurks in the deep and the dark."), 2),
    (("A fish wriggles about on the forest path. Nobody is sure where it came from, but it’s definitely alive."), 2),
    (("Pine cones have been replaced by rare and exotic fruit. It’s unusual and unexpected, but word is spreading and merchants are flocking to the area to lay claim to the rare goods."), 2),
    (("The local woodsmen have complained about breaking their axes far more frequently than usual. The tree bark is hearty and they’re denting the axe heads every other day."), 2),
    (("A message in a bottle washes up along the forest stream. It contains a map to a legendary treasure, but the starting location isn’t clear at all."), 2),
    (("As your party approaches a clearing, they are met by a group of what they initially thought to be wild horses. Upon closer look, these horses are all wearing saddles. One saddle still has what appears to be a human leg attached."), 2),
    (("A local trapper has reported sightings of several will-o-wisps out in the swamps. They coincide with recent disappearances in the area. She is very protective of what she’s targeting with her traps."), 2),
    (("Every 100 years, the owl conclave meets to discuss matters of the forest. It’s supposed to be happening tonight, but the only possible sign of the owls is a substantial pile of dead mice stacked up on the path."), 2),
    (("When the moonlight shines on a specific section of trees, they appear to be rotten and dead."), 2),
    (("A long line of cows tied together are wandering aimlessly through the forest. There haven’t been any reports of missing livestock, and their brand isn’t recognizable."), 2),
    (("Thirteen leaves are arranged in a circle in a forest glade. Each holds a small amount of hot chicken broth."), 2),
    (("A new, bright purple mushroom has sprouted from the base of a hemlock tree. Every several seconds, it puffs out a cloud of spores. Are the trees starting to look purple to you?"), 2),
    (("A group of bandits rushes into town. Turns out, while waiting to ambush hapless travelers, THEY got ambushed! Are they worth helping out?"), 2),
    (("A little girl is watching you from the trees. The next time you glance over, you see a wolf run away."), 2),
    (("The trees have linked their branches together in a network fashion, and they’re sending communications incredibly quickly throughout the forest. Some people want to take advantage of this new development."), 2),
    (("A worn rope hangs down from one of the tallest trees in the forest. It seems sturdy enough…"), 2),
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

        eventType = NonComboEvent[0]
        if(eventType == "Secret/Rumor"):
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
        return Select_Event(LEVEL_3_FIGHT_MEDIUM)
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
