from unidecode import unidecode
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

stop_words = set(stopwords.words('portuguese'))
stop_words.update(('a', 'A', 'As', 'as', 'O', 'Os', 'o', 'os', 'nao', 'ainda', 'sera', 'ser', 'ha', 'ja'))

def removerPontuacao(p_linha):
    v_atributos = p_linha.split('","')
    v_title = re.sub('[^a-zA-Z0-9 \\\]', ' ', v_atributos[0])
    v_autor = re.sub('[^a-zA-Z0-9 \\\]', ' ', v_atributos[1])
    v_data = v_atributos[2].replace('"', '')
    v_texto = re.sub('[^a-zA-Z0-9 \\\]', ' ', v_atributos[3])
    return "'" + v_title + "'" + "," + "'" + v_autor + "'" + "," + "'" + v_data + "'" + "," + "'" + v_texto + "'"

def generate_wordcloud(text): # optionally add: stopwords=STOPWORDS and change the arg below
    wordcloud = WordCloud(relative_scaling = 1.0).generate(text)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

v_nameFileToClean = 'content/Carlos Melo.arff'
v_nameFileOutPut = 'content/carlosMeloCleaned.arff'
v_file = open(v_nameFileToClean, 'r')

v_canToLowerCase = False
v_contentLower = []
for v_line in v_file:
    if(v_line == "@data\n"):
        v_canToLowerCase = True
    
    if (v_canToLowerCase == True and v_line != "@data\n"):
        v_line = str.lower(str(v_line)).decode('utf8')
        v_line = unidecode(v_line)
        v_line = removerPontuacao(v_line)
        word_tokens = word_tokenize(v_line)
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)
        
        v_line = " ".join(str(x) for x in filtered_sentence)
        v_line = v_line.replace(" '", "'")
        v_line = v_line.replace("' ", "'")
        v_contentLower.append(v_line + "\n")
v_file.close()

def escreverConteudo():
    v_fileOut = open(v_nameFileOutPut, 'w')
    v_fileOut.write('@relation TEXTvsAUTHOR')
    v_fileOut.write('\n\n')
    v_fileOut.write('@attribute title string')
    v_fileOut.write('\n')
    v_fileOut.write('@attribute Class {"daniel buarque", "josias souza", "leonardo sakamoto", "carlos melo"}')
    v_fileOut.write('\n')
    v_fileOut.write('@attribute date string')
    v_fileOut.write('\n')
    v_fileOut.write('@attribute content string')
    v_fileOut.write('\n\n')
    v_fileOut.write('@data')
    v_fileOut.write('\n')
    for v_line in v_contentLower:
        v_fileOut.write(v_line)
    v_fileOut.close();

escreverConteudo()