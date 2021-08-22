import spacy
from spacy.cli import download
#download("es_core_news_sm")
download("es_core_news_lg")

#import en_core_web_sm
#nlp = en_core_web_sm.load()
import es_core_news_sm
nlp = es_core_news_sm.load()

import pandas as pd


def obtener_entidades(texto):
    doc = nlp(texto)
    return doc


def guardar_entidades_en_dataframe(doc, path):
    # Se extraen las entidades con su tipo
    df = pd.DataFrame()
    clase = []
    texto = []
    for ent in doc.ents:
        clase.append(ent.label_)
        texto.append(ent.text)

    dictionary = {'texto': texto, 'clase': clase}
    df = pd.DataFrame(dictionary)
    df['filename'] = path
    return df