from django.shortcuts import render
from news.models import Universidad, Noticia
from bs4 import BeautifulSoup
import feedparser, unicodedata, urllib.request, time, re, datetime, time, threading
import dateutil.parser
from django.conf import settings
import logging

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

        for universidad in universidades:
            threading.Thread(target=universidad['target'], name=universidad['name']).start()
    else:
        # Este metodo de ejecutar los scraper es muy lento
        # Pero el panel uninews.datoslab.cl/scraper solo muestra información acerca de los errores e información si se usa este metodo
        # Usar solo para Desarrollo
        pucv() # Funcionando
        ucn() # Funcionando
        utfsm() # Funcionando
        uv() # Funcionando
        upla() # Funcionando
        udec() # Funcionando
        utalca() # Funcionando
        ulagos() # Funcionando
        ucsc() # Funcionando
        ubiobio() # Funcionando

        unap()
        ua()
        uda()
        userena()
        uoh()
        ucm()
        ufro()
        uct()
        uach()
        uaysen()
        umag()
        uta()

    hora_fin = time.time()
    hora["finish"] = time.strftime("%H:%M:%S")
    hora["total"] = hora_fin - hora_inicio

    result.append({'status':"", 'error_message':'', 'universidad':'', 'titulo':'', 'bajada':'', 'fecha':'', 'link_noticia':'', 'link_recurso':'', 'categoria':''})
    return render(request, "scraper/scraper.html", {'result':result, 'hora':hora})

def saveNew(new):
    try:
        n = Noticia.objects.get(titulo=new['titulo'], id_universidad__alias = new['universidad'].alias)
        print(new['universidad'].alias + ": " + new['titulo'] + " | Existe")
        e = "Existe" 
        result.append({'status':"exist", 'error_message':e, 'universidad':new['universidad'], 'titulo':new['titulo'], 'bajada':new['bajada'], 'fecha':new['fecha'], 'link_noticia':new['link_noticia'], 'link_recurso':new['link_recurso'], 'categoria':new['categoria']})
    except Noticia.DoesNotExist as e:
        n = Noticia(
            titulo=new['titulo'],
            bajada=new['bajada'],
            fecha=new['fecha'],
            link_noticia=new['link_noticia'],
            link_recurso=new['link_recurso'],
            id_universidad=new['universidad'],
            categoria=new['categoria'],
            contador_visitas=0
            )
        n.save()
        print(new['universidad'].alias + ": " + new['titulo'] + " | Insertada")
        e = "Insertada"
        result.append({'status':"ok", 'error_message':e, 'universidad':new['universidad'], 'titulo':new['titulo'], 'bajada':new['bajada'], 'fecha':new['fecha'], 'link_noticia':new['link_noticia'], 'link_recurso':new['link_recurso'], 'categoria':new['categoria']})

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
        # Esta universidad tambien entrega la hora pero no se esta usando por ahora
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

def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

# Universidad de Playa Ancha
def upla():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='UPLA')
    url_rss = "http://www.upla.cl/noticias/feed/"
    feed = feedparser.parse( url_rss )

    for item in feed['items']:
        try:
            titulo =  item['title']
            bajada =  item['summary']
            link = item['link']
            categoria = item['category']
            fecha = item['published']
            fecha = formatear_fecha(fecha, "upla")

            # Parsea la categoria para ser buscada
            categoria_busqueda = categoria.lower()
            categoria_busqueda = elimina_tildes(categoria_busqueda)
            categoria_busqueda = categoria_busqueda.replace(" ", "-")

            # Entra en la pagina de cada categoria y busca todas las noticias
            contents = urllib.request.urlopen("http://www.upla.cl/noticias/category/"+categoria_busqueda).read()
            bs = BeautifulSoup(contents, "html.parser")
            articles = bs.find_all("article", ["item-list"])

            # Por cada noticia obtiene su titulo
            for article in articles:
                titulo_articulo = article.find("a").text

                # Si el titulo de la noticia es igual al titulo obtenido del XML, obtiene la imagen de esa noticia y termina el ciclo
                if titulo_articulo == titulo:
                    imagen = article.find("img")['src']
                    break
            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
        except Exception as e:
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
    logging.debug('Deteniendo')

