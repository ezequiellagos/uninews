from django.shortcuts import render
from news.models import Universidad, Noticia
from bs4 import BeautifulSoup
from django.conf import settings

import feedparser, unicodedata, urllib.request, time, re, datetime, time, threading
import ssl
import dateutil.parser
import logging
import unidecode
import json

result = []

# Create your views here.
def scraper(request):
    hora = {}
    hora["start"] = time.strftime("%H:%M:%S")
    hora_inicio = time.time()

    if settings.DEBUG == False:
        # Usar hilos para Producción
        logging.basicConfig( level=logging.DEBUG, format='[%(levelname)s] - %(threadName)-10s : %(message)s')
        universidades = [
            {'target':pucv, 'name':'PUCV'},
            {'target':ucn, 'name':'UCN'},
            {'target':utfsm, 'name':'UTFSM'},
            {'target':uv, 'name':'UV'},
            {'target':upla, 'name':'UPLA'},
            {'target':udec, 'name':'UDEC'},
            {'target':utalca, 'name':'UTALCA'},
            {'target':ulagos, 'name':'ULAGOS'},
            {'target':unap, 'name':'UNAP'},
            {'target':ua, 'name':'UA'},
            {'target':uda, 'name':'UDA'},
            {'target':userena, 'name':'USERENA'},
            {'target':uoh, 'name':'UOH'},
            {'target':ucm, 'name':'UCM'},
            {'target':ubiobio, 'name':'UBIOBIO'},
            {'target':ucsc, 'name':'UCSC'},
            {'target':ufro, 'name':'UFRO'},
            {'target':uct, 'name':'UCT'},
            {'target':uach, 'name':'UACH'},
            {'target':uaysen, 'name':'UAYSEN'},
            {'target':umag, 'name':'UMAG'},
            {'target':uta, 'name':'UTA'}
        ]

        # Por cada universidad crea un hilo de ejecución
        for universidad in universidades:
            threading.Thread(target=universidad['target'], name=universidad['name']).start()
    else:
        # Este metodo de ejecutar los scraper es muy lento
        # Pero el panel uninews.datoslab.cl/scraper solo muestra información acerca de los errores e información si se usa este metodo
        # Usar solo para Desarrollo

        #pucv() # Funcionando
        #ucn() # Funcionando
        #utfsm() # Funcionando
        #uv() # Funcionando
        #upla() # Funcionando #Revisar
        #udec() # Funcionando
        #utalca() # Funcionando #Revisar
        #ulagos() # Funcionando
        #ucsc() # Funcionando
        #ubiobio() # Funcionando
        #uda() # En Funcionando
        #userena() # En Funcionando #Revisar
        # unap() # Funcionando
        #ua() # Funcionando

        # uoh() No se pudo scrapear

        # ucm() # Funcionando

        # ufro() # Funcionando
        uct() # Funciona con angular, usar selenium
        # uach() # Funcionando
        # uaysen() #Funcionando
        # umag() # Funcionando - Revisar la bajada
        # uta() # Funcionando

    hora_fin = time.time()
    hora["finish"] = time.strftime("%H:%M:%S")
    hora["total"] = hora_fin - hora_inicio

    result.append({'status':"", 'error_message':'', 'universidad':'', 'titulo':'', 'bajada':'', 'fecha':'', 'link_noticia':'', 'link_recurso':'', 'categoria':''})
    return render(request, "scraper/scraper.html", {'result':result, 'hora':hora})

def saveNew(new):
    try:
        # Busca la noticia en la base de datos
        # Si no la encuentra genera un error y ejecuta el except
        n = Noticia.objects.get(titulo=new['titulo'], id_universidad__alias = new['universidad'].alias)
        print(new['universidad'].alias + ": " + new['titulo'] + " | Existe")
        e = "Existe" 
        # Si la encuentra agrega un mensaje que se mostrará al de depuración
        result.append({'status':"exist", 'error_message':e, 'universidad':new['universidad'], 'titulo':new['titulo'], 'bajada':new['bajada'], 'fecha':new['fecha'], 'link_noticia':new['link_noticia'], 'link_recurso':new['link_recurso'], 'categoria':new['categoria']})
    except Noticia.DoesNotExist as e:
        # Si la noticia no se encuentra la crea
        n = Noticia(
            titulo=new['titulo'],
            titulo_busqueda=formatear_busqueda(new['titulo']),
            bajada=new['bajada'],
            bajada_busqueda=formatear_busqueda(new['bajada']),
            fecha=new['fecha'],
            link_noticia=new['link_noticia'],
            link_recurso=new['link_recurso'],
            id_universidad=new['universidad'],
            categoria=new['categoria'],
            contador_visitas=0
            )
        n.save() # Guarda la noticia en la base de datos
        print(new['universidad'].alias + ": " + new['titulo'] + " | Insertada")
        e = "Insertada"
        result.append({'status':"ok", 'error_message':e, 'universidad':new['universidad'], 'titulo':new['titulo'], 'bajada':new['bajada'], 'fecha':new['fecha'], 'link_noticia':new['link_noticia'], 'link_recurso':new['link_recurso'], 'categoria':new['categoria']})

