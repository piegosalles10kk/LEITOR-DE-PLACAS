# 🚗 Sistema de Detecção e Reconhecimento de Placas Veiculares

Sistema inteligente de reconhecimento automático de placas veiculares (ALPR) que combina visão computacional com OCR para identificar e extrair informações de placas de veículos em imagens.

## 🎯 Sobre o Projeto

 É um sistema completo de ALPR (Automatic License Plate Recognition) desenvolvido em Python que utiliza modelos YOLO para detecção de objetos e Google Cloud Vision API para reconhecimento óptico de caracteres (OCR).

### O que o sistema faz?

1. **Detecta veículos** em uma imagem usando YOLOv8
2. **Localiza placas** em cada veículo detectado com um modelo YOLO especializado
3. **Extrai o texto** das placas usando Google Cloud Vision API
4. **Valida o formato** das placas brasileiras (antigo e Mercosul)
5. **Retorna resultados** com imagens anotadas e crops individuais

### Casos de Uso

- Sistemas de estacionamento automatizado
- Controle de acesso veicular
- Monitoramento de tráfego
- Gestão de frotas
- Segurança e vigilância

## ✨ Funcionalidades

### Detecção Inteligente
- ✅ Detecção de múltiplos veículos em uma única imagem
- ✅ Identificação precisa de placas em cada veículo
- ✅ Suporte para placas brasileiras (formato antigo e Mercosul)
- ✅ Validação automática com expressões regulares

### Processamento de Imagem
- ✅ Geração de bounding boxes coloridos (veículos em vermelho, placas em verde)
- ✅ Anotação automática com o texto da placa identificada
- ✅ Crops individuais em Base64 de veículos e placas
- ✅ Imagem resultado redimensionada para visualização

### Interface e Integração
- ✅ API RESTful para integração com outros sistemas
- ✅ Interface web HTML responsiva para testes
- ✅ Preview de imagem antes do envio
- ✅ Resultados detalhados por veículo
- ✅ CORS habilitado para chamadas cross-origin

## 🔍 Como Funciona

### Fluxo de Processamento

```
1. UPLOAD DA IMAGEM
   ↓
2. DETECÇÃO DE VEÍCULOS (YOLOv8 - modelo_carros)
   • Identifica todos os carros na imagem
   • Desenha retângulos vermelhos ao redor
   ↓
3. CROP DOS VEÍCULOS
   • Extrai a região de cada veículo detectado
   • Converte para Base64 para retorno
   ↓
4. DETECÇÃO DE PLACAS (YOLOv8 - modelo_placas)
   • Procura placas dentro de cada veículo
   • Utiliza apenas a primeira placa encontrada por veículo
   ↓
5. CROP DAS PLACAS
   • Extrai a região da placa identificada
   • Prepara para processamento OCR
   ↓
6. OCR COM GOOGLE VISION API
   • Envia imagem da placa para análise
   • Recebe texto detectado
   ↓
7. VALIDAÇÃO COM REGEX
   • Remove espaços e hífens
   • Aplica regex para formatos brasileiros
   • Valida: ABC1234 ou ABC1D23
   ↓
8. ANOTAÇÃO DA IMAGEM
   • Desenha retângulos verdes nas placas
   • Adiciona texto da placa acima do veículo
   ↓
9. RESPOSTA JSON
   • Retorna dados estruturados
   • Inclui crops em Base64
   • URL da imagem processada
```

### Algoritmo de Detecção

**Classe ObjectDetector:**
```python
- detectar_carros(imagem)
  • Executa modelo YOLO de carros
  • Retorna coordenadas (x1, y1, x2, y2)

- detectar_placas(crop_imagem)
  • Executa modelo YOLO de placas
  • Retorna coordenadas relativas ao crop
```

**Processamento de Texto:**
```python
- processar_texto_placa(texto)
  • Remove espaços e hífens
  • Aplica regex: [A-Z]{3}[0-9]{1}[A-Z]{1}[0-9]{2} (Mercosul)
  • Ou: [A-Z]{3}[0-9]{4} (Antigo)
  • Retorna primeira correspondência válida
```

**Google Vision Integration:**
```python
- enviar_para_google_vision(crop_placa)
  • Converte imagem para bytes
  • Chama text_detection()
  • Processa texto retornado
  • Aplica validação de formato
```

## 🛠 Tecnologias Utilizadas

