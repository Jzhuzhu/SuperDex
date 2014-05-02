from django.db import models
from django import forms

# Create your models here.

class poke_type(models.Model):
    poke_type = models.CharField(max_length=20, primary_key=True)

    #Value represents the effectiveness of the Field AGAINST poke_type
    #Example: if poke_type = Fire/Rock, the value of Water is 4
    Steel = models.DecimalField(max_digits=3, decimal_places=2)
    Fire = models.DecimalField(max_digits=3, decimal_places=2)
    Water = models.DecimalField(max_digits=3, decimal_places=2)
    Grass = models.DecimalField(max_digits=3, decimal_places=2)
    Electric = models.DecimalField(max_digits=3, decimal_places=2)
    Psychic = models.DecimalField(max_digits=3, decimal_places=2)
    Ice = models.DecimalField(max_digits=3, decimal_places=2)
    Dragon = models.DecimalField(max_digits=3, decimal_places=2)
    Dark = models.DecimalField(max_digits=3, decimal_places=2)
    Fairy = models.DecimalField(max_digits=3, decimal_places=2)
    Normal = models.DecimalField(max_digits=3, decimal_places=2)
    Fighting = models.DecimalField(max_digits=3, decimal_places=2)
    Flying = models.DecimalField(max_digits=3, decimal_places=2)
    Poison = models.DecimalField(max_digits=3, decimal_places=2)
    Ground = models.DecimalField(max_digits=3, decimal_places=2)
    Rock = models.DecimalField(max_digits=3, decimal_places=2)
    Bug = models.DecimalField(max_digits=3, decimal_places=2)
    Ghost = models.DecimalField(max_digits=3, decimal_places=2)

    def get_effectiveness(self):
        total = []
        normal = []
        weak = []
        immune = []
        resistant = []
        for field in self._meta.fields:
            if field.name == "poke_type":
                continue
            value = getattr(self, field.name)
            if value == 1:
                string = field.name
                normal.append(string)
            elif value > 1:
                string = field.name + " (" + str(value) + "x)"
                weak.append(string)
            elif value == 0:
                string = field.name
                immune.append(string)
            elif value < 1:
                string = field.name + " (" + str(value) + "x)"
                resistant.append(string)
        total.append(normal)
        total.append(weak)
        total.append(immune)
        total.append(resistant)
        return total

    def __str__(self):
        return self.poke_type

