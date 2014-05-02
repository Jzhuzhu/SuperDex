__author__ = 'jamescheng'

#!/usr/bin/env python

import os, sys, getopt, time, datetime
import glob, operator
from collections import defaultdict
from pokemon.models import *

def importpoke():
    try:
        pokeFile = open("../db/Pokemon_db.txt", "r")
    except OSError:
        print("Error opening Pokemon.txt")
        sys.exit(1)

    while True:
        pokeLine = pokeFile.readline()

        if len(pokeLine) == 0:
            pokeFile.close()
            break

        Tokens = pokeLine.split(",")
        if len(Tokens) != 26:
            print("Data for ", Tokens[0], "corrupted")
            continue

        if Tokens[0] == "Name":
            continue

        p = Pokemon()
        p.name = str(Tokens[0])
        p.nickname = Tokens[1]
        p.number = int(Tokens[2])
        p.imageurl = Tokens[3]
        #p.type = Tokens[4]
        p.genderratio = Tokens[5]
        p.catchrate = Tokens[6]
        p.egggroups = Tokens[7]
        p.height_ft = Tokens[8]
        p.height_m  = Tokens[9]
        p.weight_lbs = Tokens[10]
        p.weight_kg = Tokens[11]
        p.evhp = int(Tokens[12])
        p.evattack = int(Tokens[13])
        if Tokens[14].isdigit():
            p.evdefense = int(Tokens[14])
        else:
            p.evdefense = 0

        if Tokens[15].isdigit():
            p.evspattack = int(Tokens[15])
        else:
            p.evspattack = 0

        if Tokens[16].isdigit():
            p.evspdefense = int(Tokens[16])
        else:
            p.evspdefense = 0

        p.evspeed = int(Tokens[17])
        
        if Tokens[18].isdigit():
            p.basefriendship = int(Tokens[18])
        else:
            p.basefriendship = 0
        p.basehp = int(Tokens[19])
        p.baseattack = int(Tokens[20])
        p.basedefense = int(Tokens[21])
        p.basespattack = int(Tokens[22])
        p.basespdefense = int(Tokens[23])
        p.basespeed = int(Tokens[24])
        p.basetotal = int(Tokens[25])

        p.save()
        #print p.name, "saved to database"

    print(Pokemon.objects.count(), "Pokemons loaded")

def importabil():
    try:
        abilFile = open("../db/Ability.txt", "r")
    except OSError:
        print("Error opening data file")
        sys.exit(1)

    while True:
        abilLine = abilFile.readline()

        if len(abilLine) == 0:
            abilFile.close()
            break

        Tokens = abilLine.split(",")

        a = Ability()
        a.ability_id = int(Tokens[0])
        a.name = Tokens[1]
        a.description = Tokens[2]

        a.save()

        print("Ability" , a.ability_id, "saved to database")

    print(Ability.objects.count(), "Abilities loaded")

def importmoves():
    try:
        movesFile = open("../db/Moves.txt", "r")
    except OSError:
        print("Error opening data file")
        sys.exit(1)

    while True:
        movesLine = movesFile.readline()

        if len(movesLine) == 0:
            movesFile.close()
            break

        Tokens = movesLine.split(",")

        if len(Tokens) != 8:
            print("Data for move ", Tokens[1], "corrupted")
            continue

        if Tokens[0] == "move_id":
            continue

        m = Moves()
        m.move_id = int(Tokens[0])
        m.name = Tokens[1]
        m.move_type = Tokens[2]
        m.category = Tokens[3]
        m.pp = int(Tokens[4])
        m.power = Tokens[5]
        m.accuracy = Tokens[6]
        m.gen = Tokens[7]

        m.save()

        print("Move" , m.move_id, "saved to database")

    print(Moves.objects.count(), "Moves loaded")

def importlearn():
    try:
        learnFile = open("../db/canlearn.txt", "r")
    except OSError:
        print("Error opening data file")
        sys.exit(1)

    prevID = -1
    while True:
        learnLine = learnFile.readline()

        if len(learnLine) == 0:
            learnFile.close()
            break

        Tokens = learnLine.split(",")

        if Tokens[0] == "pokemon_id":
            continue

        pokemonID = int(Tokens[0])
        if pokemonID != prevID:
                print("Learnset for Pokemon", prevID, "load complete")
                prevID = pokemonID

        c = can_learn()
        c.pokemon_id = Pokemon.objects.get(pk=pokemonID)

        moveID = int(Tokens[1])
        c.move_id= Moves.objects.get(pk = moveID)

        c.save()

        #print "Ability" , a.learnity_id, "saved to database"

    print(can_learn.objects.count(), "Abilities loaded")
    
def importhasAbil():
    try:
        hasAbilFile = open("../db/hasability.txt", "r")
    except OSError:
        print("Error opening data file")
        sys.exit(1)

    while True:
        hasAbilLine = hasAbilFile.readline()

        if len(hasAbilLine) == 0:
            hasAbilFile.close()
            break

        Tokens = hasAbilLine.split(",")

        h = has_ability()
        h.ability_id = Ability.objects.get(pk = int(Tokens[0]))
        h.pokemon_id = Pokemon.objects.get(pk = int(Tokens[1]))

        h.save()

        #print "Ability" , a.hasAbility_id, "saved to database"

    print(has_ability.objects.count(), "Ability relations loaded")
    
if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SuperDex.settings")

    main()
