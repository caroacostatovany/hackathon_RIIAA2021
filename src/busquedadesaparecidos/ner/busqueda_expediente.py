import re
import pandas as pd

def encontrar_expediente(texto):
    x = re.search("xp[0-9,=,-]+", texto)

    try:
        x = x.group()
    except:
        x = "No encontrado"

    return x


def convertir_texto_exp_dataframe(path, expediente, texto):
    texto_exp = "{}| {}".format(expediente, texto.replace(expediente, ''))
    df = pd.DataFrame([[path, texto_exp]], columns=["filename", "text"])

    return df