def formatear_busqueda(text):
    # Al cambiar algo tambien debe ser modificado en search_fix de views de news
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

def formatear_fecha(fecha, universidad):
    
    if universidad == "uv":
        fecha = fecha.split()
        dia = fecha[0]
        mes = fecha[2].lower()
        anno = fecha[4]
    elif universidad == "upla":
        fecha = fecha.split()
        dia = fecha[1]
        mes = fecha[2].lower()
        anno = fecha[3]
    elif universidad == "ufsm":
        fecha = fecha.split()
        dia = fecha[1]
        mes = fecha[2].lower()
        anno = fecha[3]
    elif universidad == "ucn":
        fecha = fecha.split()
        dia = fecha[1]
        mes = fecha[2].lower()
        anno = fecha[3]
    elif universidad == "pucv":
        fecha = fecha.split()
        dia = fecha[1]
        mes = fecha[3].lower()
        anno = fecha[5]
    elif universidad == "udec":
        dia = dateutil.parser.parse(fecha).strftime('%d')
        mes = dateutil.parser.parse(fecha).strftime('%m')
        anno = dateutil.parser.parse(fecha).strftime('%Y')
    elif universidad == "utalca":
        fecha = fecha.lower().split()
        dia = fecha[0]
        mes = fecha[1]
        anno = fecha[2]
    elif universidad == "ulagos":
        fecha = fecha.lower().split('/')
        dia = fecha[0]
        mes = fecha[1]
        anno = fecha[2]
    elif universidad == "ucsc":
        dia = dateutil.parser.parse(fecha).strftime('%d')
        mes = dateutil.parser.parse(fecha).strftime('%m')
        anno = dateutil.parser.parse(fecha).strftime('%Y')
    elif universidad == "ubiobio":
        fecha = fecha.split()
        dia = fecha[1]
        mes = fecha[2].lower()
        anno = fecha[3]
    elif universidad == 'uda':
        dia = dateutil.parser.parse(fecha).strftime('%d')
        mes = dateutil.parser.parse(fecha).strftime('%m')
        anno = dateutil.parser.parse(fecha).strftime('%Y')
    elif universidad == 'userena':
        dia = dateutil.parser.parse(fecha).strftime('%d')
        mes = dateutil.parser.parse(fecha).strftime('%m')
        anno = dateutil.parser.parse(fecha).strftime('%Y')
    elif universidad == 'unap':
        fecha = fecha.lower().split()
        dia = fecha[1]
        mes = fecha[3]
        anno = fecha[5]
    elif universidad == 'ua':
        dia = dateutil.parser.parse(fecha).strftime('%d')
        mes = dateutil.parser.parse(fecha).strftime('%m')
        anno = dateutil.parser.parse(fecha).strftime('%Y')
    elif universidad == 'ucm':
        dia = dateutil.parser.parse(fecha).strftime('%d')
        mes = dateutil.parser.parse(fecha).strftime('%m')
        anno = dateutil.parser.parse(fecha).strftime('%Y')
    elif universidad == 'ufro':
        dia = dateutil.parser.parse(fecha).strftime('%d')
        mes = dateutil.parser.parse(fecha).strftime('%m')
        anno = dateutil.parser.parse(fecha).strftime('%Y')
    elif universidad == 'uta':
        dia = dateutil.parser.parse(fecha).strftime('%d')
        mes = dateutil.parser.parse(fecha).strftime('%m')
        anno = dateutil.parser.parse(fecha).strftime('%Y')
    elif universidad == 'umag':
        dia = dateutil.parser.parse(fecha).strftime('%d')
        mes = dateutil.parser.parse(fecha).strftime('%m')
        anno = dateutil.parser.parse(fecha).strftime('%Y')
    elif universidad == 'uaysen':
        fecha = fecha.lower().split()
        dia = fecha[0]
        mes = fecha[1]
        anno = fecha[2]
    elif universidad == 'uach':
        dia = dateutil.parser.parse(fecha).strftime('%d')
        mes = dateutil.parser.parse(fecha).strftime('%m')
        anno = dateutil.parser.parse(fecha).strftime('%Y')
    elif universidad == 'uct':
        fecha = fecha.lower().split()
        dia = fecha[0]
        mes = fecha[1]
        anno = fecha[2]

    if mes == "enero" or mes == "jan" or mes == '1':
        mes = '01'
    elif mes == "febrero" or mes == "feb" or mes == '2':
        mes = '02'
    elif mes == "marzo" or mes == "mar" or mes == '3':
        mes = '03'
    elif mes == "abril" or mes == "apr" or mes == '4':
        mes = '04'
    elif mes == "mayo" or mes == "may" or mes == '5':
        mes = '05'
    elif mes == "junio" or mes == "jun" or mes == '6':
        mes = '06'
    elif mes == "julio" or mes == "jul" or mes == '7':
        mes = '07'
    elif mes == "agosto" or mes == "aug" or mes == '8':
        mes = '08'
    elif mes == "septiembre" or mes == "sep" or mes == '9':
        mes = '09'
    elif mes == "octubre" or mes == "oct" or mes == '10':
        mes = '10'
    elif mes == "noviembre" or mes == "nov" or mes == '11':
        mes = '11'
    elif mes == "diciembre" or mes == "dec" or mes == '12':
        mes = '12'

    if dia == "1":
        dia = '01'
    elif dia == "2":
        dia = '02'
    elif dia == "3" :
        dia = '03'
    elif dia == "4":
        dia = '04'
    elif dia == "5":
        dia = '05'
    elif dia == "6":
        dia = '06'
    elif dia == "7":
        dia = '07'
    elif dia == "8":
        dia = '08'
    elif dia == "9":
        dia = '09'

    #fecha = dia + "/" + mes + "/" + anno
    fecha = anno + "-" + mes + "-" + dia
    return fecha

