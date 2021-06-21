
from django.db.models.functions.datetime import TruncYear
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.template import RequestContext, Template
from .models import Universidad, Noticia, Region
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, date, time, timedelta
from django.db.models import Max, Sum, Q, Count
from django.conf import settings

from django.db.models.functions import ExtractYear
from django.db.models.functions import TruncMonth

import unidecode

# from wordcloud import WordCloud, STOPWORDS
# import matplotlib.pyplot as plt
# import pandas as pd
# import nltk
# from nltk.corpus import stopwords
# from nltk import tokenize
# import urllib
# import base64
# import io

CANTIDAD_NOTICIAS_MAS_VISTAS = 3

# Create your views here.
def home(request):
    # Obtiene las noticias ordenadas de sde la más reciente
    news = Noticia.objects.order_by('-fecha')
    
    # Devuelve las noticias para la paginación
    news = pagination(request, news)

    # Filtra las ultimas dos noticias más vistas
    date = mostViewed()
    news_most_view = Noticia.objects.filter(fecha__range=[date['last_date'], date['current_date']]).order_by('-contador_visitas')[:CANTIDAD_NOTICIAS_MAS_VISTAS]

    return render(request, "news/home.html", {'news':news, 'news_most_view':news_most_view})

def category(request, category):
    news = Noticia.objects.order_by('-fecha').filter(categoria=category)

    # Noticias por Categoria
    date = mostViewed()
    news_most_view = Noticia.objects.filter(categoria=category).filter(fecha__range=[date['last_date'], date['current_date']]).order_by('-contador_visitas')[:CANTIDAD_NOTICIAS_MAS_VISTAS]

    # Paginación
    news = pagination(request, news)

    return render(request, "news/category.html", {'news':news, 'news_most_view':news_most_view, 'category':category})

def region(request, region):
    news = Noticia.objects.filter(id_universidad__region__slug=region).order_by('-fecha')

    # Noticias por Categoria
    date = mostViewed()
    news_most_view = Noticia.objects.filter(id_universidad__region__slug=region).filter(fecha__range=[date['last_date'], date['current_date']]).order_by('-contador_visitas')[:CANTIDAD_NOTICIAS_MAS_VISTAS]

    # Paginación
    news = pagination(request, news)

    return render(request, "news/region.html", {'news':news, 'news_most_view':news_most_view, 'region':region})

def university(request, alias):
    news = Noticia.objects.filter(id_universidad__alias=alias).order_by('-fecha')

    # Noticias por Universidad
    date = mostViewed()
    news_most_view = Noticia.objects.filter(id_universidad__alias=alias).filter(fecha__range=[date['last_date'], date['current_date']]).order_by('-contador_visitas')[:CANTIDAD_NOTICIAS_MAS_VISTAS]

    # Paginación
    news = pagination(request, news)

    return render(request, "news/university.html", {'news':news, 'news_most_view':news_most_view, 'university':Universidad.objects.get(alias=alias)})

def detail(request, id_noticia):
    new = get_object_or_404(Noticia, pk=id_noticia)
    new.contador_visitas += 1
    new.save(update_fields=['contador_visitas'])
    return redirect(new.link_noticia)