### Backend
| Tecnologia | Versão | Finalidade |
|------------|--------|------------|
| **Python** | 3.9+ | Linguagem principal |
| **Flask** | Latest | Framework web |
| **OpenCV** | Latest | Processamento de imagem |
| **Ultralytics YOLO** | Latest | Detecção de objetos |
| **Google Cloud Vision** | Latest | OCR (reconhecimento de texto) |
| **NumPy** | Latest | Manipulação de arrays |
| **Flask-CORS** | Latest | Cross-Origin Resource Sharing |

### Frontend
- **HTML5/CSS3** - Interface responsiva
- **JavaScript (ES6+)** - Lógica do cliente
- **Fetch API** - Requisições assíncronas

### Modelos YOLO
- **yolov8_carros.pt** - Modelo treinado para detectar veículos
- **yolov8_placas.pt** - Modelo especializado em placas

## 📋 Pré-requisitos

### Software Necessário
- ✅ Python 3.9 ou superior
- ✅ pip (gerenciador de pacotes Python)
- ✅ Conta ativa no Google Cloud Platform
- ✅ Vision API habilitada no GCP

### Conhecimentos Recomendados
- Básico de Python
- Noções de APIs REST
- Conceitos de visão computacional (opcional)

## 🚀 Instalação

### Passo 1: Clone o Repositório

```bash
git clone https://github.com/piegosalles10kk/LEITOR-DE-PLACAS.git
cd LEITOR-DE-PLACAS
```

### Passo 2: Crie um Ambiente Virtual

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Passo 3: Instale as Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Dependências Instaladas:**
- certifi - Certificados SSL
- easyocr - OCR alternativo (não utilizado atualmente)
- Flask - Framework web
- flask_cors - Suporte a CORS
- opencv-python - Processamento de imagem
- numpy - Operações matemáticas
- Werkzeug - Utilitários web
- ultralytics - Framework YOLO
- PyYAML - Configurações
- requests - Requisições HTTP
- google-cloud-vision - API de OCR do Google

### Passo 4: Verifique a Estrutura de Pastas

```bash
LEITOR-DE-PLACAS/
├── models/               # ✅ Modelos já incluídos
│   ├── yolov8_carros.pt # ✅ Já presente
│   └── yolov8_placas.pt # ✅ Já presente
└── uploads/             # Criado automaticamente
```

A pasta `models/` com os modelos YOLO já está incluída no projeto. Apenas a chave da Google Cloud Vision API precisa ser configurada.

## ⚙️ Configuração

### Google Cloud Vision API (OBRIGATÓRIO)

A aplicação requer credenciais válidas da Google Cloud Vision API para funcionar.

#### Passo 1: Crie um Projeto no Google Cloud