# Pontificia Universidad Católica de Valparaíso
def pucv():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='PUCV')
    nombre_uni = "pucv"
    contents = urllib.request.urlopen("http://www.pucv.cl/pucv/site/tax/port/all/taxport_1___1.html").read()
    bs = BeautifulSoup(contents, "html.parser")
    articulos = bs.find_all("article")
    
    for articulo in articulos:
        try:
            link = articulo.a['href']
            link = "http://www.pucv.cl" + link.replace("..", "")
            fecha = articulo.find("span",{"class":"fecha aright"})

            imagen = articulo.img['src']
            imagen = "http://pucv.cl" + imagen.replace("..","")

            pagina_noticia = urllib.request.urlopen(link).read()
            bs_noticia = BeautifulSoup(pagina_noticia, "html.parser")
            titulo = bs_noticia.find("h1", { "class" : "titular" }).text

            bajada = bs_noticia.find("p",{ "class" : "bajada" }).text
            if fecha is None:
                fecha = time.strftime("%Y-%m-%d")
            else:
                fecha = formatear_fecha(fecha.text,nombre_uni)

            # No encuentra una categoría
            try:
                newpage = urllib.request.urlopen(link).read()
                bs_cate = BeautifulSoup(newpage, "html.parser")
                categoria = bs_cate.find("div",{ "class" : "breadcrumbs" })
                categorias = categoria.findAll("a")

                category = categorias[2].text
                categoria_busqueda = category.lower()
                categoria_busqueda = elimina_tildes(categoria_busqueda)
                categoria_busqueda = categoria_busqueda.replace(" ", "-")
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
    d = feedparser.parse("http://www.noticias.ucn.cl/feed/")
    for e in d.entries:
        try:
            titulo = (e.title)
            nombre_uni = "ucn"
            link = (e.link)
            categoria = (e.category)
            categoria_busqueda = categoria.lower()
            categoria_busqueda = elimina_tildes(categoria_busqueda)
            categoria_busqueda = categoria_busqueda.replace(" ", "-")
            fecha = e.published
            fecha = formatear_fecha(fecha,nombre_uni)
            description = e.description.split("/>")
            bajada = description[1]
            cuerpo = e['content']
            contenido = cuerpo[0].value
            imagen = re.search('(?P<url>http?://[^\s]+(png|jpeg|jpg))', contenido).group("url").replace("-150x150", "")
            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
        except Exception as e:
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
    logging.debug('Deteniendo')

#Universidad Técnico Federico Santa María
def utfsm():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='UTFSM')
    d = feedparser.parse("http://www.noticias.usm.cl/feed/")
    for e in d.entries:
        try:
            titulo = (e.title)
            nombre_uni = "ufsm"
            link = (e.link)
            categoria = (e.category)
            categoria_busqueda = categoria.lower()
            categoria_busqueda = elimina_tildes(categoria_busqueda)
            categoria_busqueda = categoria_busqueda.replace(" ", "-")
            bajada = (e.description).replace("[&#8230;]", "")
            fecha = e.published
            fecha = formatear_fecha(fecha,nombre_uni)
            region_u = "5"
            cuerpo = e['content']
            contenido = cuerpo[0].value
            imagen = re.search('(?P<url>https?://[^\s]+(png|jpeg|jpg))', contenido).group("url")
            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
        except Exception as e:
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
    logging.debug('Deteniendo')

