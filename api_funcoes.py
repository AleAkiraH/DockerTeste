# Libs necessárias para utilização dessa folha
# Libs Externas
# Libs required to use this sheet
# External Libs
# Libs requeridos para usar esta hoja
# Libs externas
import base64
from io import BytesIO
import json
from flask import jsonify
from PIL import Image
import numpy as np
import face_recognition
import sys
import cv2
# Libs Internas
# Libs Internal
# Libs Internas
import api_classes
import Util
import compactacao

# Função principal responsável por orquestrar a comparação das duas imagens. Passando o objeto recebido que deve conter Threshold e os 2 base64 referente as imagens.
# Main function responsible for orchestrating the comparison of the two images. Passing the received object that must contain Threshold and the 2 base64 referring to the images.
# Función principal responsable de orquestar la comparación de las dos imágenes. Al pasar el objeto recibido que debe contener Threshold y los 2 base64 que hacen referencia a las imágenes.
def exec_face_match(face_match_post):
    retorno = api_classes.FacematchRetorno()
    # Função para validar o envio do Threshold, quando o Threshold não é informado no post, é utilizado o valor de 0.52.
    threshold_informado = validar_threshold(face_match_post)
    # As imagens recebidas são compactadas antes de serem passadas pelo algoritimo de reconhecimento facial.
    compactados = comprimir_imagens(face_match_post, retorno)
    # Validação se a compactação foi bem sucedida.
    if(compactados.process_ok):
        # Função para retornar o resultado da comparação das 2 imagens.
        retorno = face_match_compare(compactados, face_match_post.Threshold)

        # Validação para determinar se o score obtido nas comparações é maior ou menor que o threshold informado.
        if(threshold_informado and retorno.isvalid):
            retorno.isequal = float(retorno.score) < float(face_match_post.Threshold)
    # Retorno do resultado em objeto json
    return  json.dumps(retorno.__dict__)

# Função principal responsável por orquestrar a comparação de uma unica imagem com um banco de imagens cadastradas no servidor.
# Main function responsible for orchestrating the comparison of a single image with a database of images registered on the server.
# Función principal responsable de organizar la comparación de una sola imagen con una base de datos de imágenes registradas en el servidor.
def exec_face_match1xnImagem(face_match_post):
    retorno = api_classes.FacematchRetorno1xn()
    # Função para validar o envio do Threshold, quando o Threshold não é informado no post, é utilizado o valor de 0.52.
    validar_threshold(face_match_post)
    # As imagens recebidas são compactadas antes de serem passadas pelo algoritimo de reconhecimento facial.
    compactados = comprimir_imagens1xn(face_match_post, retorno)
    # Validação se a compactação foi bem sucedida.
    if(compactados.process_ok):
        # Função para retornar o resultado da comparação da imagem com a base de imagens cadastradas no servidor.
        retorno = realizar_comparacoes1xn(compactados.imagem_principal, face_match_post.Threshold)
    # Retorno do resultado em objeto json
    return  json.dumps(retorno.__dict__)

def realizar_comparacoes1xn(imagem_para_comparar, Threshold):
    retorno = api_classes.FacematchRetorno1xn()

    try:
        imagem_carregada_encode = encontrar_face(imagem_para_comparar)[0]
    except:
        retorno.errorcode = 1
        return retorno
    

    db_faces = carregar_db_faces()
    db_img_encode = []
    db_img_name = []

    for db_item in db_faces:
        nome_pessoa_db = db_item.split('\\')[len(db_item.split('\\'))-1]
        try:
            db_img_encode.append(np.load(db_item)[0])
            db_img_name.append(nome_pessoa_db)
        except:
            pass
    

    matches = face_recognition.compare_faces(db_img_encode, imagem_carregada_encode, Threshold) # 0.4721197155715067
    retorno.encontrado = False
    index_comparacoes = 0
    score = 1
    for item in matches:
        if (matches[index_comparacoes]):
            if (score > float(face_recognition.face_distance([db_img_encode[index_comparacoes]], imagem_carregada_encode))):
                score = float(face_recognition.face_distance([db_img_encode[index_comparacoes]], imagem_carregada_encode))
                retorno.encontrado = True
                retorno.id = str(db_img_name[index_comparacoes].split(';')[0]).replace('.npy','')

        index_comparacoes = index_comparacoes + 1
    return retorno

# Função responsável por validar se o threshold foi informado, caso não tenha sido, o padrão determinado é de 0.52.
# Function responsible for validating whether the threshold was informed, if it has not been, the determined standard is 0.52.
# Función responsable de validar si el threshold fue informado, si no lo ha sido, el estándar determinado es 0.52.
def validar_threshold(face_match_post):
    retorno = False
    if (face_match_post.Threshold is None):
        face_match_post.Threshold = 0.52
    elif(isinstance(face_match_post.Threshold, str)):
        if(len(face_match_post.Threshold) < 1):
            face_match_post.Threshold = 0.52
        else:
            face_match_post.Threshold = float(face_match_post.Threshold)
            retorno = True
    else:
        retorno = True

    return retorno

