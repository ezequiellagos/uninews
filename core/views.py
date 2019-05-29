from django.shortcuts import render
from news.models import Universidad, Noticia
from .models import Email
from django.db import IntegrityError
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Create your views here.
def about(request):
    return render(request, "core/about.html")

def contact(request):
    return render(request, "core/contact.html")

def license(request):
    return render(request, "core/license.html")

def universities(request):
    universities = Universidad.objects.all()
    return render(request, "core/universities.html", {'universities':universities})

def categories(request):
    categories = Noticia.objects.order_by().values('categoria').distinct()
    return render(request, "core/categories.html", {'categories':categories})

def regiones(request):
    regiones = Universidad.objects.all().values('region').order_by('region').distinct()
    for region in regiones:
        if region['region'] == '1':
            region['nombre'] = 'Tarapacá'
        elif region['region'] == '2':
            region['nombre'] = 'Antofagasta'
        elif region['region'] == '3':
            region['nombre'] = 'Atacama'
        elif region['region'] == '4':
            region['nombre'] = 'Coquimbo'
        elif region['region'] == '5':
            region['nombre'] = 'Valparaíso'
        elif region['region'] == '6':
            region['nombre'] = "Libertador Bernardo O'Higgins"
        elif region['region'] == '7':
            region['nombre'] = 'Maule'
        elif region['region'] == '8':
            region['nombre'] = 'Bío-Bío'
        elif region['region'] == '9':
            region['nombre'] = 'Araucanía'
        elif region['region'] == '10':
            region['nombre'] = 'Los Lagos'
        elif region['region'] == '11':
            region['nombre'] = 'Aysén del Gral Carlos Ibáñez del Campo'
        elif region['region'] == '12':
            region['nombre'] = 'Magallanes y la Antártica Chilena'
        elif region['region'] == '13':
            region['nombre'] = 'Metropolitana'
        elif region['region'] == '14':
            region['nombre'] = 'Los Ríos'
        elif region['region'] == '15':
            region['nombre'] = 'Arica y Parinacota'
        elif region['region'] == '2':
            region['nombre'] = 'Tarapacá'
            
    return render(request, "core/regiones.html", {'regiones':regiones})

def error_404(request):
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
