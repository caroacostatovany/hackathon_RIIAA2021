import re
import pandas as pd

def encontrar_expediente(texto):
    exp = "No encontrado"
    x = re.search("xp[0-9,=,-]+", texto)

    if x is not None:
        exp = x.group()

    return exp


def convertir_texto_exp_dataframe(path, expediente, texto):
    texto_exp = "{}| {}".format(expediente, texto.replace(expediente, ''))
    df = pd.DataFrame([[path, texto_exp]], columns=["filename", "text"])

    return df