class Pokemon(models.Model):
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    number = models.IntegerField(primary_key=True)
    imageurl = models.URLField()
    poke_type = models.ForeignKey(poke_type)
    genderratio = models.CharField(max_length=30)
    catchrate = models.CharField(max_length=30)
    egggroups = models.CharField(max_length=30)
    height_ft = models.CharField(max_length=20)
    height_m = models.CharField(max_length=20)
    weight_lbs = models.CharField(max_length=20)
    weight_kg = models.CharField(max_length=20)
    evhp = models.IntegerField()
    evattack = models.IntegerField()
    evdefense = models.IntegerField()
    evspattack = models.IntegerField()
    evspdefense = models.IntegerField()
    evspeed = models.IntegerField()
    basefriendship = models.IntegerField()
    basehp = models.IntegerField()
    baseattack = models.IntegerField()
    basedefense = models.IntegerField()
    basespattack = models.IntegerField()
    basespdefense = models.IntegerField()
    basespeed = models.IntegerField()
    basetotal = models.IntegerField()
    rolestring = models.CharField(max_length=50)

    def get_moves(self):
        moveslistTemp = list(can_learn.objects.filter(pokemon_id = self).values_list('move_id', flat=True))
        moveslistTemp.extend(list(learnset.objects.filter(pokemon_id = self).values_list('move_id', flat=True)))
        moveslist = list(set(moveslistTemp))
        moveslist.sort()
        return moveslist

    def get_roles(self):
        hpthres = 80
        attthres = 94
        defthres = 85
        spathres = 87
        spdthres = 85
        spethres = 85

        any_in = lambda a,b: any(i in b for i in a)
        roles = []
        moveslist = self.get_moves()
        if self.basehp > hpthres:

            if self.basedefense > defthres:

                if self.basespattack > spathres:

                    if (92 in moveslist) and (any_in([152,273], moveslist)):
                        if any_in([20,335,128,587,83,611,463,212,328,169,250,35],moveslist):
                            roles.append(10)
                        #else:
                        roles.append(9)

                if self.baseattack > attthres:
                    roles.append(7)

                if self.basespdefense >spdthres:
                    if any_in([215,312], moveslist):
                        roles.append(17)
                    #else:
                    roles.append(6)
                if 6 not in roles:
                    roles.append(4)

            if self.basespdefense > spdthres:

                if self.basespattack > spathres:
                    roles.append(8)

                if 6 not in roles:
                    roles.append(5)

            if self.basespeed > spethres and (any_in([446,191,20],moveslist)):
                    roles.append(12)

        if self.basespeed > spethres:

            if self.baseattack > attthres:

                if self.basespattack > spathres:
                    roles.append(3)
                if 269 in moveslist:
                    roles.append(13)
                if 3 not in roles:
                    roles.append(1)

            if self.basespattack >spathres:
                if 269 in moveslist:
                    roles.append(14)
                if 3 not in roles:
                    roles.append(2)
            #else:
            if any_in([183,213,86,109,137], moveslist):
                roles.append(11)
            if (any_in([446,191,390], moveslist)) and (any_in([153,120], moveslist)):
                roles.append(15)
        #else:
        if (any_in([446,191,390], moveslist)) and (any_in([153,120], moveslist)):
            roles.append(16)

        roles.sort()


        return roles

    def set_rolestr(self):
        roleslist = self.get_roles()
        rolestr = ",".join([str(r) for r in roleslist])
        self.rolestring = rolestr
        self.save()
        return self.rolestring


    def __str__(self):
        return self.name

#class poke_type(models.Model):

class Ability(models.Model):
    ability_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length = 20)
    description = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class has_ability(models.Model):
    ability_id = models.ForeignKey(Ability)
    pokemon_id = models.ForeignKey(Pokemon)
    def __str__(self):
        return self.ability_id

class Moves(models.Model):
    move_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    move_type = models.CharField(max_length=15)
    category = models.CharField(max_length=15)
    pp = models.IntegerField()
    power = models.CharField(max_length=15)
    accuracy = models.CharField(max_length=15)
    gen = models.CharField(max_length=5)
    def __str__(self):
        return self.name

class learnset(models.Model):
    pokemon_id = models.ForeignKey(Pokemon)
    move_id = models.ForeignKey(Moves)
    level = models.IntegerField()
    def __str__(self):
        return self.level

class can_learn(models.Model):
    pokemon_id = models.ForeignKey(Pokemon)
    move_id = models.ForeignKey(Moves)
    TM = models.CharField(max_length=10)
    def __str__(self):
        return self.pokemon_id.name

class Evolution(models.Model):
    pokemon_id1 = models.ForeignKey(Pokemon, related_name='pokemon_1')
    pokemon_id2 = models.ForeignKey(Pokemon, related_name='pokemon_2')
    how = models.CharField(max_length=20)
    def __str__(self):
        return self.how

class Natures(models.Model):
    name = models.CharField(max_length=10)
    increased_stat = models.CharField(max_length=10)
    descrease_stat = models.CharField(max_length=10)

class SearchBox(forms.Form):
    query = forms.CharField(max_length=100)

class Roles(models.Model):
    rID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    reqStats = models.CharField(max_length=50)
    reqMoves = models.CharField(max_length=50)
    compIDs = models.CharField(max_length=50)
    suggNat = models.CharField(max_length=50)
    impMoves = models.CharField(max_length=150)
    compRoles = models.CharField(max_length=150)

    def __str__(self):
        return self.name


