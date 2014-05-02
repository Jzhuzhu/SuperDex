from django.shortcuts import render
from django.template import Context, loader
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from pokemon.models import Pokemon 

# Create your views here.

def index(request):
	context = {'test':'foobar'}
	return render(request, 'pokemon/main_search.html', context)

def search(request):
	query = request.GET.get('q')
	pokemon = Pokemon.objects.get(name=query)
	context = RequestContext(request)
	return render_to_response('pokemon/pokemon_profile.html', {"pokemon": pokemon,}, context_instance=context)

def pokemon_profile(request, pokemon_id):
	#template = loader.get_template('pokemon/pokemon_profile.html')
	context = {'test':'foobar'}
	return render(request, 'pokemon/pokemon_profile.html', context)
