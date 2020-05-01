from django.shortcuts import render, get_object_or_404, redirect
from .models import Universidad, Noticia, Region
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, date, time, timedelta
from django.db.models import Max, Sum, Q

import unidecode

# Create your views here.
def home(request):
    news = Noticia.objects.order_by('-fecha')
    
    # Paginación
    news = pagination(request, news)

    # Más Vistos
    date = mostViewed()
    news_most_view = Noticia.objects.filter(fecha__range=[date['last_date'], date['current_date']]).order_by('-contador_visitas')[:2]

    return render(request, "news/home.html", {'news':news, 'news_most_view':news_most_view})

def category(request, category):
    news = Noticia.objects.order_by('-fecha').filter(categoria=category)

    # Noticias por Categoria
    date = mostViewed()
    news_most_view = Noticia.objects.filter(categoria=category).filter(fecha__range=[date['last_date'], date['current_date']]).order_by('-contador_visitas')[:2]

    # Paginación
    news = pagination(request, news)

    return render(request, "news/category.html", {'news':news, 'news_most_view':news_most_view, 'category':category})

def region(request, region):
    news = Noticia.objects.filter(id_universidad__region__slug=region).order_by('-fecha')

    # Noticias por Categoria
    date = mostViewed()
    news_most_view = Noticia.objects.filter(id_universidad__region__slug=region).filter(fecha__range=[date['last_date'], date['current_date']]).order_by('-contador_visitas')[:2]

    # Paginación
    news = pagination(request, news)

    return render(request, "news/region.html", {'news':news, 'news_most_view':news_most_view, 'region':region})

def university(request, alias):
    news = Noticia.objects.filter(id_universidad__alias=alias).order_by('-fecha')

    # Noticias por Universidad
    date = mostViewed()
    news_most_view = Noticia.objects.filter(id_universidad__alias=alias).filter(fecha__range=[date['last_date'], date['current_date']]).order_by('-contador_visitas')[:2]

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

    date = mostViewed()
    estadisticas = []
    for universidad in universidades:
        estadisticas.append({
            'nombre': universidad.alias,
            # Suma de todas las visitas por universidad
            'total_visitas': (news.filter(id_universidad__alias=universidad.alias).aggregate(Sum('contador_visitas')))['contador_visitas__sum'],
            # Noticia más vista de todo el tiempo
            'noticia_mas_vista': news.filter(id_universidad__alias=universidad.alias).latest('contador_visitas'),
            # Noticia más reciente últimas 2 semanas
            'noticia_mas_vista_reciente': news.filter(id_universidad__alias=universidad.alias).filter(fecha__range=[date['last_date'], date['current_date']]).latest('contador_visitas'),
        })

    return render(request, 'news/statistics.html', {'noticias':news , 'estadisticas':estadisticas})

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

def pagination(request, news, news_per_page = 9):
    
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


# Topic News
def topicNewWidget(request):
    # Palabras clave para cada tema
    if request.path == '/coronavirus/':
        topic = 'Coronavirus'
        key_words = ['coronavirus', 'covid', 'covid-19', 'covid19', 'pandemia', 'cuarentena', 'sars', 'cov-2', 'cov2', 'sars-cov2', 'sars-cov-2']
    else:
        return redirect('/')

    # Filtra para cada palabra clave
    news = Noticia.objects.none()
    for key in key_words:
        news |= Noticia.objects.filter( Q(titulo_busqueda__icontains=key) | Q(bajada_busqueda__icontains=key) )

    # Entrega determinada cantidad de items
    if request.GET.get('items') and request.GET.get('items').isnumeric() :
        news_request = int(request.GET['items'])
        if news_request == 0:
            n_r = 10000
        elif news_request >= 1:
            n_r = news_request
        else:
            n_r = 10
    else:
        n_r = 10
    news = news.distinct().order_by('-fecha')[:n_r]

    return render(request, "news/thematic.html", {'news':news, 'topic':topic})