# Função responsável por comprimir as imagens enviadas afim de agilizar o processo de comparação das imagens.
# Function responsible for compressing the images sent in order to streamline the image comparison process.
# Función responsable de comprimir las imágenes enviadas para agilizar el proceso de comparación de imágenes.
def comprimir_imagens(face_match_post, face_match_retorno):
    retorno = api_classes.ImagensCompactadas()

    try:
        retorno.imagem_principal = compactacao.comprimir_imagem(face_match_post.ImagemPrincipal, False)
        try:
            retorno.imagem_segundaria = compactacao.comprimir_imagem(face_match_post.ImagemSecundaria, False)
            retorno.process_ok = True
        except:
            face_match_retorno.errorcode = api_classes.ErrorCode.segunda_imagem_invalida.value
    except:
        face_match_retorno.errorcode = api_classes.ErrorCode.primeira_imagem_invalida.value
        
    return retorno

# Função responsável por comprimir as imagens enviadas afim de agilizar o processo de comparação das imagens.
# Function responsible for compressing the images sent in order to streamline the image comparison process.
# Función responsable de comprimir las imágenes enviadas para agilizar el proceso de comparación de imágenes.
def comprimir_imagens1xn(face_match_post, face_match_retorno):
    retorno = api_classes.ImagensCompactadas()

    try:
        retorno.imagem_principal = compactacao.comprimir_imagem(face_match_post.ImagemPrincipal, False)
        retorno.process_ok = True
    except:
        face_match_retorno.errorcode = api_classes.ErrorCode.imagem_invalida.value
        
    return retorno

# Função responsável por comparar as imagens previamente compactadas, de acordo com o threshold informado.
# Function responsible for comparing previously compressed images, according to the informed threshold.
# Función responsable de comparar imágenes previamente comprimidas, de acuerdo con el threshold informado.
def face_match_compare(compactados, threshold):
    retorno = api_classes.FacematchRetorno()
    
    imagem_principal = encontrar_face(compactados.imagem_principal)
    if not (len(imagem_principal) == 0):
        imagem_principal = imagem_principal[0]
        imagem_segundaria = encontrar_face(compactados.imagem_segundaria)

        if not (len(imagem_segundaria) == 0):
            imagem_segundaria = imagem_segundaria[0]
            retorno.score = float(face_recognition.face_distance([imagem_principal], imagem_segundaria))
            retorno.isvalid = True
        else:
            retorno.errorcode = api_classes.ErrorCode.segunda_imagem_sem_face.value
    else:
        retorno.errorcode = api_classes.ErrorCode.primeira_imagem_sem_face.value
    
    return retorno

# Função responsável por encontrar os pontos faciais.
# Function responsible for finding facial points.
# Función responsable de encontrar puntos faciales.
def encontrar_face(imagem):
    face = []
    for i in range(0, 4):
        face = get_encoding(imagem, i)
        
        if not (len(face) == 0):
            break
    
    return face

# Função responsável por rotacionar as imagens quando necessário.E por fim retornar o array das imagens para processamento na funçãod e comparação.
# Function responsible for rotating images when necessary. Finally, return the array of images for processing in the function and comparison.
# Función responsable de rotar las imágenes cuando sea necesario. Finalmente, devuelva la matriz de imágenes para procesar en la función y comparación.
def get_encoding(imagem, rot):
    if(rot > 0):
        imagem_rotacionada = ((Util.rotacionar(imagem,90 * rot, True)).convert('RGB'))
        np_array = np.array(imagem_rotacionada)
    else:
        np_array = np.array(Image.open(BytesIO(base64.b64decode(imagem))).convert('RGB'))

    return face_recognition.face_encodings(np_array)

# Função responsável por cadastrar os .npy no servidor. Através das imagens em .jpg 
# Function responsible for registering .npy on the server. Through the images in .jpg
# Función responsable de registrar .npy en el servidor. A través de las imágenes en .jpg
def salvar_db_faces_npy(caminho_fotos, caminho_array):
    retorno = api_classes.FaceCadastroRetorno1xn()
    imagens_recebidas = Util.getfiles(caminho_fotos,'jpg')
    
    npy_registradas = []
    for item_list in Util.getfiles(caminho_array,'npy'):
        npy_registradas.append(item_list.split('\\')[len(item_list.split('\\'))-1].replace('.npy',''))
    
    data_img = {}
    data_img['imagens'] = []

    for imagem_item in imagens_recebidas:
        nome_foto = imagem_item.split('\\')[len(imagem_item.split('\\'))-1].replace('.jpg','')
        if nome_foto in npy_registradas:
            continue
        imagem_item = Util.file_to_base64(imagem_item)
        array_img = encontrar_face(imagem_item)
        if (len(array_img) < 1):
            data_img['imagens'].append({
            "id_img": ""+str(imagem_item["id_img"])+""
        })
        else:
            img_pil = Image.open(BytesIO(base64.b64decode(imagem_item))).convert('RGB')
            np.save('imgs_array\\' + str(nome_foto), array_img)
    
    qtd_erros = len(data_img['imagens'])
    qtd_recebidas = len(imagens_recebidas)

    erros_recebidas_result = qtd_recebidas - qtd_erros

    retorno.cadastrados = str(erros_recebidas_result) +"/"+ str(qtd_recebidas)
    retorno.imagens_nao_cadastradas = data_img
    retorno.errorcode = api_classes.ErrorCode.null.value

    return json.dumps(retorno.__dict__)

