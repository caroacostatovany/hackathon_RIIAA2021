import re


def encontrar_expediente(texto):
    x = re.search("xp[0-9,=,-]+", texto_limpio_minusculas)
    return x


def convertir_texto_exp_dataframe(path, expediente, texto):
    texto_exp = "{}| {}".format(x.group(), texto_limpio_minusculas.replace(x.group(), ''))
    df = pd.DataFrame([[path, texto_exp]], columns=["filename", "text"])

    return df