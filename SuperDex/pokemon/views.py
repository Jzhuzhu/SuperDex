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
    try:
        if query.isdigit():
            pokemon = Pokemon.objects.get(pk=float(query))
        else:
            pokemon = Pokemon.objects.get(name=query)
    except ObjectDoesNotExist:
        return render(request, 'pokemon/main_search.html', {'error': True})

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
        TM_list.append(learn.TM)
        TM_move_list.append(learn_move)
    zip_TM = zip(TM_list, TM_move_list)

    learnset_list = learnset.objects.filter(pokemon_id=pokemon)
    level_list = []
    level_move_list = []
    for lset in learnset_list:
        learnset_move = lset.move_id
        level_list.append(lset.level)
        level_move_list.append(learnset_move)
    zip_level = zip(level_list, level_move_list)

    try:
        evo_from = Evolution.objects.get(pokemon_id2=pokemon)	
    except ObjectDoesNotExist:
        evo_from = False

    try:
        evo_to = Evolution.objects.get(pokemon_id1=pokemon)
    except ObjectDoesNotExist:
        evo_to = False

    Pokemon_type = poke_type.objects.get(poke_type = pokemon.poke_type)
    context = RequestContext(request)
    return render_to_response('pokemon/pokemon_profile.html', {"pokemon": pokemon, "abilities": abilities,
     "zip_TM":zip_TM, "zip_level":zip_level, "evo_from":evo_from, "evo_to":evo_to, "Pokemon_type":Pokemon_type,}, context_instance=context)

def pokemon_profile(request, pokemon_id):
    #template = loader.get_template('pokemon/pokemon_profile.html')
    context = {'test':'foobar'}
    return render(request, 'pokemon/pokemon_profile.html', context)

def index_comparison(request):
    context = {'test':'foobar'}
    return render(request, 'pokemon/main_search_compare.html', context)

def comp_search(request):
    query1 = request.GET.get('p1')
    query2 = request.GET.get('p2')
    try:
        if query1.isdigit():
            pokemon1 = Pokemon.objects.get(pk=float(query1))
        else:
            pokemon1 = Pokemon.objects.get(name=query1)
    except ObjectDoesNotExist:
        return render(request, 'pokemon/main_search_compare.html', {'error1': True})

    try:
        if query2.isdigit():
            pokemon2 = Pokemon.objects.get(pk=float(query2))
        else:
            pokemon2 = Pokemon.objects.get(name=query2)
    except ObjectDoesNotExist:
        return render(request, 'pokemon/main_search_compare.html', {'error2': True})

    has_abilities1 = has_ability.objects.filter(pokemon_id=pokemon1)
    ability1 = []
    for has in has_abilities1:
        ability = has.ability_id
        ability1.append(ability)
    has_abilities2 = has_ability.objects.filter(pokemon_id=pokemon2)
    ability2 = []
    for has in has_abilities2:
        ability = has.ability_id
        ability2.append(ability)
    ability_comp = zip(ability1,ability2)

    type1 = poke_type.objects.get(poke_type = pokemon1.poke_type)
    type2 = poke_type.objects.get(poke_type = pokemon2.poke_type)
    sumtype1 = poke_type.objects.filter(poke_type = pokemon1.poke_type).values_list(flat=True)
    sumtype2 = poke_type.objects.filter(poke_type = pokemon2.poke_type).values_list(flat=True)
    sum1 = 0.0
    sum2 = 0.0

    for i in range(1,len(sumtype1)):
        sum1 += sumtype1[0][i]
        sum2 += sumtype2[0][i]

    if pokemon1.basetotal > pokemon2.basetotal:
        pokemon_stat = pokemon1
    elif pokemon1.basetotal < pokemon2.basetotal:
        pokemon_stat = pokemon2

    if sum1 > sum2:
        pokemon_less_weak = pokemon1
    else:
        pokemon_less_weak = pokemon2

    context = RequestContext(request)
    return render_to_response('pokemon/pokemon_comparison.html', {"pokemon1":pokemon1, "pokemon2":pokemon2,
        "ability_comp":ability_comp, "type1":type1, "type2":type2, "pokemon_stat":pokemon_stat, "pokemon_less_weak":pokemon_less_weak,}, context_instance=context)
