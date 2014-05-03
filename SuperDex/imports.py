__author__ = 'jamescheng'

#!/usr/bin/env python

import os, sys, getopt, time, datetime, itertools
import glob, operator
from collections import defaultdict
from pokemon.models import *


def importpoke():
    try:
        pokeFile = open("../db/Pokemon_db.txt", "r")
    except IOError, inst:
        print "Error opening Pokemon.txt"
        sys.exit(1)

    while True:
        pokeLine = pokeFile.readline()

        if len(pokeLine) == 0:
            pokeFile.close()
            break

        Tokens = pokeLine.split(",")
        if len(Tokens) != 26:
            print "Data for ", Tokens[0], "corrupted"
            continue

        if Tokens[0] == "Name":
            continue

        p = Pokemon()
        p.name = str(Tokens[0])
        p.nickname = Tokens[1]
        p.number = int(Tokens[2])
        p.imageurl = Tokens[3]
        unsorted = Tokens[4]
        subtoks = unsorted.split("/")
        subtoks.sort()
        good = "/".join(subtoks)
        p.poke_type = poke_type.objects.get(pk = good)
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
        p.basetotal = p.basehp + p.baseattack + p.basedefense + p.basespattack + p.basespdefense + p.basespeed

        p.save()
        print p.name, "saved to database"

    print Pokemon.objects.count(), "Pokemons loaded"

def importabil():
    try:
        abilFile = open("../db/Ability.txt", "r")
    except IOError, inst:
        print "Error opening data file"
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

        print "Ability" , a.ability_id, "saved to database"

    print Ability.objects.count(), "Abilities loaded"

def importmoves():
    try:
        movesFile = open("../db/Moves.txt", "r")
    except IOError, inst:
        print "Error opening data file"
        sys.exit(1)

    while True:
        movesLine = movesFile.readline()

        if len(movesLine) == 0:
            movesFile.close()
            break

        Tokens = movesLine.split(",")

        if len(Tokens) != 8:
            print "Data for move ", Tokens[1], "corrupted"
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

        print "Move" , m.move_id, "saved to database"

    print Moves.objects.count(), "Moves loaded"

def importlearn():
    try:
        learnFile = open("../db/canlearn.txt", "r")
    except IOError, inst:
        print "Error opening data file"
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
                print "can_learn for Pokemon", prevID, "load complete"
                prevID = pokemonID

        c = can_learn()
        c.pokemon_id = Pokemon.objects.get(pk=pokemonID)

        moveID = int(Tokens[1])
        c.move_id= Moves.objects.get(pk = moveID)

        c.TM = Tokens[3]

        c.save()

        #print "Ability" , a.learnity_id, "saved to database"

    print can_learn.objects.count(), "can_learn relations loaded"
    
def importhasAbil():
    try:
        hasAbilFile = open("../db/hasability.txt", "r")
    except IOError, inst:
        print "Error opening data file"
        sys.exit(1)

    while True:
        hasAbilLine = hasAbilFile.readline()

        if len(hasAbilLine) == 0:
            hasAbilFile.close()
            break

        Tokens = hasAbilLine.split(",")

        if not Tokens[0].isdigit():
            continue

        h = has_ability()
        h.ability_id = Ability.objects.get(pk = int(Tokens[0]))
        h.pokemon_id = Pokemon.objects.get(pk = int(Tokens[1]))

        h.save()

        #print "Ability" , a.hasAbility_id, "saved to database"

    print has_ability.objects.count(), "Ability relations loaded"
    
def importlset():
    try:
        lsetFile = open("../db/learnset.txt", "r")
    except IOError, inst:
        print "Error opening data file"
        sys.exit(1)

    #counter= 0
    prevID = 0
    while True:


        lsetLine = lsetFile.readline()

        if len(lsetLine) == 0:
            lsetFile.close()
            break
        #Debug
        #if counter >= 50:
        #    lsetFile.close()
        #    break

        Tokens = lsetLine.split(",")

        if not Tokens[0].isdigit():
            continue

        pokemonID = int(Tokens[0])
        if pokemonID != prevID:
                print "Learnset for Pokemon", prevID, "load complete"
                prevID = pokemonID

        l = learnset()

        l.pokemon_id = Pokemon.objects.get(pk = int(Tokens[0]))
        l.move_id = Moves.objects.get(pk = int(Tokens[1]))
        #print Tokens[3][:-1]
        if Tokens[3][:-1].isdigit():
            l.level = int(Tokens[3][:-1])
            #print l.level
        else:
            l.level = 0

        l.save()

        #counter += 1

    print learnset.objects.count(), "Learnsets loaded"

