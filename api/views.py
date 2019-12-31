from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ApiForm
from aylienapiclient import textapi
import os

#initialization
LANGUAGE = 'en'
MODE = 'document'
APP_ID = os.environ['TEXTAPI_APP_ID']
APP_KEY = os.environ['TEXTAPI_APP_KEY']
client = textapi.Client(APP_ID, APP_KEY)

# Create your views here.


def api(request):
    api_form = ApiForm()
    results = {}
    sentiment = {}
    entities = []
    classifications = {}
    summary = {}
    concepts = []

    if request.method == "POST":
        api_form = ApiForm(data=request.POST)
        #form validation
        if api_form.is_valid():
            url = request.POST.get('url', '')

            if (url != ""):
                # Lo enviamos y redireccionamos
                try:
                    #Sentiment Analysis
                    sentiment = client.Sentiment({'url' : url,
                                                  'language' : LANGUAGE,
                                                  'mode' : MODE})

                    #Classification Analysis
                    classifications = client.Classify({'url' : url,
                                                       'language' : LANGUAGE})

                    #Entity Analysis
                    entities = []
                    entities_total = client.Entities({'url' : url,
                                                      'language' : LANGUAGE})

                    for type, values in entities_total['entities'].items():
                        entities.append({'type' : type,
                                         'entity' : " - ".join(values)})

                    #Concept Analysis
                    concepts = []
                    concepts_total = client.Concepts({'url' : url,
                                                      'language' : LANGUAGE})

                    for uri, value in concepts_total['concepts'].items():
                        sfs = " - ".join(map(lambda c: c['string'] + " :"
                            + str(round(c['score'], 4)),
                                                    value['surfaceForms']))
                        concepts.append({'uri' : uri, 'words' : sfs})

                    #Summary Analysis
                    summary = client.Summarize({'url' : url,
                                                'language' : LANGUAGE})

                    results = {'sentiment' : sentiment,
                               'classifications' : classifications,
                               'entities' : entities,
                               'summary' : summary,
                               'concepts' : concepts,
                               'form': api_form}

                    return render(request, "api/api.html", results)
                except:
                    # Algo no ha ido bien, redireccionamos a FAIL
                    return redirect(reverse('api')+"?fail")

    return render(request, "api/api.html",
                            {'sentiment': sentiment,
                             'classifications' : classifications,
                             'entities' : entities,
                             'summary' : summary,
                             'concepts' : concepts,
                             'form' : api_form})
