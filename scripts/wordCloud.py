from unidecode import unidecode
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

def generate_wordcloud(text): # optionally add: stopwords=STOPWORDS and change the arg below
    wordcloud = WordCloud(width=1600, height=800, 
    font_path='/home/deylon/Documentos/projetos-git/globoCrawler/scripts/font/Open_Sans/OpenSans-Regular.ttf').generate(text)
    #plt.figure( figsize=(20,10), facecolor='k')
    plt.figure(figsize=(20,10), dpi=1000)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()

def obterTexto(p_linha):
    v_atributos = p_linha.split("','")
    v_title = re.sub('[^a-zA-Z0-9 \\\]', ' ', v_atributos[0])
    v_autor = re.sub('[^a-zA-Z0-9 \\\]', ' ', v_atributos[1])
    v_data = v_atributos[2].replace('"', '')
    v_texto = re.sub('[^a-zA-Z0-9 \\\]', ' ', v_atributos[3])
    return v_texto


v_nameFile = 'content/carlosMeloCleaned.arff'
v_file = open(v_nameFile, 'r')

v_canToLowerCase = False
v_palavasAutor = ''
for v_line in v_file:
    if(v_line == "@data\n"):
        v_canToLowerCase = True
    
    if (v_canToLowerCase == True and v_line != "@data\n"):
        v_line = str.lower(str(v_line)).decode('utf8')
        v_line = unidecode(v_line)
        v_texto = obterTexto(v_line)
        v_palavasAutor = v_palavasAutor + " " + v_texto
v_file.close()

generate_wordcloud(v_palavasAutor)