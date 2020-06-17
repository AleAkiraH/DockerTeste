from PIL import Image, ImageOps
from io import BytesIO
import base64

__comprimir_tamanho = True
__size_maximo_imagem = 1024
__optimize = True
__qualidade_porcentual = 70
__modificar_qualidade = True

def set_comprimir_tamanho(value):
    global __comprimir_tamanho
    __comprimir_tamanho = value

def set_size_maximo_imagem(value):
    global __size_maximo_imagem
    __size_maximo_imagem = value

def set_optimize(value):
    global __optimize
    __optimize = value

def set_qualidade_porcentual(value):
    global __qualidade_porcentual
    __qualidade_porcentual = value

def set_modificar_qualidade(value):
    global __modificar_qualidade
    __modificar_qualidade = value

def comprimir_imagem(imagem, retornar_objeto_imagem = False):
    if(isinstance(imagem, str)):
        imagem = Image.open(BytesIO(base64.b64decode(imagem)))

    nova_imagem =  __comprimir_tamanho_imagem(imagem) if(__comprimir_tamanho) else imagem
    buffered = BytesIO()

    if(__modificar_qualidade):
        nova_imagem.save(buffered, format=imagem.format, optimize=__optimize, quality=__qualidade_porcentual)
    else:
        nova_imagem.save(buffered, format=imagem.format, optimize=__optimize)
    
    return Image.open(BytesIO(buffered.getvalue())) if(retornar_objeto_imagem) else base64.b64encode(buffered.getvalue()).decode("utf-8")

def __comprimir_tamanho_imagem(imagem):
    tamanho_compressao = imagem.size[0] if imagem.size[0] > imagem.size[1] else imagem.size[1]
    if(tamanho_compressao <= __size_maximo_imagem):
        return imagem
    else:
        porcentual_compressao = __calcular_porcentagem_compressao(tamanho_compressao)
        size = __calcular_tamanho_porcentual(imagem.size[0], imagem.size[1], porcentual_compressao)
        return ImageOps.fit(imagem, size, Image.ANTIALIAS)

def __calcular_porcentagem_compressao(tamanho):
    porcentagem = 0
    for porcentagem in range(0, 99):
        if((tamanho - ((tamanho * porcentagem) / 100)) <= __size_maximo_imagem):
            break
    return porcentagem

def __calcular_tamanho_porcentual(tamanho0, tamanho1, porcentagem):
    return (int(tamanho0 - ((tamanho0 * porcentagem) / 100)), int(tamanho1 - ((tamanho1 * porcentagem) / 100)))