# Realiza limpieza a cada categoria
def setCategoria(categoria = ''):
    if categoria == '' or categoria == None:
        return 'sin-categoria'
    else:
        categoria = categoria.lower()
        categoria = elimina_tildes(categoria)
        categoria = categoria.replace(" ", "-")
        categoria = categoria.replace("&", "y")
        categoria = categoria.replace("#", "")
        categoria = categoria.replace(",", "-")
    return categoria

def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))


# Universidad de Playa Ancha
def upla():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='UPLA')
    url_rss = "https://www.upla.cl/noticias/feed/" # URL de feed RSS
    feed = feedparser.parse( url_rss ) # Se obtiene el XML y se procesa

    for item in feed['items']:
        try:
            titulo =  item['title']
            bajada =  item['summary']
            link = item['link']
            fecha = item['published']
            fecha = formatear_fecha(fecha, "upla")

            # Se obtiene y filtra la categoria para ser buscada
            categoria_busqueda = setCategoria(item['category'])
            if categoria_busqueda == 'gestion-institucional':
                categoria_busqueda = 'gestion'

            # Entra en la pagina de cada categoria y busca todas las noticias
            contents = urllib.request.urlopen("https://www.upla.cl/noticias/category/"+categoria_busqueda).read()
            bs = BeautifulSoup(contents, "html.parser")
            
            # Se realizan ajustes para las catergorias con alguna particularidad
            if categoria_busqueda == 'coronavirus':
                articles = bs.find_all("div", ["timeline-content"])
            else:
                articles = bs.find_all("article", ["item-list"])
            
            # Por cada noticia de cada categoria obtiene su titulo
            for article in articles:                
                if categoria_busqueda == 'coronavirus':
                    titulo_articulo = article.h2.a.text
                else:
                    titulo_articulo = article.find("a").text

                # Si el titulo de la noticia es igual al titulo obtenido del XML, obtiene la imagen de esa noticia y termina el ciclo
                if titulo_articulo == titulo:
                    imagen = article.find("img")['src']
                    break
                else: 
                    imagen = ''
            # Se ejecuta la función para guardar la noticia en la base de datos
            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
        except Exception as e:
            # Si ocurre un error se individualiza y se prepara para mostrar
            # en la pantalla de depuración
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
    logging.debug('Deteniendo')