def statistics(request):
    # Crea objeto con la tabla de noticias
    news = Noticia.objects.order_by('-contador_visitas')
    universidades = Universidad.objects.order_by('-alias')


    # nltk.download('stopwords')

    date = mostViewed()
    estadisticas_universidades = []
    total_noticias = 0
    total_visitas = 0

    for universidad in universidades:

        # Si la universidad no tiene noticias, pasa a la siguiente
        if news.filter(id_universidad__alias=universidad.alias).count() == 0:
            continue
        
        n = news.filter(id_universidad__alias=universidad.alias)

        total_noticias += n.count()
        total_visitas += (n.aggregate(Sum('contador_visitas')))['contador_visitas__sum']

        try:
            estadisticas_universidades.append({
                'nombre_corto': universidad.alias,
                'nombre_largo': universidad.nombre,
                # Suma de todas las visitas por universidad
                'total_visitas': (n.aggregate(Sum('contador_visitas')))['contador_visitas__sum'],
                # Noticia más vista de todo el tiempo
                'noticia_mas_vista': n.latest('contador_visitas'),
                # Noticia más reciente últimas 2 semanas
                'noticia_mas_vista_reciente': n.filter(fecha__range=[date['last_date'], date['current_date']]).latest('contador_visitas'),
                # Cantidad de noticias totales
                'total_noticias': n.count(),
                # Noticias por mes, colocar en grafico
                'noticias_por_mes': n.annotate(month=TruncMonth('fecha')).values('month').annotate(total=Count('id_noticia')).order_by(),
                # Noticias por año
                'noticias_por_anio': n.annotate(year=TruncYear('fecha')).values('year').annotate(total=Count('id_noticia')).order_by(),
                # Nube de palabras
                # 'nube_de_palabras': word_cloud(list(n.values('titulo', 'bajada'))),

                # 'test': n.extra(select={'day': 'date( fecha )'}).values('day').annotate(noticias=Count('id_noticia')).order_by('fecha'),
                
            })

            # now = datetime.now()
            # for year in range(2017, now.year):
            #     print(year)

            # print("-------------------------")
            # print(estadisticas_universidades['nube_de_palabras'])
            # print("-------------------------")

            
        except Exception as e:
            print("-------------------------")
            print(universidad.alias)
            print(e)
            print("-------------------------")


# agregar una estadisticas que sea la tasa de crecimiento mensual por universidad y otra de la plataforma en cantidad de noticias

    estadisticas_generales = {}

    estadisticas_generales['estadisticas_fecha'] = Noticia.objects.extra(select={'day': 'date( fecha )'}).values('day').annotate(noticias=Count('id_noticia'))
    estadisticas_generales['total_noticias'] = total_noticias
    estadisticas_generales['total_visitas'] = total_visitas
    
    
    return render(request, 'news/statistics.html', {
        'estadisticas_universidades':estadisticas_universidades, 
        'estadisticas_generales':estadisticas_generales
        })


# def word_cloud(lista):
#     comment_words = ''
#     stopwords_es = set(stopwords.words('spanish'))

#     for val in lista:
#         # typecaste each val to string
#         val = str(val['titulo'] + ' ' + val['bajada'])

#         # split the value
#         tokens = val.split()

#         # Converts each token into lowercase
#         for i in range(len(tokens)):
#             tokens[i] = tokens[i].lower()

#         comment_words += " ".join(tokens)+" "

#     wordcloud = WordCloud(width=800, height=800,
#                         background_color='white',
#                         stopwords=stopwords_es,
#                         min_font_size=10).generate(comment_words)

#     # plot the WordCloud image
#     plt.figure(figsize=(8, 8), facecolor=None)
#     plt.imshow(wordcloud)
#     plt.axis("off")

#     image = io.BytesIO()
#     plt.savefig(image, format='png')
#     image.seek(0)  # rewind the data
#     string = base64.b64encode(image.read())

#     image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
#     return image_64

def search(request):
    info = False
    if request.method == 'GET':
        search = request.GET['search']
        search = unidecode.unidecode(search).lower()
        # news = Noticia.objects.filter( Q(titulo__icontains=search) | Q(bajada__icontains=search) )
        news = Noticia.objects.filter( Q(titulo_busqueda__icontains=search) | Q(bajada_busqueda__icontains=search) )
        info = True

        # Paginación
        news = pagination(request, news)
    return render(request, "news/search.html", {'news':news, 'info':info, 'search':request.GET['search']})

def search_fix(request):
    news = Noticia.objects.order_by('-fecha')
    for new in news:
        new.titulo_busqueda = formatear_busqueda(new.titulo)
        new.bajada_busqueda = formatear_busqueda(new.bajada)
        new.save(update_fields=['titulo_busqueda', 'bajada_busqueda'])

    return render(request, "core/testing.html", {'result': 'ok'})

def formatear_busqueda(text):
    # Al cambiar algo tambien debe ser modificado en views de scraper
    text = unidecode.unidecode(text).lower()
    text = text.replace('"', "")
    text = text.replace('?', "")
    text = text.replace('¿', "")
    text = text.replace(':', "")
    text = text.replace('#', "")
    text = text.replace('.', "")
    text = text.replace(',', "")
    text = text.replace(';', "")
    text = text.replace('(', "")
    text = text.replace(')', "")

    return text

