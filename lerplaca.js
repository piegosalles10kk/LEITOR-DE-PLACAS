const express = require('express');
const fileUpload = require('express-fileupload');
const cors = require('cors');
const cv = require('opencv4nodejs');
const fs = require('fs');
const path = require('path');
const base64 = require('base64-js');
const { ImageAnnotatorClient } = require('@google-cloud/vision');
const YOLO = require('yolo-v8'); // Suponha que exista um pacote para YOLOv8

// Carregar variáveis de ambiente
process.env.GOOGLE_APPLICATION_CREDENTIALS = "models/chave.json";

// Inicializar Express
const app = express();
app.use(cors());
app.use(fileUpload());

// Configuração do diretório de upload
const UPLOAD_FOLDER = 'uploads';
if (!fs.existsSync(UPLOAD_FOLDER)) {
    fs.mkdirSync(UPLOAD_FOLDER);
}

const FILENAME = 'imagem_atual.jpg';

// Inicialização dos modelos YOLO
const modelCarros = new YOLO('models/yolov8_carros.pt');
const modelPlacas = new YOLO('models/yolov8_placas.pt');

class ObjectDetector {
    async detectarCarros(imagem) {
        const resultados = await modelCarros.detect(imagem);
        return resultados;
    }

    async detectarPlacas(cropImagem) {
        const resultados = await modelPlacas.detect(cropImagem);
        return resultados;
    }
}

const objectDetector = new ObjectDetector();

// Função para converter a imagem em base64
function cropParaBase64(cropImagem) {
    const buffer = cv.imencode('.jpg', cropImagem);
    return buffer.toString('base64');
}

// Processar texto da placa usando regex
function processarTextoPlaca(textoDetectado) {
    const textoLimpo = textoDetectado.replace(/[\s-]/g, "");
    const padraoPlaca = /([A-Za-z]{3}[0-9]{1}[A-Za-z]{1}[0-9]{2}|[A-Za-z]{3}[0-9]{4})/;
    const correspondencia = padraoPlaca.exec(textoLimpo);
    return correspondencia ? correspondencia[0] : null;
}

// Enviar imagem para o Google Vision e processar texto da placa
async function enviarParaGoogleVision(cropImagem) {
    const client = new ImageAnnotatorClient();
    const buffer = cv.imencode('.jpg', cropImagem);
    const [result] = await client.textDetection({ image: { content: buffer.toString('base64') } });
    const texts = result.textAnnotations;
    
    if (texts.length > 0) {
        const textoDetectado = texts[0].description.replace(/\n/g, "").trim();
        return processarTextoPlaca(textoDetectado);
    }
    return null;
}

// Função principal de processamento de imagem
async function processarImagem(imagem) {
    let todasAsPlacas = [];
    const caixasCarros = await objectDetector.detectarCarros(imagem);

    for (const carro of caixasCarros) {
        const { x1, y1, x2, y2 } = carro; // supõe-se que as caixas retornem um objeto com coordenadas
        const cropCarro = imagem.getRegion(new cv.Rect(x1, y1, x2 - x1, y2 - y1));

        const caixasPlacas = await objectDetector.detectarPlacas(cropCarro);
        for (const placa of caixasPlacas) {
            const { x1: px1, y1: py1, x2: px2, y2: py2 } = placa; 
            const cropPlaca = cropCarro.getRegion(new cv.Rect(px1, py1, px2 - px1, py2 - py1));

            const textoPlaca = await enviarParaGoogleVision(cropPlaca);
            if (textoPlaca) {
                todasAsPlacas.push(textoPlaca);
            }
        }
    }
    return todasAsPlacas;
}

// Endpoint da API para upload de imagem
app.post('/upload', async (req, res) => {
    if (!req.files || !req.files.file) {
        return res.status(400).json({ error: 'No file part' });
    }

    const file = req.files.file;
    const filePath = path.join(UPLOAD_FOLDER, FILENAME);
    await file.mv(filePath);

    const imagem = cv.imread(filePath);
    const placasIdentificadas = await processarImagem(imagem);

    const resultadoPath = path.join(UPLOAD_FOLDER, 'resultado_' + FILENAME);
    cv.imwrite(resultadoPath, imagem);

    res.json({
        numero_veiculos: placasIdentificadas.length,
        placas: placasIdentificadas,
        imagem_resultado: resultadoPath
    });
});

// Iniciar servidor
const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Servidor rodando na porta ${PORT}`);
});
