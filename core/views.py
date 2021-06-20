from django.shortcuts import render
from news.models import Universidad, Noticia, Region
from .models import Email
from django.db import IntegrityError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# Create your views here.
def about(request):
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