def pagination(request, news, news_per_page = 21):
    
    page = request.GET.get('page')
    paginator = Paginator(news, news_per_page)
    try:
        return paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        return paginator.get_page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        return paginator.get_page(paginator.num_pages)

def mostViewed():
    days_news_most_viewed = 14
    hoy = datetime.today()
    semana_atras = date.today() - timedelta(days=days_news_most_viewed)
    formato = "%Y-%m-%d" # AAAA-MM-DD
    fecha_actual = hoy.strftime(formato)
    fecha_pasada = semana_atras.strftime(formato)
    return {'current_date':fecha_actual, 'last_date':fecha_pasada}

def topicos(request):
    return home(request)

def topicKeyWords(topic):

    universities = []
    date_range = {}

    hoy = datetime.today().strftime("%Y-%m-%d")

    if topic == 'coronavirus':
        key_words = ['coronavirus', 'covid', 'covid-19', 'covid19', 'pandemia', 'cuarentena', 'sars', 'cov-2', 'cov2', 'sars-cov2', 'sars-cov-2']
    elif topic == 'uninews':
        key_words = ['uninews']
    elif topic == 'obsnieves':
        key_words = ['observatorio satelital', 'satelital', 'nieves', 'observatorio satelital de nieves']
        universities = ['UPLA']
        date_range = {
            'last_date': '2018-11-23',
            'current_date': hoy
        }
    elif topic == 'datoslab':
        key_words = ['datoslab', 'miguel guevara', 'uninews', 'fastask', 'moneda social']
    else:
        key_words = ['uninews']

    return key_words, universities, date_range

def topicNew(request, topic):

    key_words, universities, date_range = topicKeyWords(topic)

    news = Noticia.objects.none()

    if len(universities) != 0:
        for alias in universities:
            for key in key_words:
                news |= Noticia.objects.filter(id_universidad__alias=alias).filter( Q(titulo_busqueda__icontains=key) | Q(bajada_busqueda__icontains=key) )
    else:
        for key in key_words:
            news |= Noticia.objects.filter( Q(titulo_busqueda__icontains=key) | Q(bajada_busqueda__icontains=key) )
    

    if len(date_range) != 0:
        news = news.distinct().filter(fecha__range=[date_range['last_date'], date_range['current_date']]).order_by('-fecha')
    else:
        news = news.distinct().order_by('-fecha')


    # Noticias más vistas
    date = mostViewed()
    news_most_view = news.filter(fecha__range=[date['last_date'], date['current_date']]).order_by('-contador_visitas')[:CANTIDAD_NOTICIAS_MAS_VISTAS]

    # Paginación
    news = pagination(request, news)

    return render(request, "news/topic.html", {'news':news, 'news_most_view':news_most_view, 'topic':topic})

# Topic News Widget
def topicNewWidget(request):
    # Palabras clave para cada tema
    if request.path == '/coronavirus/':
        topic = 'Coronavirus'
        key_words, universities, date_range = topicKeyWords('coronavirus')
    elif request.path == '/obsnieves/':
        topic = 'Observatorio Satelital de Nieves'
        key_words, universities, date_range = topicKeyWords('obsnieves')
    else:
        return redirect('/')

    # Filtra para cada palabra clave
    news = Noticia.objects.none()
    if len(universities) != 0:
        for alias in universities:
            for key in key_words:
                news |= Noticia.objects.filter(id_universidad__alias=alias).filter( Q(titulo_busqueda__icontains=key) | Q(bajada_busqueda__icontains=key) )
    else:
        for key in key_words:
            news |= Noticia.objects.filter( Q(titulo_busqueda__icontains=key) | Q(bajada_busqueda__icontains=key) )

    # Entrega determinada cantidad de items
    if request.GET.get('items') and request.GET.get('items').isnumeric() :
        news_request = int(request.GET['items'])
        if news_request == 0:
            n_r = 100000
        elif news_request >= 1:
            n_r = news_request
        else:
            n_r = 10
    else:
        n_r = 10

    if len(date_range) != 0:
        news = news.distinct().filter(fecha__range=[date_range['last_date'], date_range['current_date']]).order_by('-fecha')[:n_r]
    else:
        news = news.distinct().order_by('-fecha')[:n_r]

    return render(request, "news/thematic.html", {'news':news, 'topic':topic})