1. Acesse [Google Cloud Console](https://console.cloud.google.com)
2. Clique em **Criar Projeto**
3. Dê um nome ao projeto (ex: "locar-vision-api")
4. Anote o **ID do Projeto**

#### Passo 2: Habilite a Vision API

1. No menu lateral, vá em **APIs e Serviços** > **Biblioteca**
2. Pesquise por "Cloud Vision API"
3. Clique em **ATIVAR**
4. Aguarde a habilitação (pode levar alguns segundos)

#### Passo 3: Crie uma Conta de Serviço

1. Vá em **APIs e Serviços** > **Credenciais**
2. Clique em **Criar Credenciais** > **Conta de serviço**
3. Preencha:
   - **Nome:** locar-vision-service
   - **ID:** (gerado automaticamente)
   - **Descrição:** Conta para Locar Vision OCR
4. Clique em **Criar e Continuar**
5. Em **Papel**, selecione: **Proprietário** ou **Editor**
6. Clique em **Concluir**

#### Passo 4: Gere e Baixe a Chave JSON

1. Na lista de contas de serviço, clique na conta criada
2. Vá na aba **Chaves**
3. Clique em **Adicionar Chave** > **Criar nova chave**
4. Selecione **JSON**
5. Clique em **Criar**
6. O arquivo será baixado automaticamente

#### Passo 5: Configure a Chave no Projeto

1. **Renomeie** o arquivo baixado para `chave.json`
2. **Mova** o arquivo para a pasta `models/`:

```bash
# Linux/Mac
mv ~/Downloads/nome-do-arquivo-baixado.json models/chave.json

# Windows (PowerShell)
Move-Item "$env:USERPROFILE\Downloads\nome-do-arquivo-baixado.json" "models\chave.json"
```

3. **Verifique** se o arquivo está no local correto:

```bash
# Deve listar: models/chave.json
ls models/chave.json
```

**⚠️ IMPORTANTE:** O arquivo `chave.json` contém credenciais sensíveis. Nunca compartilhe ou commite este arquivo em repositórios públicos!

#### Estrutura Esperada da Chave JSON

```json
{
  "type": "service_account",
  "project_id": "seu-projeto-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "locar-vision-service@seu-projeto.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  ...
}
```

### Verificação da Configuração

Execute este script Python para testar a conexão:

```python
from google.cloud import vision
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "models/chave.json"

try:
    client = vision.ImageAnnotatorClient()
    print("✅ Google Cloud Vision API configurada corretamente!")
except Exception as e:
    print(f"❌ Erro na configuração: {e}")
```

## 📖 Uso

### Execução Local

#### 1. Inicie o Servidor Flask

```bash
python lerPlaca.py
```

Você verá:
```
 * Serving Flask app 'lerPlaca'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

#### 2. Acesse a Interface Web

Abra seu navegador e acesse:
```
http://localhost:5000
```

#### 3. Teste o Sistema

1. **Selecione uma imagem** com veículos visíveis
2. **Visualize o preview** da imagem selecionada
3. Clique em **Enviar e Processar Imagem**
4. Aguarde o processamento (pode levar alguns segundos)
5. **Veja os resultados**:
   - Número de veículos detectados
   - Placas identificadas
   - Crops individuais de veículos e placas

### Usando a API Diretamente

#### cURL
```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@/caminho/para/imagem.jpg"
```

#### Python
```python
import requests

url = "http://localhost:5000/upload"
files = {'file': open('imagem.jpg', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

#### JavaScript (Fetch)
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:5000/upload', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

### Interface Web (index.html)

A interface web oferece:

**Funcionalidades:**
- 📤 Upload de arquivo com drag-and-drop
- 👁️ Preview da imagem antes do envio
- 🔄 Indicador de progresso durante processamento
- 📊 Resultados detalhados por veículo
- 🖼️ Visualização de crops em Base64
- ⚠️ Tratamento de erros com mensagens claras

**Configuração:**
O arquivo `index.html` possui URLs fixas para o backend:
```javascript
const apiUrl = "https://lively-giving-crayfish.ngrok-free.app/upload";
const baseUrlFlask = "https://lively-giving-crayfish.ngrok-free.app";
```

**Para uso local, altere para:**
```javascript
const apiUrl = "http://localhost:5000/upload";
const baseUrlFlask = "http://localhost:5000";
```

## 🔌 API

### Endpoints Disponíveis

#### GET `/`
Serve a interface web HTML.

**Resposta:**
- Status: 200 OK
- Content-Type: text/html
- Body: Arquivo index.html

---

#### POST `/upload`

Processa uma imagem e retorna veículos e placas detectadas.

**Request:**
- **Method:** POST
- **Content-Type:** multipart/form-data
- **Body:**
  - `file`: Arquivo de imagem (JPEG, PNG, etc.)

**Response (Sucesso):**
```json
{
  "numero_veiculos": 2,
  "veiculos": [
    {
      "placa": "ABC1234",
      "crop_carro_base64": "/9j/4AAQSkZJRgABAQEAYABgAAD...",
      "crop_placa_base64": "iVBORw0KGgoAAAANSUhEUgAA..."
    },
    {
      "placa": "XYZ5D67",
      "crop_carro_base64": "R0lGODlhAQABAIAAAP///wAAACH5BA...",
      "crop_placa_base64": "PHN2ZyB3aWR0aD0iMTAwIiBoZWln..."
    }
  ],
  "placas": ["ABC1234", "XYZ5D67"],
  "imagem_resultado": "uploads/resultado_imagem_atual.jpg"
}
```

**Campos da Resposta:**
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `numero_veiculos` | integer | Total de veículos com placas identificadas |
| `veiculos` | array | Lista de objetos com dados de cada veículo |
| `veiculos[].placa` | string | Texto da placa (formato brasileiro) |
| `veiculos[].crop_carro_base64` | string | Imagem do veículo em Base64 |
| `veiculos[].crop_placa_base64` | string | Imagem da placa em Base64 |
| `placas` | array | Lista simplificada apenas com os textos |
| `imagem_resultado` | string | Caminho relativo da imagem anotada |

**Response (Sem Detecção):**
```json
{
  "numero_veiculos": 0,
  "veiculos": [],
  "placas": [],
  "imagem_resultado": "uploads/resultado_imagem_atual.jpg"
}
```

**Response (Erro):**
```json
{
  "error": "No file part"
}
```

**Status Codes:**
- `200 OK` - Processamento bem-sucedido
- `400 Bad Request` - Arquivo não enviado ou inválido
- `500 Internal Server Error` - Erro no processamento

### Formatos de Placa Suportados

**Formato Antigo:**
- Padrão: `ABC1234`
- Regex: `[A-Z]{3}[0-9]{4}`
- Exemplo: `RAB2022`, `JKL4567`

**Formato Mercosul:**
- Padrão: `ABC1D23`
- Regex: `[A-Z]{3}[0-9]{1}[A-Z]{1}[0-9]{2}`
- Exemplo: `BRA2E19`, `FGH3K45`

### Exemplos de Uso

#### Python com requests
```python
import requests
import json

def detectar_placas(imagem_path):
    url = "http://localhost:5000/upload"
    
    with open(imagem_path, 'rb') as img:
        files = {'file': img}
        response = requests.post(url, files=files)
    
    if response.status_code == 200:
        dados = response.json()
        print(f"Veículos detectados: {dados['numero_veiculos']}")
        for veiculo in dados['veiculos']:
            print(f"  Placa: {veiculo['placa']}")
    else:
        print(f"Erro: {response.text}")

detectar_placas("carro.jpg")
```

#### Node.js com axios
```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

async function detectarPlacas(imagemPath) {
    const form = new FormData();
    form.append('file', fs.createReadStream(imagemPath));
    
    try {
        const response = await axios.post('http://localhost:5000/upload', form, {
            headers: form.getHeaders()
        });
        
        console.log(`Veículos: ${response.data.numero_veiculos}`);
        response.data.placas.forEach(placa => {
            console.log(`  Placa: ${placa}`);
        });
    } catch (error) {
        console.error('Erro:', error.message);
    }
}

detectarPlacas('carro.jpg');
```

## 📁 Estrutura do Projeto

```
LEITOR-DE-PLACAS/
│
├── lerPlaca.py              # 🐍 Aplicação Flask principal
│   ├── Classe ObjectDetector
│   ├── Funções de processamento
│   ├── Rotas da API
│   └── Servidor Flask
│
├── index.html               # 🌐 Interface web responsiva
│   ├── Preview de imagem
│   ├── Upload com Fetch API
│   └── Exibição de resultados
│
├── requirements.txt         # 📦 Dependências Python
│   └── 11 pacotes necessários
│
├── models/                  # 🤖 Modelos e credenciais
│   ├── yolov8_carros.pt    # ✅ Modelo YOLO (incluído)
│   ├── yolov8_placas.pt    # ✅ Modelo YOLO (incluído)
│   └── chave.json          # ⚠️ Criar manualmente (GCP)
│
├── uploads/                 # 📂 Arquivos temporários (auto-criado)
│   ├── imagem_atual.jpg    # Última imagem enviada
│   └── resultado_imagem_atual.jpg  # Imagem processada
│
├── README.md                # 📖 Documentação original
├── lerplaca.js              # (Não utilizado - versão Node.js)
├── teste.php                # (Não utilizado - arquivo vazio)
├── dockerfile               # 🐳 Configuração Docker
├── fly.toml                 # ✈️ Deploy Fly.io
└── package.json             # (Não utilizado - config Node.js)
```

### Arquivos Principais

**lerPlaca.py** (395 linhas)
- Inicialização dos modelos YOLO
- Classe `ObjectDetector` com métodos de detecção
- Funções auxiliares de processamento
- Integração com Google Vision API
- Rotas Flask (`/` e `/upload`)
- Servidor configurado para `0.0.0.0:5000`

**index.html** (240 linhas)
- Interface HTML5 moderna
- Estilos CSS3 inline
- JavaScript com Fetch API
- Preview de imagem dinâmico
- Tratamento de erros robusto
- Exibição de resultados estruturada

## 🔧 Troubleshooting

### Problema: Erro "No module named 'flask'"

**Causa:** Dependências não instaladas ou ambiente virtual não ativado.

**Solução:**
```bash
# Ative o ambiente virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstale as dependências
pip install -r requirements.txt
```

---

### Problema: "google.auth.exceptions.DefaultCredentialsError"

**Causa:** Arquivo `chave.json` ausente ou caminho incorreto.

**Solução:**
```bash
# Verifique se o arquivo existe
ls models/chave.json

# Se não existir, baixe novamente do Google Cloud Console
# e mova para models/chave.json
```

**Verificação do caminho no código:**
```python
# Em lerPlaca.py, linha 12
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "models/chave.json"
```

---

### Problema: "FileNotFoundError: yolov8_carros.pt"

**Causa:** Modelos YOLO ausentes na pasta `models/`.

**Solução:**
Os modelos já devem estar incluídos no projeto. Se não estiverem:
```bash
# Verifique se existem
ls models/yolov8_carros.pt
ls models/yolov8_placas.pt

# Se ausentes, contate o mantenedor do repositório
```

---

### Problema: Porta 5000 já está em uso

**Causa:** Outro processo usando a porta 5000.

**Solução:**
```bash
# Linux/Mac - Encontre e mate o processo
lsof -ti:5000 | xargs kill -9

# Windows - Encontre o PID
netstat -ano | findstr :5000
# Mate o processo pelo PID
taskkill /PID <número_do_pid> /F

# Ou altere a porta no código (lerPlaca.py, última linha)
app.run(host='0.0.0.0', port=8080, debug=True)
```

---

### Problema: CORS bloqueando requisições

**Causa:** Frontend em domínio diferente do backend.

**Solução:**
O Flask-CORS já está habilitado. Se o problema persistir:
```python
# Em lerPlaca.py, linha 19, modifique para:
CORS(app, resources={r"/*": {"origins": "*"}})
```

---

### Problema: Placas não são detectadas

**Possíveis Causas:**
1. Imagem de baixa qualidade
2. Placa muito pequena ou cortada
3. Ângulo desfavorável
4. Iluminação inadequada

**Soluções:**
- Use imagens com resolução mínima de 800x600
- Certifique-se de que a placa está visível
- Evite fotos com reflexos intensos
- Teste com diferentes imagens para validar

---

### Problema: OCR retorna texto errado

**Causa:** Google Vision API pode interpretar caracteres similares incorretamente (0/O, 1/I, 5/S).

**Solução:**
O código já aplica regex para validar formatos brasileiros. Se o problema persistir:
```python
# Adicione tratamentos customizados em processar_texto_placa()
def processar_texto_placa(texto_detectado):
    texto_limpo = texto_detectado.replace(" ", "").replace("-", "")
    
    # Correções comuns
    texto_limpo = texto_limpo.replace("O", "0")
    texto_limpo = texto_limpo.replace("I", "1")
    
    padrao_placa = re.compile(r'([A-Za-z]{3}[0-9]{1}[A-Za-z]{1}[0-9]{2}|[A-Za-z]{3}[0-9]{4})')
    correspondencia = padrao_placa.search(texto_limpo)
    if correspondencia:
        return correspondencia.group(0)
    return None
```

---

### Problema: Imagem resultado não carrega no navegador

**Causa:** Caminho de URL incorreto (barras invertidas no Windows).

**Solução:**
O código JavaScript já corrige isso:
```javascript
// Em index.html, linha 132
imagePath = imagePath.replace(/\\/g, '/');
```

Se o problema persistir, verifique permissões da pasta `uploads/`.

---

### Problema: "Address already in use" ao iniciar

**Causa:** Servidor Flask ainda rodando em segundo plano.

**Solução:**
```bash
# Linux/Mac
pkill -f lerPlaca.py

# Windows
taskkill /F /IM python.exe
```



## 📞 Suporte

### Recursos
- 📖 [Documentação Google Cloud Vision](https://cloud.google.com/vision/docs)
- 🤖 [Ultralytics YOLO Docs](https://docs.ultralytics.com/)
- 🌐 [Flask Documentation](https://flask.palletsprojects.com/)

### Problemas e Dúvidas
- 🐛 Reporte bugs via [GitHub Issues](https://github.com/piegosalles10kk/LEITOR-DE-PLACAS/issues)
- 💬 Discussões no repositório

---

**Desenvolvido com ❤️ para facilitar o reconhecimento automático de placas veiculares**

*Última atualização: Outubro 2025*
