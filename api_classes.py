# Libs necessárias para utilização dessa folha
# Libs Externas
# Libs required to use this sheet
# External Libs
# Libs requeridos para usar esta hoja
# Libs externas
import json
from enum import Enum

# Classe para retorno de erros conhecidos, por exemplo, envio de imagens sem face...
# Class for returning known errors, for example, sending faceless images ...
# Clase para devolver errores conocidos, por ejemplo, enviar imágenes sin rostro ...
class ErrorCode(Enum):
    null = 0
    primeira_imagem_sem_face = 1
    segunda_imagem_sem_face = 2
    primeira_imagem_invalida = 3
    segunda_imagem_invalida = 4

# Classe genérica para receber JSON e converter em objeto.
# Generic class to receive JSON and convert to object.
# Clase genérica para recibir JSON y convertir a objeto.
class FaceMatchPost(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

# Classe para retorno facematch 1x1
# 1x1 facematch return class
# 1x1 clase de devolución de facematch
class FacematchRetorno:
    def __init__(self):
        self.isequal = None
        self.score = 1
        self.isvalid = False
        self.errorcode = ErrorCode.null.value

# Classe para organização das imagens compactadas
# Class for organizing compressed images
# Clase para organizar imágenes comprimidas
class retorno_face_match_ImgsxCadastro:
    def __init__(self):
        self.maior_score = 1
        self.menor_score = 1
        self.desvio_padrao = 0

class face_match_ImgsxCadastro:
    def __init__(self):
        self.ImagemPrincipal = ""
        self.ImagemSecundaria = ""
        self.Threshold = 0.52

class ImagensCompactadas:
    def __init__(self):
        self.imagem_principal = None
        self.imagem_segundaria = None
        self.process_ok = False

# class FaceCadastroPost(object):
#     def __init__(self, j):
#         self.__dict__ = json.loads(j)


class FaceCadastroRetorno1xn:
    def __init__(self):
        self.cadastrados = ""
        self.imagens_nao_cadastradas = {}
        self.errorcode = ErrorCode.null.value

# Classe genérica para retorno facematch 1xn imagens e videos.
# Generic class to return 1xn facematch images and videos.
# Clase genérica para devolver imágenes y videos 1xn facematch.
class FacematchRetorno1xn:
    def __init__(self):
        self.errorcode = ErrorCode.null.value