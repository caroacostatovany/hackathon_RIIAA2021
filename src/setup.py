#see: https://setuptools.readthedocs.io/en/latest/userguide/package_discovery.html
from setuptools import setup, find_packages

setup(name="busqueda_desaparecidos",
      version="0.1",
      description=u"Paquete que contiene preprocesamiento imagen, ocr, y clasificacion de entidades",
      url="",
      author="JesusBandaG, Arturo-Granados, caroacostatovany,  cuauhtemocbe, gerald1978",
      author_email="",
      license="MIT",
      packages=find_packages(),
      install_requires = [
                          "numpy",
                          "pandas",
                          "sphinx",
                          "nltk",
                          "regex",
                          "tesseract",
                          "opencv-python"
                          ],
      )