# Pontificia Universidad Católica de Valparaíso
def pucv():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='PUCV')
    nombre_uni = "pucv"
    context = ssl._create_unverified_context()
    contents = urllib.request.urlopen("https://www.pucv.cl/pucv/site/tax/port/all/taxport_1___1.html", context=context).read()
    bs = BeautifulSoup(contents, "html.parser")
    articulos = bs.find_all("article")
    
    for articulo in articulos:
        try:
            link = articulo.a['href']
            link = "https://www.pucv.cl" + link.replace("..", "")
            fecha = articulo.find("span",{"class":"fecha aright"})

            imagen = articulo.img['src']
            imagen = "https://pucv.cl" + imagen.replace("..","")

            pagina_noticia = urllib.request.urlopen(link).read()
            bs_noticia = BeautifulSoup(pagina_noticia, "html.parser")
            titulo = bs_noticia.find("h1", { "class" : "titular" }).text
            if fecha is None:
                fecha = time.strftime("%Y-%m-%d")
            else:
                fecha = formatear_fecha(fecha.text,nombre_uni)

            try:
                bajada = bs_noticia.find("p",{ "class" : "bajada" }).text
            except Exception as e:
                bajada = ''
                result.append({'status':"warning", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})

            # No encuentra una categoría
            try:
                newpage = urllib.request.urlopen(link).read()
                bs_cate = BeautifulSoup(newpage, "html.parser")
                categoria = bs_cate.find("div",{ "class" : "breadcrumbs" })
                categorias = categoria.findAll("a")

                category = categorias[2].text
                categoria_busqueda = setCategoria(category)

            except Exception as e:
                categoria_busqueda = 'sin-categoria'
                result.append({'status':"warning", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
            saveNew({'status':"ok", 'error_message':'', 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
        except Exception as e:
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
    logging.debug('Deteniendo')

# Universidad Católica del Norte
def ucn():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='UCN')

    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    d = feedparser.parse("https://www.noticias.ucn.cl/feed/")

    for e in d.entries:
        try:
            titulo = (e.title)
            nombre_uni = "ucn"
            link = (e.link)
            categoria_busqueda = setCategoria((e.category))
            fecha = e.published
            fecha = formatear_fecha(fecha,nombre_uni)
            description = e.description.split("/>")
            bajada = description[1]
            cuerpo = e['content']
            contenido = cuerpo[0].value
            imagen = re.search('(?P<url>https?://[^\s]+(png|jpeg|jpg))', contenido).group("url").replace("-150x150", "")
            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
        except Exception as e:
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
    logging.debug('Deteniendo')

#Universidad Técnico Federico Santa María
def utfsm():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='UTFSM')
    d = feedparser.parse("https://noticias.usm.cl/feed/")
    for e in d.entries:
        try:
            titulo = (e.title)
            nombre_uni = "ufsm"
            link = (e.link)
            categoria_busqueda = setCategoria((e.category))
            bajada = (e.description).replace("[&#8230;]", "").strip()
            fecha = e.published
            fecha = formatear_fecha(fecha,nombre_uni)
            cuerpo = e['content']
            contenido = cuerpo[0].value
            try:
                imagen = re.search('(?P<url>https?://[^\s]+(png|jpeg|jpg))', contenido).group("url")
            except:
                imagen = ''
            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
        except Exception as e:
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
    logging.debug('Deteniendo')

# Universidad de Valparaíso
def uv():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='UV')
    contents = urllib.request.urlopen("https://www.uv.cl/pdn/archivo/").read()
    bs = BeautifulSoup(contents, "html.parser")
    divs = bs.find_all("div", ["item n_caja borde6", "item n_caja borde6 fin"])

    for div in divs:
        try:
            fecha = div.find("div", ["fecha"]).text
            fecha = formatear_fecha(fecha, "uv")
            link = div.a['href']
            link = "https://www.uv.cl/pdn" + link.replace("..", "")

            # Accede a la pagina de la noticia
            pagina_noticia = urllib.request.urlopen(link).read()
            bs_noticia = BeautifulSoup(pagina_noticia, "html.parser")
            titulo = bs_noticia.find("div", id="n_titulo").text
            bajada = bs_noticia.find("div", id="n_bajada").text
            try:
                imagen = bs_noticia.find("div", id="n_clipex").img['src']
                imagen = "https://www.uv.cl" + imagen
            except TypeError:
                imagen = div.find("img", ["sombra"])['src']
                imagen = "https://www.uv.cl/pdn" + imagen.replace("..", "")

            categoria_busqueda = setCategoria()
            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
        except Exception as e:
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
    logging.debug('Deteniendo')

# Universidad de Concepción
def udec():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='UDEC')
    url_rss = "https://noticias.udec.cl/feed/"
    feed = feedparser.parse( url_rss )

    for item in feed['items']:
        try:
            titulo =  item['title']
            link = item['link']
            bajada =  BeautifulSoup(item['summary'], "html.parser").find('p').text.strip()
            fecha = item['published']
            fecha = formatear_fecha(fecha, "udec")
            categoria_busqueda = setCategoria(item['category'])
            imagen = BeautifulSoup(urllib.request.urlopen(link).read(), "html.parser").find_all('img', {'class': 'attachment-large size-large'})[1]['src']

            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
        except Exception as e:
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
    logging.debug('Deteniendo')