def importnature():
    try:
        natureFile = open("../db/Nature.txt", "r")
    except IOError, inst:
        print "Error opening data file"
        sys.exit(1)

    while True:
        natureLine = natureFile.readline()

        if len(natureLine) == 0:
            natureFile.close()
            break

        Tokens = natureLine.split(",")

        if Tokens[0] == "Name":
            continue

        n = Natures()
        n.name = Tokens[0]
        n.increased_stat = Tokens[1]
        n.descrease_stat = Tokens[2]

        n.save()

        print "Nature" , n.name, "saved to database"

    print Natures.objects.count(), "Natures loaded"


def importevo():
    try:
        evoFile = open("../db/evo_db.txt", "r")
    except IOError, inst:
        print "Error opening data file"
        sys.exit(1)

    while True:
        evoLine = evoFile.readline()

        if len(evoLine) == 0:
            evoFile.close()
            break

        Tokens = evoLine.split(",")

        if not Tokens[0].isdigit():
            continue

        e = Evolution()
        e.pokemon_id1 = Pokemon.objects.get(pk = int(Tokens[0]))
        e.pokemon_id2 = Pokemon.objects.get(pk = int(Tokens[2]))
        e.how = Tokens[4][1:-1]

        e.save()

        print "Evolution loaded for " , e.pokemon_id1.name

    print Evolution.objects.count(), "Evolutions loaded"

def importtypes():
    try:
        typesFile = open("../db/types_db.txt", "r")
    except IOError, inst:
        print "Error opening data file"
        sys.exit(1)

    while True:
        typesLine = typesFile.readline()

        if len(typesLine) == 0:
            typesFile.close()
            break

        Tokens = typesLine.split(",")

        if len(Tokens) != 19:
            print "Data for Type ", Tokens[0], "corrupted"
            continue

        t = poke_type()
        unsorted = Tokens[0]
        subtoks = unsorted.split("/")
        subtoks.sort()
        good = "/".join(subtoks)
        t.poke_type = good
        t.Normal = float(Tokens[1])
        t.Fighting = float(Tokens[2])
        t.Flying = float(Tokens[3])
        t.Poison = float(Tokens[4])
        t.Ground = float(Tokens[5])
        t.Rock = float(Tokens[6])
        t.Bug = float(Tokens[7])
        t.Ghost = float(Tokens[8])
        t.Steel = float(Tokens[9])
        t.Fire = float(Tokens[10])
        t.Water = float(Tokens[11])
        t.Grass = float(Tokens[12])
        t.Electric = float(Tokens[13])
        t.Psychic = float(Tokens[14])
        t.Ice = float(Tokens[15])
        t.Dragon = float(Tokens[16])
        t.Dark = float(Tokens[17])
        t.Fairy = float(Tokens[18])

        t.save()

        print "Effectiveness of" , t.poke_type, "saved to database"

    print poke_type.objects.count(), "types loaded"

