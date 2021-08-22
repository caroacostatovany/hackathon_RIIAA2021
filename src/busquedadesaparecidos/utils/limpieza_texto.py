import re
from busquedadesaparecidos.utils.constantes import STOPWORDS_PROPIOS

clases = ['organizacion', 'persona', 'lugar', 'fecha']

def convierte_minusculas(texto):
    """Convierte a minúsculas todo el texto
    :param texto: texto a convertir
    :return: texto convertido
    """

    return texto.lower()


def quitar_caracteres_especiales(phrase):
    """
    :param phrase:
    :return:
    """
    caracteres_especiales = "’'?!,.():;#\/°_@~%=<>"
    # quita dobles espacios y lo hace 1
    phrase = re.sub(' +', ' ', phrase)

    phrase = re.sub("á", "a", phrase)
    phrase = re.sub("é", "e", phrase)
    phrase = re.sub("í", "i", phrase)
    phrase = re.sub("ó", "o", phrase)
    phrase = re.sub("ú", "u", phrase)

    phrase = re.sub("\n", "", phrase)

    # quita los caracteres especiales
    regex = re.compile('[%s]' % re.escape(caracteres_especiales))

    phrase = regex.sub('', phrase)

    return phrase

def quitar_nonascii(phrase):
    """
    :param phrase:
    :return:
    """
    return phrase.encode('ascii', errors='ignore').decode('utf-8')


def quitar_stopwords(texto):
    text_tokens = word_tokenize(texto)

    tokens_without_sw = [word for word in text_tokens if not word in STOPWORDS_PROPIOS]

    filtered_sentence = (" ").join(tokens_without_sw)

    return filtered_sentence


def renombrar_clases_spacy(df):
    df.loc[df['clase'] == 'ORG', 'clase'] = 'organizacion'
    df.loc[df['clase'] == 'PER', 'clase'] = 'persona'
    df.loc[df['clase'] == 'LOC', 'clase'] = 'lugar'
    df.loc[df['clase'] == 'DATE', 'clase'] = 'fecha'
    # Not in clases
    df.loc[~df['clase'].isin(clases), 'clase'] = 'otro'

    return df