# Função responsável por carregar e armazenar em variavel as faces cadastradas no servidor
# Function responsible for loading and storing in variable the faces registered on the server
# Función responsable de cargar y almacenar en variable las caras registradas en el servidor
def carregar_db_faces():
    db_faces = []
    db_faces = Util.getfiles('imgs_array','npy')
    return db_faces

# Remover duplicados da lista
# Remove duplicates from the list
# Eliminar duplicados de la lista
def remover_duplicados(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

# Função principal responsável por orquestrar a comparação de uma unica imagem com um banco de imagens cadastradas no servidor.
# Main function responsible for orchestrating the comparison of a single image with a database of images registered on the server.
# Función principal responsable de organizar la comparación de una sola imagen con una base de datos de imágenes registradas en el servidor.
def exec_face_match1xnVideo(tolerancia, video):    
    retorno = api_classes.FacematchRetorno1xn()
    video_capturado = cv2.VideoCapture(video)
    
    # Definições de algumas variaveis
    # Definitions of some variables
    diretorio_com_faces = "dev\\fotos"
    localizacoes_faces = []
    codificacao_faces = []
    nomes_faces = []
    processar_este_frame = True
    # contador de frames para limitação da verificação
    # frame counter to limit verification
    # contador de cuadros para limitar la verificación
    contagem_frame = 0
    # de quantos em quantos frames irão ocorrer as avaliações
    # how many in how many frames will ratings take place
    # cuántos en cuántos cuadros tendrán lugar las clasificaciones
    selecionar_frames_do_video = 15
    # lista todos os nomes conhecidos encontrados
    # lists all known names found
    # enumera todos los nombres conocidos encontrados
    encontrados = [] 
    conhecido_codificacao_faces = []
    conhecido_face_nomes = []

    # Carrega base de imagens cadastradas em .npy
    # Load base of images registered in .npy
    # Base de carga de imágenes registradas en .npy
    db_faces = carregar_db_faces()
    db_img_encode = []
    db_img_name = []

    # Definição das imagens e organização em lista.
    # Definition of images and organization in list.
    # Definición de imágenes y organización en lista.
    for db_item in db_faces:
        nome_pessoa_db = db_item.split('\\')[len(db_item.split('\\'))-1].replace('.npy','')
        try:
            conhecido_codificacao_faces.append(np.load(db_item)[0])
            conhecido_face_nomes.append(nome_pessoa_db)
        except:
            pass
    
    # Leitura do vídeo, o loop correrá de acordo com o número de frames previamento preenchido na variavel "selecionar_frames_do_video".
    # Read the video, the loop will run according to the number of frames pre-filled in the variable "select_frames_do_video".
    # Lea el video, el bucle se ejecutará de acuerdo con el número de fotogramas rellenados previamente en la variable "select_frames_do_video".
    while True:
        ret, frame = video_capturado.read()

        try:
            rgb_frame = frame[:, :, ::-1]
        except:
            break
        
        processar_este_frame = False
        contagem_frame = contagem_frame + 1
        if contagem_frame == selecionar_frames_do_video:
            contagem_frame = 0
            processar_este_frame = True

        if processar_este_frame:
            localizacoes_faces = face_recognition.face_locations(rgb_frame)
            codificacao_faces = face_recognition.face_encodings(rgb_frame, localizacoes_faces)

            nomes_faces = []
            # a cada frame comparado ele valida se exxiste no banco de faces cadastrados no servidor.
            # each frame compared it validates if it exists in the face bank registered on the server.
            # cada fotograma comparado se valida si existe en el banco frontal registrado en el servidor.
            for face_encoding in codificacao_faces:
                matches = face_recognition.compare_faces(conhecido_codificacao_faces, face_encoding, tolerancia)
                nome = "Desconhecido"

                # todos os nomes encontrados são colocados em uma lista para serem retornados no final da função.
                # all names found are placed in a list to be returned at the end of the function.
                # todos los nombres encontrados se colocan en una lista para ser devueltos al final de la función.
                if True in matches:
                    first_match_index = matches.index(True)
                    nome = conhecido_face_nomes[first_match_index]
                    encontrados.append(nome)

                nomes_faces.append(nome)
    # antes de retornar os nomes, a função remover duplicados é executada afim de remover nomes repetidos encontrados no vídeo.
    # before returning the names, the remove duplicates function is performed in order to remove repeated names found in the video.
    # antes de devolver los nombres, la función eliminar duplicados se realiza para eliminar los nombres repetidos que se encuentran en el video.
    retorno.encontrados = remover_duplicados(encontrados)
    # Retorno do resultado em objeto json.
    # Result return in json object.
    # Resultado devuelto en objeto json.
    return json.dumps(retorno.__dict__)