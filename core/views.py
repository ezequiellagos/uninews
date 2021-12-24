from os import error
from django.shortcuts import render
from news.models import Universidad, Noticia, Region, University, News, Category
from .models import Email
from django.db import IntegrityError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

import sys
from django.utils.text import slugify
from datetime import date
from datetime import datetime

# Create your views here.
def about(request):
    noticias = Noticia.objects.all()
    universities = University.objects.using('other').all()
    categories = Category.objects.using('other').all()
    errors = []

    for n in noticias:
        try:
            uni = universities.get(alias=n.id_universidad.alias)
            cat = categories.get(name=n.categoria)
            
            if type(n.fecha) is datetime.date:
                print(n.fecha)
                dt_fecha = datetime.combine(n.fecha, datetime.min.time())
                print(dt_fecha)

            slug_generate = slugify(str(n.titulo) + '-' + str(n.fecha.year) + '-' + str(n.fecha.month) + '-' + str(n.fecha.day) + '-' + str(uni.alias))
            new = News(id = n.id_noticia, title = n.titulo, summary = n.bajada, pub_date = n.fecha, url_source = n.link_noticia, url_image = n.link_recurso, visitor_counter = n.contador_visitas, created_at = n.created, updated_at = n.updated, university = uni, search_summary = n.bajada_busqueda, search_title = n.titulo_busqueda, active = True, featured = False, content = '', search_content = '', slug = slug_generate, is_legacy = True)
            new.save(using='other')
            new.categories.add(cat)


            # new_update = News.objects.using('other').filter(id=n.id_noticia).update(created_at=n.created, updated_at=n.updated)
        
        except Exception as e:
            print('||||||||||||||||||||||||||||||||||||||||||')
            # print(n.id_noticia)
            print(f'ID: {n.id_noticia}')
            print(f'Size ID: {len(str(n.id_noticia))}')
            print(f'Type ID: {type(n.id_noticia)}')
            print('--------------------')

            print(f'Titulo: {n.titulo}')
            print(f'Size Titulo: {len(str(n.titulo))}')
            print(f'Type Titulo: {type(n.titulo)}')
            print('--------------------')

            print(f'Bajada: {n.bajada}')
            print(f'Size Bajada: {len(str(n.bajada))}')
            print(f'Type Bajada: {type(n.bajada)}')
            print('--------------------')

            print(f'Fecha: {n.fecha}')
            print(f'Size Fecha: {len(str(n.fecha))}')
            print(f'Type Fecha: {type(n.fecha)}')
            print('--------------------')
            
            print(f'Link Noticia: {n.link_noticia}')
            print(f'Size Link Noticia: {len(str(n.link_noticia))}')
            print(f'Type Link Noticia: {type(n.link_noticia)}')
            print('--------------------')

            print(f'Link Recurso: {n.link_recurso}')
            print(f'Size Link Recurso: {len(str(n.link_recurso))}')
            print(f'Type Link Recurso: {type(n.link_recurso)}')
            print('--------------------')

            print(f'Contador Visitas: {n.contador_visitas}')
            print(f'Size Contador Visitas: {len(str(n.contador_visitas))}')
            print(f'Type Contador Visitas: {type(n.contador_visitas)}')
            print('--------------------')

            print(f'Created: {n.created}')
            print(f'Size Created: {len(str(n.created))}')
            print(f'Type Created: {type(n.created)}')
            print('--------------------')

            print(f'Updated: {n.updated}')
            print(f'Size Updated: {len(str(n.updated))}')
            print(f'Type Updated: {type(n.updated)}')
            print('--------------------')

            print(f'ID Universidad: {n.id_universidad.alias}')
            print(f'Size ID Universidad: {len(str(n.id_universidad.alias))}')
            print(f'Type ID Universidad: {type(n.id_universidad.alias)}')
            print('--------------------')

            print(f'Categoria: {n.categoria}')
            print(f'Size Categoria: {len(str(n.categoria))}')
            print(f'Type Categoria: {type(n.categoria)}')
            print('--------------------')

            print(f'Error: {e}')
            
            errors.append(n.id_noticia)
            continue
    print(errors)
    return render(request, "core/about.html")

def contact(request):
    return render(request, "core/contact.html")

def license(request):
    return render(request, "core/license.html")

def universities(request):
    universities = Universidad.objects.order_by('alias')
    news = Noticia.objects.order_by('-contador_visitas')
    list_universities = Universidad.objects.none()

    # Si la universidad tiene más de 0 noticias, entonces mostrará su logo
    for university in universities:
        if news.filter(id_universidad__alias=university.alias).count() > 0:
            list_universities |= Universidad.objects.filter(alias=university.alias)

    return render(request, "core/universities.html", {'universities':list_universities})

def categories(request):
    categories = Noticia.objects.order_by().values('categoria').distinct()
    return render(request, "core/categories.html", {'categories':categories})

def regiones(request):
    regiones = Region.objects.filter(numero_region__in=Universidad.objects.values_list('region_id', flat=True)).order_by('numero_region')
    return render(request, "core/regiones.html", {'regiones':regiones})

if settings.DEBUG == False:
    def error_404(request, exception):
        data = {}
        return render(request,'core/error_404.html', data)
else:
    def error_404(request, exception):
        data = {}
        return render(request,'core/error_404.html', data)



def error_500(request):
    data = {}
    return render(request,'core/error_500.html', data)

def email(request):
    if request.method == 'POST':
        try:
            e = Email(email=request.POST['email'])
            e.save()

            # msg_html = render_to_string('core/mail/welcome.html', {'some_params': email})
            # msg_txt = render_to_string('core/mail/welcome.txt', {'some_params': email})
            # send_mail('Bienvenido a UniNews!', msg_txt, 'uninews@uninews.datoslab.cl', [request.POST['email']], fail_silently=True, html_message=msg_html)

            info = True
        except IntegrityError:
            info = False
    return render(request, "core/email.html", {'info':info})
