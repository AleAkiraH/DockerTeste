# Libs necessárias para utilização dessa folha
# Libs Externas
import base64
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
import os
import imutils

def file_to_base64(caminho_imagem):
    b64 = base64.b64encode(open(caminho_imagem,"rb").read())    
    return b64.decode("utf8")

def base64_to_img_pil(base64_string):
    if(isinstance(base64_string, str)):
        imagem = Image.open(BytesIO(base64.b64decode(base64_string)))
    return imagem

def base64_to_img_npar(base64_string):
    buffer = cv2.imencode('.jpg', base64_to_img_pil(base64_string))[0]
    image_bs64 = base64.b64encode(buffer) 
    return np.array(Image.open(BytesIO(base64.b64decode(image_bs64))))

def img_pil_to_base64(imagem):
    buffered = BytesIO()
    imagem.save(buffered, format=imagem.format)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def img_npar_to_base64(np_imagem):
    output_bytes = BytesIO()
    pil_img = Image.fromarray(np_imagem)
    pil_img.save(output_bytes, 'JPEG')
    bytes_data = output_bytes.getvalue()
    base64_str = str(base64.b64encode(bytes_data), 'utf-8')    
    return base64_str

def base64_to_img(base64_string):
    image = base64.b64decode(base64_string)
    img_np = np.frombuffer(image, np.uint8)
    return cv2.imdecode(img_np, cv2.COLOR_BGR2GRAY)

def rotacionar(base64_image_string, angle, img_object = False):
    image = base64_to_img(base64_image_string)
    image = imutils.rotate_bound(image, angle)
    buffer = cv2.imencode('.jpg', image)[1]
    image_bs64 = base64.b64encode(buffer) 

    if (img_object):
        result_align = Image.open(BytesIO(base64.b64decode(image_bs64)))
        return result_align
    else:
        return image_bs64.decode("utf-8", "ignore")

def getfiles(dir, extensao):
    all_files = list()
    for root, dirs, files in os.walk(dir):
        for f in files:
            fullpath = os.path.join(root, f)
            if os.path.splitext(fullpath)[1] == '.'+ str(extensao) +'':
                all_files.append(str(fullpath))
    return all_files