# Universidad de Talca
def utalca():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='UTALCA')
    contents = urllib.request.urlopen("https://www.utalca.cl/noticias/").read()
    bs = BeautifulSoup(contents, "html.parser")
    items = bs.find('div', {'class': 'section-news'})
    items = items.find_all("div", {"class": "card-news"})
    items = list(set(items)) # Elimina elementos duplicados
    
    for item in items:
        try:
            link = item.a['href']
            titulo = item.find("h5").text
            if item.div.p is None:
                categoria_busqueda = setCategoria()
            else:
                categoria_busqueda = setCategoria(item.div.p.text)
            
            noticia = urllib.request.urlopen(link).read()
            bs_noticia = BeautifulSoup(noticia, "html.parser")
            bajada = bs_noticia.find("div", {"class": "interior-body"}).h6.text
            fecha = bs_noticia.find("div", {"class": "interior-body"}).span.text
            fecha = formatear_fecha(fecha, 'utalca')
            imagen = bs_noticia.find("img", {"class": "attachment-post-thumbnail size-post-thumbnail wp-post-image"})['src']
            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})            
        except Exception as e:
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
    logging.debug('Deteniendo')

# Universidad de Los Lagos
def ulagos():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='ULAGOS')
    items = []
    categorias = ['campus-osorno', 'campus-pto-montt', 'sede-santiago', 'sede-chiloe']
    for categoria in categorias:
        contents = urllib.request.urlopen("https://www.ulagos.cl/category/" + categoria + "/").read()
        bs = BeautifulSoup(contents, "html.parser")
        items.extend(bs.find_all("div", {"class": "ultimas-noticias"}))
    
    for item in items:
        try:
            link = item.a['href']
            titulo = item.find("div", {"class": "overflow_titulo_noticias"}).text.strip()

            noticia = urllib.request.urlopen(link).read()
            bs_noticia = BeautifulSoup(noticia, "html.parser")

            bajada = bs_noticia.find("div", {"class":"title-post"}).span.text.strip()
            categoria_busqueda = bs_noticia.find("div", {"class":"category-post"}).a.text.lower().strip()
            categoria_busqueda = setCategoria(categoria_busqueda)

            fecha = bs_noticia.find("div", {"class":"conten-post-date"}).text.strip()
            fecha = formatear_fecha(fecha, "ulagos")            
            if bs_noticia.find("img", {"class": "img-destacado"}) is None:
                imagen = ''
            else:
                imagen = bs_noticia.find("img", {"class": "img-destacado"})["src"]

            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})            
        except Exception as e:
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
    logging.debug('Deteniendo')

# Universidad Católica de la Santísima Concepción
def ucsc():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='UCSC')
    contents = urllib.request.urlopen("https://www.ucsc.cl/noticias/").read()
    bs = BeautifulSoup(contents, "html.parser")
    items = bs.find_all("article", {"class": "hentry-news"})    
    items = list(set(items)) # Elimina elementos duplicados
    
    for item in items:
        try:
            link = item.header.h2.a['href']
            titulo = item.header.h2.a.text
            fecha = item.header.p.time['datetime']
            fecha = formatear_fecha(fecha, 'ucsc')
            
            noticia = urllib.request.urlopen(link).read()
            bs_noticia = BeautifulSoup(noticia, "html.parser")
            bajada = bs_noticia.find("div", {"class": "entry-summary"}).p.text
            
            try:
                imagen = bs_noticia.find("article", {"class": "hentry hentry-news"}).header.span.img['src']
            except Exception as e:
                imagen = ''

            categoria_busqueda = bs_noticia.find("a", {"rel": "category tag"})
            categoria_busqueda = setCategoria(categoria_busqueda.text)
            
            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})            
        except Exception as e:
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
    logging.debug('Deteniendo')

