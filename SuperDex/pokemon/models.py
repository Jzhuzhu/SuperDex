from django.db import models
from django import forms

# Create your models here.

class Pokemon(models.Model):
	name = models.CharField(max_length=50)
	nickname = models.CharField(max_length=50)
	number = models.IntegerField(primary_key=True)
	imageurl = models.URLField()
	#poke_type = models.ForeignKey('poke_type')
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
	def __str__(self):
		return self.pokemon_id

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