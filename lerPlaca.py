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
# OBS: O Flask precisa da localização correta. Se o script estiver no raiz, use o caminho relativo.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "models/chave.json"

# Inicialização dos modelos YOLO
model_carros = YOLO('models/yolov8_carros.pt')
model_placas = YOLO('models/yolov8_placas.pt')

# Configuração da aplicação Flask
# Definimos o diretório raiz para os templates/arquivos estáticos servidos (opcional, mas bom para organização)
# O root_path é o caminho do diretório do script atual.
app = Flask(__name__, static_url_path='/uploads', static_folder='uploads')
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

FILENAME = 'imagem_atual.jpg'

# O diretório onde o index.html está (assumimos que é o mesmo que o script principal)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


# --- Funções Auxiliares (Omitidas para brevidade, pois não foram alteradas) ---

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

def crop_para_base64(crop_imagem):
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

def processar_imagem(imagem):
    veiculos_detectados = []
    caixas_carros = object_detector.detectar_carros(imagem)

    for i, carro in enumerate(caixas_carros):
        x1, y1, x2, y2 = map(int, carro)
        crop_carro = imagem[y1:y2, x1:x2]
        cv2.rectangle(imagem, (x1, y1), (x2, y2), (0, 0, 255), 2)
        crop_carro_base64 = crop_para_base64(crop_carro)
        
        placa_identificada = None
        crop_placa_base64 = None

        caixas_placas = object_detector.detectar_placas(crop_carro)

        if caixas_placas is not None and len(caixas_placas) > 0:
            placa = caixas_placas[0] 
            px1, py1, px2, py2 = map(int, placa)
            
            crop_placa = crop_carro[py1:py2, px1:px2]
            
            texto_placa = enviar_para_google_vision(crop_placa)
            
            if texto_placa:
                placa_identificada = texto_placa
                crop_placa_base64 = crop_para_base64(crop_placa)

                cv2.rectangle(imagem, (px1 + x1, py1 + y1), (px2 + x1, py2 + y1), (0, 255, 0), 2)
                cv2.putText(imagem, placa_identificada, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        if placa_identificada:
            veiculos_detectados.append({
                'placa': placa_identificada,
                'crop_carro_base64': crop_carro_base64,
                'crop_placa_base64': crop_placa_base64,
            })
    
    return veiculos_detectados, imagem

# --- ROTA RAIZ (Nova) ---
@app.route('/')
def serve_index():
    """Serve o arquivo index.html que está no diretório raiz do script."""
    # Usamos send_from_directory para servir o arquivo
    return send_from_directory(ROOT_DIR, 'index.html')


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
    veiculos_detectados, imagem_resultado = processar_imagem(imagem)
    
    imagem_resultado = cv2.resize(imagem_resultado, (500, 500))
    resultado_nome = 'resultado_' + FILENAME
    resultado_path_sistema = os.path.join(UPLOAD_FOLDER, resultado_nome)

    cv2.imwrite(resultado_path_sistema, imagem_resultado)
    
    resultado_url = f"{UPLOAD_FOLDER}/{resultado_nome}"
    
    return jsonify({
        'numero_veiculos': len(veiculos_detectados),
        'veiculos': veiculos_detectados, 
        'placas': [v['placa'] for v in veiculos_detectados], 
        'imagem_resultado': resultado_url
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)