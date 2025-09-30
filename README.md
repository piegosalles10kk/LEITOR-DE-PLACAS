# 🚗 Locar Vision - Sistema de Detecção de Placas Veiculares

Sistema inteligente para detecção e reconhecimento automático de placas veiculares em imagens utilizando YOLO e Google Cloud Vision API.

## 🎯 Sobre o Projeto

O Locar Vision é um sistema de reconhecimento automático de placas veiculares (ALPR - Automatic License Plate Recognition) que combina modelos YOLO para detecção de veículos e placas com a Google Cloud Vision API para OCR (reconhecimento óptico de caracteres).

O sistema é capaz de:
- Detectar múltiplos veículos em uma imagem
- Identificar placas em cada veículo detectado
- Extrair o texto das placas usando OCR
- Suportar placas no formato brasileiro (antigo e Mercosul)
- Retornar imagens processadas com bounding boxes
- Fornecer crops individuais das placas detectadas

## ⚡ Funcionalidades

- **Detecção de Veículos**: Utiliza YOLOv8 para identificar carros na imagem
- **Detecção de Placas**: Segundo modelo YOLO especializado em placas
- **OCR Inteligente**: Google Cloud Vision API para leitura precisa do texto
- **Regex Avançado**: Processamento de texto para formatos de placa brasileiros
- **API RESTful**: Interface simples para integração
- **Interface Web**: Frontend HTML para testes e demonstração
- **Docker Ready**: Containerização para deploy facilitado
- **Deploy Fly.io**: Configuração pronta para deploy na nuvem

## 🛠 Tecnologias Utilizadas

### Backend
- **Python 3.9**
- **Flask** - Framework web
- **OpenCV** - Processamento de imagem
- **Ultralytics YOLO** - Detecção de objetos
- **Google Cloud Vision API** - OCR
- **NumPy** - Manipulação de arrays
- **Flask-CORS** - Habilitação de CORS

### Frontend
- **HTML5/CSS3/JavaScript**
- **Fetch API** - Requisições HTTP

### DevOps & Deploy
- **Docker** - Containerização
- **Fly.io** - Plataforma de deploy
- **Ubuntu/Debian** - Sistema base

## 📋 Pré-requisitos

- Python 3.9 ou superior
- Conta no Google Cloud Platform com Vision API habilitada
- Docker (opcional, para containerização)
- Conta no Fly.io (opcional, para deploy)

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/piegosalles10kk/LEITOR-DE-PLACAS
cd LEITOR-DE-PLACAS
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Crie as pastas necessárias
```bash
mkdir uploads models
```

## ⚙️ Configuração

### 1. Google Cloud Vision API

1. Crie um projeto no [Google Cloud Console](https://console.cloud.google.com)
2. Habilite a Vision API
3. Crie uma conta de serviço e baixe o arquivo JSON das credenciais
4. Salve o arquivo como `models/chave.json`

### 2. Modelos YOLO

Adicione os modelos treinados na pasta `models/`:
- `yolov8_carros.pt` - Modelo para detecção de veículos
- `yolov8_placas.pt` - Modelo para detecção de placas

## 📖 Como Usar

### Execução Local

1. **Inicie o servidor Flask**:
```bash
python lerPlaca2.py
```

2. **Abra o navegador** em `http://localhost:5000`

3. **Use a interface web**:
   - Abra o arquivo `upload.html` no navegador
   - Altere a URL da API para `http://localhost:5000/upload`
   - Selecione uma imagem com veículos
   - Clique em "Enviar Arquivo"

### Usando Docker

1. **Build da imagem**:
```bash
docker build -t locar-vision .
```

2. **Execute o container**:
```bash
docker run -p 5000:5000 locar-vision
```

### Deploy no Fly.io

1. **Instale o Fly CLI**:
```bash
curl -L https://fly.io/install.sh | sh
```

2. **Faça login**:
```bash
flyctl auth login
```

3. **Deploy**:
```bash
flyctl deploy
```

## 🔌 API Endpoints

### POST `/upload`

Envia uma imagem para processamento.

**Parâmetros:**
- `file`: Arquivo de imagem (multipart/form-data)

**Resposta de Sucesso:**
```json
{
  "numero_veiculos": 2,
  "placas": ["ABC1234", "XYZ5D67"],
  "imagem_resultado": "uploads/resultado_imagem_atual.jpg",
  "crops_base64": ["base64_string1", "base64_string2"]
}
```

**Resposta sem Detecção:**
```json
{
  "numero_veiculos": 0,
  "placas": [],
  "mensagem": "Não foi localizado placa nem veículo na imagem."
}
```

**Resposta de Erro:**
```json
{
  "error": "No file part"
}
```

## 📁 Estrutura do Projeto

```
locar-vision/
├── lerPlaca2.py          # Aplicação principal Python
├── lerplaca.js           # Versão alternativa em Node.js
├── upload.html           # Interface web para testes
├── teste.php             # Arquivo de teste (vazio)
├── dockerfile            # Configuração Docker
├── fly.toml              # Configuração Fly.io
├── package.json          # Configuração Node.js
├── requirements.txt      # Dependências Python
├── models/
│   ├── chave.json       # Credenciais Google Cloud
│   ├── yolov8_carros.pt # Modelo YOLO para carros
│   └── yolov8_placas.pt # Modelo YOLO para placas
└── uploads/             # Pasta para arquivos temporários
```

## 🎨 Exemplo de Uso

### Fluxo de Processamento

1. **Upload da Imagem**: Cliente envia imagem via POST
2. **Detecção de Veículos**: YOLO identifica carros na imagem
3. **Crop dos Veículos**: Extrai região de cada veículo
4. **Detecção de Placas**: YOLO identifica placas em cada veículo
5. **Crop das Placas**: Extrai região de cada placa
6. **OCR**: Google Vision processa texto das placas
7. **Regex**: Filtra e valida formato das placas
8. **Resposta**: Retorna placas encontradas e imagens processadas

### Formatos de Placa Suportados

- **Formato Antigo**: ABC1234 (3 letras + 4 números)
- **Formato Mercosul**: ABC1D23 (3 letras + 1 número + 1 letra + 2 números)


## 📝 Notas Importantes

- O sistema foi otimizado para placas brasileiras, mas pode ser adaptado para outros países
- A aplicação redimensiona a imagem resultado para 500x500 pixels por padrão

## 🔧 Troubleshooting

### Problemas Comuns

1. **Erro de credenciais Google**: Verifique se o arquivo `models/chave.json` está presente e válido
2. **Modelos não encontrados**: Certifique-se de que os arquivos `.pt` estão na pasta `models/`
3. **Erro de porta**: Verifique se a porta 5000 não está sendo usada por outro processo
4. **CORS**: O Flask-CORS está configurado para aceitar todas as origens em desenvolvimento

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**Desenvolvido com ❤️ para facilitar o reconhecimento automático de placas veiculares**