# Universidad del Bío-Bío
def ubiobio():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='UBIOBIO')
    d = feedparser.parse("http://noticias.ubiobio.cl/feed/")
    for e in d.entries:
        try:
            titulo = (e.title)
            link = (e.link)
            categoria_busqueda = setCategoria(e.category)
            bajada = (e.description).replace("[&#8230;]", "")
            bs_bajada = BeautifulSoup(bajada, "html.parser")
            bajada = bs_bajada.find("p").text
            fecha = e.published
            fecha = formatear_fecha(fecha,'ubiobio')
            cuerpo = e['content']
            contenido = cuerpo[0].value
            imagen = re.search('(?P<url>https?://[^\s]+(png|jpeg|jpg))', contenido).group("url")

            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
        except Exception as e:
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
    logging.debug('Deteniendo')


# Universidad Arturo Prat
def unap():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='UNAP')
    url_base = 'https://www.unap.cl'
    urls_news = {
        'investigacion': 'https://www.unap.cl/prontus_unap/site/tax/port/all/taxport_13_48__1.html',
        'vinculacion': 'https://www.unap.cl/prontus_unap/site/tax/port/all/taxport_38_39__1.html',
        'acreditacion': 'https://www.unap.cl/prontus_unap/site/tax/port/all/taxport_83_113__1.html',
        'casa-central': 'https://www.unap.cl/prontus_unap/site/tax/port/all/taxport_5_15__1.html',
        'sede-victoria': 'https://www.unap.cl/prontus_unap/site/tax/port/all/taxport_5_17__1.html',
        'noticias-arica': 'https://www.unap.cl/prontus_unap/site/tax/port/all/taxport_5_12__1.html',
        'noticias-antofagasta': 'https://www.unap.cl/prontus_unap/site/tax/port/all/taxport_5_14__1.html',
        'noticias-santiago': 'https://www.unap.cl/prontus_unap/site/tax/port/all/taxport_5_16__1.html'
    }

    for cat, url in urls_news.items():
        contents = urllib.request.urlopen(url).read()
        bs = BeautifulSoup(contents, "html.parser")
        items = bs.find_all("div", {"class": "taxport-item"})
        items = list(set(items)) # Elimina elementos duplicados
    
        for item in items:
            try:
                link = url_base + item.find("div", {"class": "titular"}).a['href'].strip()
                titulo = item.find("div", {"class": "titular"}).a.text.strip()
                fecha = item.find("div", {"class": "fecha"}).text.strip()
                fecha = formatear_fecha(fecha, 'unap')
                
                noticia = urllib.request.urlopen(link).read()
                bs_noticia = BeautifulSoup(noticia, "html.parser")

                try:
                    bajada = bs_noticia.find(id='content').find('h2', {'class': 'bajada'}).text.strip()
                except Exception:
                    bajada = bs_noticia.find("div", {"class": "CUERPO"}).find_all('p')
                    for b in bajada:
                        b = b.text.strip()
                        if b: # Si la bajada no está vacia devuelvela y termina de buscar
                            bajada = b
                            break

                try:
                    imagen = url_base + bs_noticia.find("div", {"class": "CUERPO"}).find("img")['src'].strip()
                except Exception:
                    imagen = ''

                categoria_busqueda = setCategoria(cat)

                saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})            
            except Exception as e:
                result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
    logging.debug('Deteniendo')

# Universidad de Antofagasta
def ua():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='UA')
    url_rss = "http://www.comunicacionesua.cl/feed/"
    feed = feedparser.parse( url_rss )

    for item in feed['items']:
        try:
            titulo =  item['title']
            bajada =  item['description']
            link = item['link']
            fecha = item['published']
            fecha = formatear_fecha(fecha, "ua")
            categoria_busqueda = setCategoria(item['category'])

            noticia = urllib.request.urlopen(link).read()
            imagen = BeautifulSoup(noticia, "html.parser").find('div', {'class': 'qode-post-image'}).img['src']
            
            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
        except Exception as e:
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
    logging.debug('Deteniendo')

# Universidad de Atacama
def uda():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='UDA')
    url_rss = "http://www.uda.cl/index.php?option=com_content&view=category&layout=blog&id=15&Itemid=253&format=feed&type=atom"
    feed = feedparser.parse( url_rss )

    for item in feed['items']:
        try:
            titulo =  item['title']
            bajada =  BeautifulSoup(item['summary'], "html.parser").find('p').text
            link = item['link']
            fecha = item['published']
            fecha = formatear_fecha(fecha, "uda")
            categoria_busqueda = setCategoria(item['category'])
            imagen = "http://www.uda.cl/" + BeautifulSoup(item['summary'], "html.parser").find('img')['src']

            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
        except Exception as e:
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
    logging.debug('Deteniendo')

