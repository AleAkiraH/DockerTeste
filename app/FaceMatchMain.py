# Libs necessárias para utilização dessa api
# Libs required to use this api
# Libs requeridas para usar esta API
# Libs Externas
# Libs External
# Libs externa
from flask import Flask, jsonify, request
import json
import datetime
import base64
import uuid
import os
import math
# Libs Internas
# Libs Internal
# Libs interna
import api_classes
import api_funcoes
        
app = Flask(__name__)
def somar(valores):
                soma = 0
                for v in valores:
                    soma += v
                return soma
            
def media(valores):
    soma = somar(valores)
    qtd_elementos = len(valores)
    media = soma / float(qtd_elementos)
    return media
            
def variancia(valores):
    _media = media(valores)
    soma = 0
    _variancia = 0

    for valor in valores:
        soma += math.pow( (valor - _media), 2)
    _variancia = soma / float( len(valores) )
    return _variancia

def desvio_padrao(valores):
    return math.sqrt( variancia(valores) )

# Método de entrada chama facematch 1x1
# 1x1 facematch input method
# 1x1 método de entrada de facematch
@app.route("/Api/FaceMatch/", methods=['POST'])
def index():
    # variável recebe objeto json enviado pelo post. Objeto recebido deve conter Threshold e os 2 base64 referente as imagens a serem comparadas.
    # variable receives json object sent by post. Received object must contain Threshold and the 2 base64 referring to the images to be compared.
    # variable recibe objeto json enviado por "POST". El objeto recibido debe contener "Threshold" y los 2 base64 que se refieren a las imágenes a comparar.
    face_match_post = api_classes.FaceMatchPost(json.dumps(request.get_json()))

    # executa a função principal responsavel por orquestrar a comparação das duas imagens. Passando o objeto recebido que deve conter Threshold e os 2 base64 referente as imagens
    # performs the main function responsible for orchestrating the comparison of the two images. Passing the received object that must contain Threshold and the 2 base64 referring to the images
    # realiza la función principal responsable de orquestar la comparación de las dos imágenes. Al pasar el objeto recibido que debe contener Threshold y el 2 base64 que hace referencia a las imágenes
    return api_funcoes.exec_face_match(face_match_post)

# Método de entrada chama facematch 1xn imagem
# Input method calls facematch 1xn image
# El método de entrada llama a facematch 1xn image
@app.route("/Api/FaceMatch1xnImagem/", methods=['POST'])
def FaceMatch1xnImagem():
    # variável recebe objeto json enviado pelo post. Objeto recebido deve conter Threshold e o base64 referente a imagem que deseja consultar na base de imagens registrada na API.
    # variable receives json object sent by post. Received object must contain Threshold and base64 referring to the image you want to consult in the image base registered in the API.
    # variable recibe objeto json enviado por "POST". El objeto recibido debe contener Threshold y base64 que se refieren a la imagen que desea consultar en la base de imágenes registrada en la API.
    face_match_post = api_classes.FaceMatchPost(json.dumps(request.get_json()))

    # armazena o resultado para retornar ao usuario que fez a chamada para api. o retorno será um objeto json. 
    # stores the result to return to the user who made the call to api. the return will be a json object.  
    # almacena el resultado para devolverlo al usuario que realizó la llamada a la API. El retorno será un objeto json. 
    resultado = (api_funcoes.exec_face_match1xnImagem(face_match_post))
    print(str(resultado))
    return resultado

# Método de entrada chama facematch 1xn video
# Input method calls facematch 1xn video
# Método de entrada llama facematch 1xn video
@app.route("/Api/FaceMatch1xnVideo/", methods=['POST'])
def FaceMatch1xnVideo():
    # variavel recebe objeto json enviado pelo post. Objeto recebido deve conter Threshold e o base64 referente ao video que deseja consultar na base de imagens registrada na API.
    # variable receives json object sent by post. Received object must contain Threshold and base64 for the video you want to consult in the image base registered in the API.
    # variable recibe objeto json enviado por "POST". El objeto recibido debe contener Threshold y base64 para el video que desea consultar en la base de imágenes registrada en la API.
    face_match_post = api_classes.FaceMatchPost(json.dumps(request.get_json()))

    # Realiza a conversão do video base64 para escrever um arquivo.mp4 (Necessário para a checagem da função que virá a seguir).
    # Performs the conversion of the base64 video to write an .mp4 file (Necessary for checking the function that will follow).
    # Realiza la conversión del video base64 para escribir un archivo .mp4 (necesario para verificar la función que seguirá). 
     
    video_binary_string = base64.b64decode(face_match_post.video)
    video_binary_string = bytes(video_binary_string)
    decoded_string = base64.decodestring(video_binary_string)

    # Definição do caminho onde o arquivo será escrito, é utilizado um guid para atender a diversas requisições ao mesmo tempo.
    # Definition of the path where the file will be written, a guid is used to attend to several requests at the same time.
    # Definición de la ruta donde se escribirá el archivo, se utiliza un guid para atender varias solicitudes al mismo tiempo.
    diretorio_arquivo = "dev\\tempVideos\\"+str(uuid.uuid4())+".mp4"

    # criação do arquivo .mp4   
    # creating the .mp4 file 
    # creando el archivo .mp4
    with open(diretorio_arquivo, 'wb') as wfile:
        wfile.write(decoded_string)
    
    # armazena o resultado para retornar ao usuario que fez a chamada para api. o retorno será um objeto json.    
    # stores the result to return to the user who made the call to api. the return will be a json object.
    # almacena el resultado para devolverlo al usuario que realizó la llamada a la API. El retorno será un objeto json.
    resultado = api_funcoes.exec_face_match1xnVideo(tolerancia = face_match_post.Threshold, video = diretorio_arquivo)
    os.remove(diretorio_arquivo)
    print(str(resultado))
    return resultado

