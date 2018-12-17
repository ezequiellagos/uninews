from django.shortcuts import render
from news.models import Universidad, Noticia
from .models import Email
from django.db import IntegrityError

from django.core.mail import send_mail

# Create your views here.
def about(request):
    return render(request, "core/about.html")

def contact(request):
    return render(request, "core/contact.html")

def universities(request):
    universities = Universidad.objects.all()
    return render(request, "core/universities.html", {'universities':universities})

def categories(request):
    categories = Noticia.objects.order_by().values('categoria').distinct()
    return render(request, "core/categories.html", {'categories':categories})

def regiones(request):
        regiones = Universidad.objects.all().values('region').order_by('region').distinct()
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
                        info = True
                except IntegrityError:
                        info = False
        return render(request, "core/email.html", {'info':info})