# Universidad de Valparaíso
def uv():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='UV')
    contents = urllib.request.urlopen("http://www.uv.cl/pdn/archivo/").read()
    bs = BeautifulSoup(contents, "html.parser")
    divs = bs.find_all("div", ["item n_caja borde6", "item n_caja borde6 fin"])

    for div in divs:
        try:
            fecha = div.find("div", ["fecha"]).text
            fecha = formatear_fecha(fecha, "uv")
            link = div.a['href']
            link = "http://www.uv.cl/pdn" + link.replace("..", "")

            # Accede a la pagina de la noticia
            pagina_noticia = urllib.request.urlopen(link).read()
            bs_noticia = BeautifulSoup(pagina_noticia, "html.parser")
            titulo = bs_noticia.find("div", id="n_titulo").text
            bajada = bs_noticia.find("div", id="n_bajada").text
            try:
                imagen = bs_noticia.find("div", id="n_clipex").img['src']
                imagen = "http://www.uv.cl" + imagen
            except TypeError:
                imagen = div.find("img", ["sombra"])['src']
                imagen = "http://www.uv.cl/pdn" + imagen.replace("..", "")

            categoria_busqueda = 'sin-categoria'
            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
        except Exception as e:
            result.append({'status':"error", 'error_message':e, 'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})
    logging.debug('Deteniendo')

# Universidad de Concepción
def udec():
    logging.debug('Lanzado')
    universidad = Universidad.objects.get(alias='UDEC')
    contents = urllib.request.urlopen("http://www.udec.cl/panoramaweb2016/noticias").read()
    bs = BeautifulSoup(contents, "html.parser")
    items = bs.find_all("tr")

    for item in items:
        try:
            link = "http://www.udec.cl" + item.a['href']
            titulo = item.a.text
            bajada = item.p.text
            categoria_busqueda = 'sin-categoria'
            noticia = urllib.request.urlopen(link).read()
            bs_noticia = BeautifulSoup(noticia, "html.parser")
            fecha = bs_noticia.find("span", {"class": "submitted"}).span["content"]
            fecha = formatear_fecha(fecha, "udec")
            imagen = bs_noticia.find("div", {"class": "content node-noticias"}).img["src"]

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
    items = bs.find_all("div", {"class": "card-news"})
    items = list(set(items)) # Elimina elementos duplicados
    
    for item in items:
        try:
            link = item.a['href']
            titulo = item.find("h5").text

            if item.div.p is None:
                categoria_busqueda = 'sin-categoria'
            else:
                categoria_busqueda = elimina_tildes(item.div.p.text.lower())
                categoria_busqueda = categoria_busqueda.replace(" ", "-")
            
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
        contents = urllib.request.urlopen("http://www.ulagos.cl/category/" + categoria + "/").read()
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
            if(categoria_busqueda == "vinculación con el medio"):
                categoria_busqueda = "vinculacion"
            categoria_busqueda = categoria_busqueda.replace(" ", "-")
            categoria_busqueda = elimina_tildes(categoria_busqueda)

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
            imagen = bs_noticia.find("article", {"class": "hentry hentry-news"}).header.span.img['src']
            categoria_busqueda = bs_noticia.find("a", {"rel": "category tag"})
            categoria_busqueda = elimina_tildes(categoria_busqueda.text.lower()).replace(" ", "-")
            
            saveNew({'universidad':universidad, 'titulo':titulo, 'bajada':bajada, 'fecha':fecha, 'link_noticia':link, 'link_recurso':imagen, 'categoria':categoria_busqueda})            
        except Exception as e:
            pass
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
            categoria_busqueda = elimina_tildes(e.category.lower())
            categoria_busqueda = categoria_busqueda.replace(" ", "-")
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
    logging.debug('Deteniendo')
    # http://www.unap.cl/prontus_unap/site/edic/base/port/inicio.html
    pass

# Universidad de Antofagasta
def ua():
    logging.debug('Lanzado')
    logging.debug('Deteniendo')
    # http://www.uantof.cl/
    pass

# Universidad de Atacama
def uda():
    logging.debug('Lanzado')
    logging.debug('Deteniendo')
    #http://www.uda.cl/
    pass

# Universidad de La Serena
# Región de Coquimbo
def userena():
    logging.debug('Lanzado')
    logging.debug('Deteniendo')
    # http://www.userena.cl/
    pass

# Universidad de O'Higgins
def uoh():
    logging.debug('Lanzado')
    logging.debug('Deteniendo')
    # https://www.uoh.cl/
    pass

# Universidad Católica del Maule
def ucm():
    logging.debug('Lanzado')
    logging.debug('Deteniendo')
    # http://portal.ucm.cl/
    pass

# Universidad de la Frontera
def ufro():
    logging.debug('Lanzado')
    logging.debug('Deteniendo')
    # https://www.ufro.cl/
    pass

# Universidad Católica de Temuco
def uct():
    logging.debug('Lanzado')
    logging.debug('Deteniendo')
    # https://www.uct.cl/
    pass

# Universidad Austral de Chile
def uach():
    logging.debug('Lanzado')
    logging.debug('Deteniendo')
    # https://www.uach.cl/
    pass

# Universidad de Aysén
def uaysen():
    logging.debug('Lanzado')
    logging.debug('Deteniendo')
    # https://uaysen.cl/
    pass

# Universidad de Magallanes
def umag():
    logging.debug('Lanzado')
    logging.debug('Deteniendo')
    # http://www.umag.cl/
    pass

# Universidad de Taracapá
def uta():
    logging.debug('Lanzado')
    logging.debug('Deteniendo')
    # https://www.uta.cl/
    pass
    