# Get simples para validação caso api esteja fora do ar.
# "Get" simple for validation if api is down.
# "Get" simples para validación si la API está inactiva.
@app.route("/AtualizarBancoImagens/", methods=['GET'])
def home():
    # função responsavel por carregar as imagens no diretório especifico. 
    # function responsible for loading the images in the specific directory.
    # función responsable de cargar las imágenes en el directorio específico.
    api_funcoes.salvar_db_faces_npy('dev\\fotos', 'imgs_array')
    return "Api FaceMatch - {}".format(datetime.datetime.now())
        
@app.route("/Api/face_match_ImgsxCadastro/", methods=['POST'])
def face_match_ImgsxCadastro():
    # variavel recebe objeto json enviado pelo post. Objeto recebido deve conter lista de imagens base64, Threshold, ImagemCadastrada.
    # variable receives json object sent by post. Received object must contain list of base64 images, Threshold, ImageCadastrada.
    # variable recibe objeto json enviado por correo. El objeto recibido debe contener una lista de imágenes base64, Threshold, ImageCadastrada.
    face_match_post = api_classes.FaceMatchPost(json.dumps(request.get_json()))
    # Instancia Objeto para organização das variaveis.
    # Instance Object for organizing variables.
    # Objeto de instancia para organizar variables.
    face_match_ImgsxCadastro = api_classes.face_match_ImgsxCadastro()
    # Instancia Objeto para organização do retorno das variaveis.
    # Instance Object for organizing the return of variables.
    # Objeto de instancia para organizar el retorno de variables.
    retorno = api_classes.retorno_face_match_ImgsxCadastro()
     
    resultado = []
    
    # Inicia as comparações para cada face recebida
    # Starts comparisons for each face received
    # Inicia comparaciones para cada cara recibida
    for imagem_item in face_match_post.imagens:
        face_match_ImgsxCadastro.ImagemPrincipal = face_match_post.ImagemCadastrada
        face_match_ImgsxCadastro.ImagemSecundaria = imagem_item["base64"]
        face_match_ImgsxCadastro.Threshold:0.52
        resultado.append(api_funcoes.exec_face_match(face_match_ImgsxCadastro))
    
    scores = []
    erros = []
    
    # Armazena os scores encontrados em uma lista
    # Stores scores found in a list
    # Almacena los puntajes encontrados en una lista
    for r in resultado:
        scores.append(json.loads(r)["score"])
        erros.append(json.loads(r)["errorcode"])
        
    # Registra os retornos no objeto para retorno.
    # Records returns in the object for return.
    # Registros devuelve en el objeto para devolución.
    if len(erros) == 0:
        retorno.erros = []
    else:
        retorno.erros = erros
    retorno.maior_score = max(scores, key=float) 
    retorno.menor_score = min(scores, key=float)
    retorno.desvio_padrao = desvio_padrao(scores)
    
    
    
    return json.dumps(retorno.__dict__)

@app.route("/", methods=['GET'])
def getsimples():
    # função responsavel por carregar as imagens no diretório especifico. 
    # function responsible for loading the images in the specific directory.
    # función responsable de cargar las imágenes en el directorio específico.
    return "Api FaceMatch - {}".format(datetime.datetime.now())
# Inicia uma instancia da api na porta definida para poder ser chamada.
# Start an instance of the api on the defined port so it can be called.
# Inicie una instancia de la API en el puerto definido para que se pueda llamar.
if __name__ == '__main__':
    print ('API_FACEMATCH INICIADA')
    app.run(host='127.0.0.1', port=6068)
    
