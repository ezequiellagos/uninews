from django.shortcuts import render, get_object_or_404, redirect
from .models import Universidad, Noticia
from django.core.paginator import Paginator
from datetime import datetime, date, time, timedelta
from django.db.models import Max,Sum

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
    news = Noticia.objects.filter(id_universidad__region=region).order_by('-fecha')

    # Noticias por Categoria
    date = mostViewed()
    news_most_view = Noticia.objects.filter(id_universidad__region=region).filter(fecha__range=[date['last_date'], date['current_date']]).order_by('-contador_visitas')[:2]

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

    # Suma de todas las visitas por universidad
    contador_pucv = news.filter(id_universidad__alias="PUCV").aggregate(Sum('contador_visitas'))
    contador_upla = news.filter(id_universidad__alias="UPLA").aggregate(Sum('contador_visitas'))
    contador_ufsm = news.filter(id_universidad__alias="UTFSM").aggregate(Sum('contador_visitas'))
    contador_ucn = news.filter(id_universidad__alias="UCN").aggregate(Sum('contador_visitas'))
    contador_uv = news.filter(id_universidad__alias="UV").aggregate(Sum('contador_visitas'))

    mejores_noticia_pucv = news.filter(id_universidad__alias="PUCV").aggregate(Max('contador_visitas'))
    
    # Asigna los contadores al diccionario contador
    contador = {'upla':contador_upla, 'pucv':contador_pucv, 'ucn':contador_ucn, 'ufsm':contador_ufsm, 'uv':contador_uv, 'mejores_noticia_pucv':mejores_noticia_pucv}

    return render(request, 'news/statistics.html', {'noticias':news , 'contador':contador})

def search(request):
    info = False
    if request.method == 'GET':
        news = Noticia.objects.filter(titulo__contains=request.GET['search'])
        info = True

        # Paginación
        news_per_page = 9
        paginator = Paginator(news, news_per_page)
        page = request.GET.get('page')
        try:
            news = paginator.get_page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            news = paginator.get_page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            news = paginator.get_page(paginator.num_pages)
    return render(request, "news/search.html", {'news':news, 'info':info, 'search':request.GET['search']})

def pagination(request, news):
    news_per_page = 10
    paginator = Paginator(news, news_per_page)
    page = request.GET.get('page')
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
