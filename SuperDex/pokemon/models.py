from django.db import models

# Create your models here.

class poke_type(models.Model):
	poke_type = models.CharField(max_length=20)
	Normal = models.DecimalField(max_digits=3, decimal_places=2)
	Fighting = models.DecimalField(max_digits=3, decimal_places=2)
	Flying = models.DecimalField(max_digits=3, decimal_places=2)
	Poison = models.DecimalField(max_digits=3, decimal_places=2)
	Ground = models.DecimalField(max_digits=3, decimal_places=2)
	Rock = models.DecimalField(max_digits=3, decimal_places=2)
	Bug = models.DecimalField(max_digits=3, decimal_places=2)
	Ghost = models.DecimalField(max_digits=3, decimal_places=2)
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
	def __str__(self):
		return self.name

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
		return self.ability_id.name

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