# Universidad de La Serena
# Región de Coquimbo
def userena():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='USERENA')
    url_rss = ['http://www.userena.cl/actualidad-uls.feed?type=rss',
                'http://www.userena.cl/cultura-y-extension.feed?type=rss',
                'http://www.userena.cl/dgae.feed?type=rss']

    feeds = []
    for url in url_rss:
        feeds.append(feedparser.parse( url ))

    for feed in feeds:
        for item in feed['items']:
            try:
                titulo =  item['title']
                bajada =  BeautifulSoup(item['summary'], "html.parser").find_all('p')[2].text
                link = item['link']
                fecha = item['published']
                fecha = formatear_fecha(fecha, "userena")
                categoria_busqueda = setCategoria(item['category'])
                imagen = BeautifulSoup(item['summary'], "html.parser").p.img['src']

                saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
            except Exception as e:
                result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
    logging.debug('Deteniendo')

# Universidad de O'Higgins
def uoh():
    # https://www.uoh.cl/
    # https://www.uoh.cl/#noticias-y-eventos
    logging.debug('Lanzado')

    # universidad = Universidad.objects.get(alias='UOH')
    # contents = urllib.request.urlopen("https://www.uoh.cl/#noticias-y-eventos").read()
    logging.debug('Deteniendo')
    

# Universidad Católica del Maule
def ucm():
    # http://portal.ucm.cl/
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='UCM')
    url_rss = "https://portal.ucm.cl/feed" # URL de feed RSS
    feed = feedparser.parse( url_rss ) # Se obtiene el XML y se procesa

    for item in feed['items']:
        try:
            titulo = item['title']
            link = item['link']
            fecha = item['published']
            fecha = formatear_fecha(fecha, "ucm")
            categoria_busqueda = setCategoria(item['category'])

            noticia = urllib.request.urlopen(link).read()

            imagen = BeautifulSoup(noticia, "html.parser").find('div', {'class': 'section-content-image'}).img['src']
            bajada =  BeautifulSoup(noticia, "html.parser").find('div', {'class': 'section-content-paragraph'}).find_all('p')[1].text

            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
        except Exception as e:
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
    logging.debug('Deteniendo')

# Universidad de la Frontera
def ufro():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='UFRO')
    url_rss = 'https://www.ufro.cl/index.php/noticias/12-destacadas?format=feed&type=rss'
    feed = feedparser.parse( url_rss )

    for item in feed['items']:
        try:
            titulo = item['title']
            link = item['link']
            fecha = item['published']
            fecha = formatear_fecha(fecha, "ufro")
            categoria_busqueda = setCategoria(item['category'])

            noticia = urllib.request.urlopen(link).read()

            imagen = 'https://www.ufro.cl' + BeautifulSoup(noticia, "html.parser").find('td', {'id': 'imagen'}).p.img['src']
            bajada =  BeautifulSoup(noticia, "html.parser").find('p', {'class': 'bajada'}).text.strip()
            if not bajada:
                bajada =  BeautifulSoup(noticia, "html.parser").find('table', {'class': 'tnoticia'}).tbody.tr.find_all('td')[1].p.text.strip()

            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
        except Exception as e:
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})

    logging.debug('Deteniendo')
    # https://www.ufro.cl/

# Universidad Católica de Temuco
def uct():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='UCT')
    url_base = 'https://www.uct.cl/actualidad/'
    contents = urllib.request.urlopen(url_base).read()
    bs = BeautifulSoup(contents, "html.parser")
    items = bs.find('div', {'id': 'cardslist'}).find('cards-container')[':cards'].strip()
    data = json.loads(items)

    for item in data:
        try:
            titulo = item['title'].replace('“','"').replace('”','"').strip()
            link = item['button']['link']
            fecha = item['date']
            fecha = formatear_fecha(fecha, "uct")
            categoria_busqueda = setCategoria(item['cat'])

            noticia = urllib.request.urlopen(link).read()
            noticia_bs = BeautifulSoup(noticia, "html.parser")
            
            try:
                imagen = item['image']['src']
                if imagen is None:
                    imagen = noticia_bs.find('div', {'class': 'wysiwyg'}).find('img')['src']
            except Exception as e:
                imagen = ''

            bajada =  noticia_bs.find('div', {'class': 'wysiwyg'}).find('p').text.replace('“','"').replace('”','"').strip()

            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
        except Exception as e:
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})

    logging.debug('Deteniendo')
    # https://www.uct.cl/

