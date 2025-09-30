import os
import cv2
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
from ultralytics import YOLO
import base64
from google.cloud import vision
import re

# Caminho do arquivo de chave do Google
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "models/chave.json"

# Inicialização dos modelos YOLO
model_carros = YOLO('models/yolov8_carros.pt')
model_placas = YOLO('models/yolov8_placas.pt')

# Configuração da aplicação Flask
app = Flask(__name__, static_url_path='/uploads', static_folder='uploads')
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

FILENAME = 'imagem_atual.jpg'

# --- Funções Auxiliares (Não alteradas) ---

class ObjectDetector:
    def __init__(self, model_carros_path='models/yolov8_carros.pt', model_placas_path='models/yolov8_placas.pt'):
        self.model_carros = YOLO(model_carros_path)
        self.model_placas = YOLO(model_placas_path)

    def detectar_carros(self, imagem):
        resultados = self.model_carros(imagem)
        return resultados[0].boxes.xyxy

    def detectar_placas(self, crop_imagem):
        resultados = self.model_placas(crop_imagem)
        return resultados[0].boxes.xyxy

# Função para converter a imagem cropada em base64
def crop_para_base64(crop_imagem):
    # Garantir que a imagem tem pelo menos 1 pixel de altura/largura
    if crop_imagem.shape[0] == 0 or crop_imagem.shape[1] == 0:
        return None
    retval, buffer = cv2.imencode('.jpg', crop_imagem)
    return base64.b64encode(buffer).decode('utf-8')

def processar_texto_placa(texto_detectado):
    texto_limpo = texto_detectado.replace(" ", "").replace("-", "")
    padrao_placa = re.compile(r'([A-Za-z]{3}[0-9]{1}[A-Za-z]{1}[0-9]{2}|[A-Za-z]{3}[0-9]{4})')
    correspondencia = padrao_placa.search(texto_limpo)
    if correspondencia:
        return correspondencia.group(0)
    return None

def enviar_para_google_vision(crop_imagem):
    client = vision.ImageAnnotatorClient()
    _, buffer = cv2.imencode('.jpg', crop_imagem)
    image = vision.Image(content=buffer.tobytes())
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        texto_detectado = texts[0].description.strip().replace("\n", "")
        texto_placa = processar_texto_placa(texto_detectado)
        return texto_placa
    return None

object_detector = ObjectDetector()

# 🚨 ALTERAÇÃO CHAVE: Modificando a saída para agrupar os resultados por carro
def processar_imagem(imagem):
    # Lista que vai conter todos os dados (carro, placa, crops)
    veiculos_detectados = []

    # Detecta os carros na imagem
    caixas_carros = object_detector.detectar_carros(imagem)

    for i, carro in enumerate(caixas_carros):
        x1, y1, x2, y2 = map(int, carro)
        crop_carro = imagem[y1:y2, x1:x2]
        
        # Desenha a caixa do carro na imagem principal
        cv2.rectangle(imagem, (x1, y1), (x2, y2), (0, 0, 255), 2)
        
        # Converte o crop do carro para base64
        crop_carro_base64 = crop_para_base64(crop_carro)
        
        placa_identificada = None
        crop_placa_base64 = None

        # Detecta as placas no crop do carro
        caixas_placas = object_detector.detectar_placas(crop_carro)

        if caixas_placas is not None and len(caixas_placas) > 0:
            # Pegamos apenas a primeira placa encontrada por carro para simplificar
            placa = caixas_placas[0] 
            px1, py1, px2, py2 = map(int, placa)
            
            crop_placa = crop_carro[py1:py2, px1:px2]
            
            # Envia a placa para o Google Vision e processa o texto detectado
            texto_placa = enviar_para_google_vision(crop_placa)
            
            if texto_placa:
                placa_identificada = texto_placa
                crop_placa_base64 = crop_para_base64(crop_placa)

                # Desenha a caixa da placa na imagem original
                cv2.rectangle(imagem, (px1 + x1, py1 + y1), (px2 + x1, py2 + y1), (0, 255, 0), 2)
                
                # Opcional: Adicionar a placa na imagem original (para visualização)
                cv2.putText(imagem, placa_identificada, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)


        # Adiciona o resultado na lista de veículos
        if placa_identificada:
            veiculos_detectados.append({
                'placa': placa_identificada,
                'crop_carro_base64': crop_carro_base64,
                'crop_placa_base64': crop_placa_base64,
            })
    
    return veiculos_detectados, imagem


# Endpoint da API para upload de imagem
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(FILENAME)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    imagem = cv2.imread(filepath)
    # 🚨 ALTERAÇÃO: Receber a lista de veículos e a imagem resultado
    veiculos_detectados, imagem_resultado = processar_imagem(imagem)
    
    imagem_resultado = cv2.resize(imagem_resultado, (500, 500))
    resultado_nome = 'resultado_' + FILENAME
    resultado_path_sistema = os.path.join(UPLOAD_FOLDER, resultado_nome)

    cv2.imwrite(resultado_path_sistema, imagem_resultado)
    
    # Retorna o caminho limpo (URL-friendly)
    resultado_url = f"{UPLOAD_FOLDER}/{resultado_nome}"
    
    # 🚨 ALTERAÇÃO: Retorna a lista de veículos agrupados
    return jsonify({
        'numero_veiculos': len(veiculos_detectados),
        'veiculos': veiculos_detectados, # Lista com todos os dados agrupados
        'placas': [v['placa'] for v in veiculos_detectados], # Lista simples de placas
        'imagem_resultado': resultado_url
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)