from decruft import Document
import urllib2
f = urllib2.urlopen('http://jph.cointet.free.fr')
f = urllib2.urlopen("http://lautregrenelledelamer.over-blog.com/article-algues-vertes-tous-les-acteurs-reunis-ce-samedi-a-fouesnant-of-89583483.html")
f=urllib2.urlopen("http://jph.cointet.free.fr/wp/?page_id=5")
f=urllib2.urlopen("http://www.liberation.fr/societe/01012377958-l-ex-homme-de-confiance-de-liliane-bettencourt-mis-en-examen")
print Document(f.read()).summary()