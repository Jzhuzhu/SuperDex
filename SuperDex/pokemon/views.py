from django.shortcuts import render
from django.template import Context, loader
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist

from pokemon.models import * 

# Create your views here.

def index(request):
	context = {'test':'foobar'}
	return render(request, 'pokemon/main_search.html', context)

def search(request):
	query = request.GET.get('q')
	pokemon = Pokemon.objects.get(name=query)

	has_abilities = has_ability.objects.filter(pokemon_id=pokemon)
	abilities = []
	for has in has_abilities:
		ability = has.ability_id
		abilities.append(ability)

	can_learn_list = can_learn.objects.filter(pokemon_id=pokemon)
	TM_list = []
	TM_move_list = []
	for learn in can_learn_list:
		learn_move = learn.move_id
		TM_list.apppend(learn.TM)
		TM_move_list.append(learn_move)
	zip_TM = zip(TM_list, TM_move_list)

	learnset_list = learnset.objects.filter(pokemon_id=pokemon)
	level_list = []
	level_move_list = []
	for learnset in learnset_list:
		learnset_move = learnset.move_id
		level_list.append(learnset.level)
		level_move_list.append(learnset_move)
	zip_level = zip(level_list, level_move_list)

	context = RequestContext(request)
	return render_to_response('pokemon/pokemon_profile.html', {"pokemon": pokemon, "abilities": abilities,
	 "zip_TM":zip_TM, "zip_level":zip_level,}, context_instance=context)

def pokemon_profile(request, pokemon_id):
	#template = loader.get_template('pokemon/pokemon_profile.html')
	context = {'test':'foobar'}
	return render(request, 'pokemon/pokemon_profile.html', context)