# Universidad Austral de Chile
def uach():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='UACH')
    url_rss = 'https://diario.uach.cl/feed/'

    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    feed = feedparser.parse( url_rss )

    for item in feed['items']:
        try:
            titulo = item['title']
            link = item['link']
            fecha = item['published']
            fecha = formatear_fecha(fecha, "uach")
            categoria_busqueda = setCategoria(item['category'])

            noticia = urllib.request.urlopen(link).read()
            noticia_bs = BeautifulSoup(noticia, "html.parser")

            imagen = noticia_bs.find('article', {'class': 'post'}).find('div', {'class': 'post-image'}).a['href'].strip()
            bajada =  noticia_bs.find('p', {'class': 'bajada'}).text.replace('“','"').replace('”','"').strip()

            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
        except Exception as e:
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})

    logging.debug('Deteniendo')
    # https://www.uach.cl/

# Universidad de Aysén
def uaysen():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='UAYSEN')
    url = 'https://uaysen.cl/actualidad/noticias'
    contents = urllib.request.urlopen(url).read()
    bs = BeautifulSoup(contents, "html.parser")
    items = bs.find_all("div", {"class": "mb-4 col-xl-4 col-lg-4 col-md-6 col-sm-12"})

    for item in items:
        try:
            titulo = item.div.a.text.strip()
            link = item.div.find("a")['href']
            fecha = item.find("small", {"class": "date"}).text.strip()
            fecha = formatear_fecha(fecha, "uaysen")
            categoria_busqueda = setCategoria(item.find("ul", {"class": "list-inline"}).li.a.text.strip())
            imagen = item.find("div", {"class": "image-news-container-small"}).img['src']

            noticia = urllib.request.urlopen(link).read()
            noticia_bs = BeautifulSoup(noticia, "html.parser")
            bajada =  noticia_bs.find("div", {"class": "text-justify font-weight-bold mb-3"}).text.strip()

            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
        except Exception as e:
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})

    logging.debug('Deteniendo')
    # https://uaysen.cl/
    pass

# Universidad de Magallanes
def umag():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='UMAG')
    url = 'http://www.umag.cl/vcm/?page_id=459'
    contents = urllib.request.urlopen(url).read()
    bs = BeautifulSoup(contents, "html.parser")
    items = bs.find_all("div", {"class": "not-col11"})

    for item in items:
        try:
            link = item.find('a', {'class': 'link'})['href']
            noticia = urllib.request.urlopen(link).read()
            bs_noticia = BeautifulSoup(noticia, "html.parser")

            titulo = bs_noticia.find('div', {'class': 'post-title'}).h2.a.text.strip()

            fecha = bs_noticia.find('span', {'class': 'post-dates'}).text.strip()
            fecha = formatear_fecha(fecha, "umag")

            categoria_busqueda = setCategoria('')

            try:
                imagen = bs_noticia.find('div', {'class': 'entry'}).find('a').find('img')['src']
            except:
                imagen = ''

            bajada =  bs_noticia.find('div', {'class': 'entry'}).p.text.strip()
            if not bajada:
                bajada =  bs_noticia.find('div', {'class': 'entry'}).find_all('p')[2].text.strip()

            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
        except Exception as e:
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})

    logging.debug('Deteniendo')
    # http://www.umag.cl/

# Universidad de Tarapacá
def uta():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='UTA')
    url_rss = 'https://www.uta.cl/index.php/feed/'
    feed = feedparser.parse( url_rss )

    for item in feed['items']:
        try:
            titulo = item['title']
            link = item['link']
            fecha = item['published']
            fecha = formatear_fecha(fecha, "uta")
            
            try:
                categoria_busqueda = setCategoria(item['category'])
            except:
                categoria_busqueda = setCategoria()
            
            bajada = item['summary'].strip()

            noticia = urllib.request.urlopen(link).read()
            
            try:
                imagen = BeautifulSoup(noticia, "html.parser").find('div', {'class': 'wp-block-image'}).figure.a.img['src']
            except:
                try:
                    imagen = BeautifulSoup(noticia, "html.parser").find('figure', {'class': 'wp-block-image'}).a.img['src']
                except:
                    imagen = ''

            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
        except Exception as e:
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
    logging.debug('Deteniendo')
    # https://www.uta.cl/
    