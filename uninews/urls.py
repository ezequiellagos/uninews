"""uninews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include, re_path
from django.conf.urls import handler404, handler500

from core import views as core_views
from news import views as news_views
from scraper import views as scraper_views

from django.conf import settings

urlpatterns = [
    path('', news_views.home, name='home'),
    # re_path(r'^/page/(?P<page>\d+)/$', news_views.home),
    path('detalle/<int:id_noticia>', news_views.detail, name='detail'),
    path('universidad/<str:alias>', news_views.university, name='university'),
    path('categoria/<slug:category>', news_views.category, name='category'),
    path('region/<slug:region>', news_views.region, name='region'),
    path('estadisticas/', news_views.statistics, name='statistics'),
    path('busqueda/', news_views.search, name='search'),
    path('search_fix/', news_views.search_fix, name='search_fix'),

    path('nosotros/', core_views.about, name='about'),
    path('contacto/', core_views.contact, name='contact'),
    path('licencia/', core_views.license, name='license'),
    path('universidades/', core_views.universities, name='universities'),
    path('categorias/', core_views.categories, name='categories'),
    path('regiones/', core_views.regiones, name='regiones'),
    path('email/', core_views.email, name='email'),

    # Noticias temáticas
    path('coronavirus/', news_views.topicNewWidget, name='coronavirus'),

    path('scraper/', scraper_views.scraper, name='scraper'),

    path('admin/', admin.site.urls),
]

handler404 = core_views.error_404
handler500 = core_views.error_500

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    