def gentypes():
    typeDict = {}
    typeDict["Normal"] = [1.0,2.0,1.0,1.0,1.0,1.0,1.0,0.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
    typeDict["Fighting"] = [1.0,1.0,2.0,1.0,1.0,0.5,0.5,1.0,1.0,1.0,1.0,1.0,1.0,2.0,1.0,1.0,0.5,2.0]
    typeDict["Flying"] = [1.0,0.5,1.0,1.0,0.0,2.0,0.5,1.0,1.0,1.0,1.0,0.5,2.0,1.0,2.0,1.0,1.0,1.0]
    typeDict["Bug"] = [1.0,0.5,2.0,1.0,0.5,2.0,1.0,1.0,1.0,2.0,1.0,0.5,1.0,1.0,1.0,1.0,1.0,1.0]
    typeDict["Ground"] = [1.0,1.0,1.0,0.5,1.0,0.5,1.0,1.0,1.0,1.0,2.0,2.0,0.0,1.0,2.0,1.0,1.0,1.0]
    typeDict["Rock"] = [0.5,2.0,0.5,0.5,2.0,1.0,1.0,1.0,2.0,0.5,2.0,2.0,1.0,1.0,1.0,1.0,1.0,1.0]
    typeDict["Poison"] = [1.0,0.5,1.0,0.5,0.0,1.0,0.5,1.0,1.0,1.0,1.0,0.5,1.0,2.0,1.0,1.0,1.0,0.5]
    typeDict["Ghost"] = [0.0,0.0,1.0,0.5,1.0,1.0,0.5,2.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,2.0,1.0]
    typeDict["Steel"] = [0.5,2.0,0.5,0.0,2.0,0.5,0.5,1.0,0.5,2.0,1.0,0.5,1.0,0.5,0.5,0.5,1.0,0.5]
    typeDict["Fire"] = [1.0,1.0,1.0,1.0,2.0,2.0,0.5,1.0,0.5,0.5,2.0,0.5,1.0,1.0,0.5,1.0,1.0,0.5]
    typeDict["Water"] = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.5,0.5,0.5,2.0,2.0,1.0,0.5,1.0,1.0,1.0]
    typeDict["Grass"] = [1.0,1.0,2.0,2.0,0.5,1.0,2.0,1.0,1.0,2.0,0.5,0.5,0.5,1.0,2.0,1.0,1.0,1.0]
    typeDict["Electric"] = [1.0,1.0,0.5,1.0,2.0,1.0,1.0,1.0,0.5,1.0,1.0,1.0,0.5,1.0,1.0,1.0,1.0,1.0]
    typeDict["Psychic"] = [1.0,0.5,1.0,1.0,1.0,1.0,2.0,2.0,1.0,1.0,1.0,1.0,1.0,0.5,1.0,1.0,2.0,1.0]
    typeDict["Ice"] = [1.0,2.0,1.0,1.0,1.0,2.0,1.0,1.0,2.0,2.0,1.0,1.0,1.0,1.0,0.5,1.0,1.0,1.0]
    typeDict["Dragon"] = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.5,0.5,0.5,0.5,1.0,2.0,2.0,1.0,2.0]
    typeDict["Dark"] = [1.0,2.0,1.0,1.0,1.0,1.0,2.0,0.5,1.0,1.0,1.0,1.0,1.0,0.0,1.0,1.0,0.5,2.0]
    typeDict["Fairy"] = [1.0,0.5,1.0,2.0,1.0,1.0,0.5,1.0,2.0,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.5,1.0]

    sortedtypeDict = sorted(typeDict)

    type_list = []
    for type in sortedtypeDict:
        type_list.append(type)
    #print type_list

    all_combos = itertools.combinations(type_list, 2)
    combos_list = [list(c) for c in all_combos]
    for combo in combos_list:
        tlist1 = typeDict[combo[0]]
        tlist2 = typeDict[combo[1]]
        if len(tlist1) != len(tlist2):
            print "Corrupted type list for ", combo

        mixtlist = [0.0 for x in xrange(len(tlist1))]
        for i in xrange(len(tlist1)):
            mixtlist[i] = float(tlist1[i]) * float(tlist2[i])

        mixkey = "/".join(combo)
        typeDict[mixkey] = mixtlist

    #for type, tlist in typeDict.iteritems():
    #    print type, ":", tlist

    return typeDict

def importroles():
    try:
        rolesFile = open("../db/roles_db.txt", "r")
    except IOError, inst:
        print "Error opening data file"
        sys.exit(1)

    while True:
        rolesLine = rolesFile.readline()

        if len(rolesLine) == 0:
            rolesFile.close()
            break

        Tokens = rolesLine.split(",")

        if len(Tokens) != 8:
            print "Data for role ", Tokens[1], "corrupted"
            continue

        if not Tokens[0].isdigit():
            continue

        r = Roles()
        r.rID = int(Tokens[0])
        r.name = Tokens[1]
        r.reqStats = Tokens[2]
        r.reqMoves = Tokens[3]
        r.compIDs = Tokens[4]
        r.suggNat = Tokens[5]
        r.impMoves = Tokens[6]
        r.compRoles = Tokens[7]

        r.save()

        print "Role" , r.name, "saved to database with reqStats and compIDs", r.reqStats, r.compIDs

    print Roles.objects.count(), "Roles loaded"
    
    
def populatetypes():
        
    typeDict = gentypes()
        
    for type, tlist in typeDict.iteritems():
        t = poke_type()
        #unsorted = Tokens[0]
        #subtoks = unsorted.split("/")
        #subtoks.sort()
        #good = "/".join(subtoks)
        t.poke_type = type
        t.Normal = tlist[0]
        t.Fighting = tlist[1]
        t.Flying = tlist[2]
        t.Poison = tlist[3]
        t.Ground = tlist[4]
        t.Rock = tlist[5]
        t.Bug = tlist[6]
        t.Ghost = tlist[7]
        t.Steel = tlist[8]
        t.Fire = tlist[9]
        t.Water = tlist[10]
        t.Grass = tlist[11]
        t.Electric = tlist[12]
        t.Psychic = tlist[13]
        t.Ice = tlist[14]
        t.Dragon = tlist[15]
        t.Dark = tlist[16]
        t.Fairy = tlist[17]

        t.save()

        print "Effectiveness of" , t.poke_type, "saved to database"

    print poke_type.objects.count(), "types loaded"

def importall():
    populatetypes()
    importpoke()
    importmoves()
    importabil()
    importhasAbil()
    importlearn()
    importlset()
    importevo()
    importnature()
    importroles()
    for poke in Pokemon.objects.all():
        poke.set_rolestr()
