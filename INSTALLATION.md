# 🚀 Installation Guide - New Features

Este guia mostra como instalar e configurar todas as novas funcionalidades.

---

## 📦 **Instalação Básica**

### 1. Atualizar Dependências

```bash
cd /Users/gregorizeidler/medium

# Instalar/atualizar todas as dependências
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp env.example .env

# Editar .env com suas configurações
nano .env  # ou use seu editor preferido
```

---

## 🔧 **Configuração por Funcionalidade**

### ✅ **1. Database SQLite** (Nenhuma configuração necessária)

- Criado automaticamente na primeira execução
- Arquivo `reporter.db` será gerado
- Sem necessidade de setup adicional

**Pronto para usar!** ✓

---

### ✅ **2. Multi-idiomas**

**Configuração mínima (.env):**

```bash
TARGET_LANGUAGE=pt  # ou en, es, fr, de, etc.
LANGUAGE_VARIANT=0   # Variante do idioma
```

**Idiomas disponíveis:**
- `en` - English
- `pt` - Português (0=BR, 1=PT)
- `es` - Español (0=ES, 1=MX, 2=AR)
- `fr` - Français
- `de` - Deutsch
- `it` - Italiano
- `ja` - 日本語
- `ko` - 한국어
- `zh` - 中文

**Pronto para usar!** ✓

---

### ⚙️ **3. NewsAPI** (Recomendado)

**1. Obter API Key:**

1. Acesse: https://newsapi.org
2. Clique em "Get API Key"
3. Cadastre-se (grátis - 100 requests/dia)
4. Copie sua API key

**2. Configurar (.env):**

```bash
NEWSAPI_KEY=sua-api-key-aqui
USE_NEWSAPI=true
```

**Testar:**

```bash
python -c "from news_sources import NewsAPICollector; c = NewsAPICollector(); print('✓ NewsAPI configurada!' if c.api_key else '✗ API key não encontrada')"
```

---

### ⚙️ **4. RSS Feeds** (Nenhuma configuração necessária)

**Configurar (.env):**

```bash
USE_RSS_FEEDS=true
```

**Fontes incluídas:**
- CNN, BBC, ESPN, Yahoo, TechCrunch, etc.

**Pronto para usar!** ✓

---

### ⚙️ **5. Reddit** (Opcional)

**Configurar (.env):**

```bash
USE_REDDIT=true  # ou false para desabilitar
```

**Subreddits incluídos:**
- r/sports, r/worldnews, r/technology, r/investing, etc.

**Pronto para usar!** ✓

---

### ⚙️ **6. Agendamento Inteligente**

**Configurar (.env):**

```bash
USE_INTELLIGENT_SCHEDULING=true
TIMEZONE_OFFSET=-3  # Seu fuso horário (Brasil = -3)
MIN_HOURS_BETWEEN_POSTS=4
```

**Fusos horários comuns:**
- Brasil: `-3`
- EUA (EST): `-5`
- EUA (PST): `-8`
- Europa (CET): `+1`
- Japão: `+9`

**Pronto para usar!** ✓

---

### ⚙️ **7. Personalização de Voz**

**Para ElevenLabs (AI Voice):**

```bash
AUTO_SELECT_VOICE=true
# Voz será escolhida automaticamente por categoria

# Ou fixar uma voz:
AUTO_SELECT_VOICE=false
VOICE_OVERRIDE=21m00Tcm4TlvDq8ikWAM
```

**Vozes disponíveis:**
- Ver em: https://elevenlabs.io/voice-library
- Lista completa em `voice_manager.py`

**Para Free TTS (gTTS/edge-tts):**

```bash
# Voz selecionada automaticamente por idioma
# Nenhuma configuração adicional necessária
```

**Pronto para usar!** ✓

---

### ⚙️ **8. Geração de Thumbnails**

#### **Opção A: Template** (Grátis - Recomendado para começar)

```bash
AUTO_GENERATE_THUMBNAILS=true
THUMBNAIL_MODE=template
```

**Pronto para usar!** ✓

---

#### **Opção B: AI (DALL-E 3)**

**1. Usar sua OpenAI API key existente**

```bash
THUMBNAIL_MODE=ai
# OPENAI_API_KEY já configurada
```

**Custo:** ~$0.04 por thumbnail

**Pronto para usar!** ✓

---

#### **Opção C: Stock Images**

**Para Pexels:**

1. Acesse: https://www.pexels.com/api/
2. Cadastre-se (grátis)
3. Gere API key

```bash
THUMBNAIL_MODE=stock
PEXELS_API_KEY=sua-api-key-aqui
```

**Para Unsplash:**

1. Acesse: https://unsplash.com/developers
2. Cadastre-se (grátis)
3. Crie aplicação e copie Access Key

```bash
THUMBNAIL_MODE=stock
UNSPLASH_ACCESS_KEY=sua-access-key-aqui
```

---

### ⚙️ **9. Legendas Automáticas**

#### **Opção A: Script-based** (Padrão - Grátis)

```bash
AUTO_GENERATE_SUBTITLES=true
SUBTITLE_METHOD=script
SUBTITLE_LANGUAGES=en  # ou pt, es, etc.
```

**Pronto para usar!** ✓

---

#### **Opção B: Whisper** (Mais preciso)

**1. Instalar Whisper:**

```bash
pip install openai-whisper
```

**2. Verificar FFmpeg:**

```bash
# Mac
brew install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt-get install ffmpeg

# Windows
# Baixe de: https://ffmpeg.org/download.html
```

**3. Configurar:**

```bash
SUBTITLE_METHOD=whisper
```

**Testar:**

```bash
python -c "import whisper; print('✓ Whisper instalado!')"
```

---

### ⚙️ **10. Múltiplas Legendas (Tradução)**

**Gerar legendas em vários idiomas:**

```bash
SUBTITLE_LANGUAGES=en,pt,es,fr
```

**Requer:** OpenAI API key (para tradução)

**Custo:** ~$0.01 por idioma adicional

**Pronto para usar!** ✓

---

## 🧪 **Testar Instalação**

### Teste Rápido:

```bash
# Executar exemplos
python example_usage.py
```

### Teste Completo:

```bash
# Executar um ciclo completo
python main.py --once
```

### Verificar cada componente:

```python
# Database
python -c "from database import get_database; db = get_database(); print('✓ Database OK')"

# Multi-lang
python -c "from multilang import LanguageManager; print('✓ Multi-lang OK')"

# News sources
python -c "from news_sources import EnhancedNewsCollector; print('✓ News sources OK')"

# Scheduler
python -c "from scheduler import IntelligentScheduler; print('✓ Scheduler OK')"

# Voice
python -c "from voice_manager import VoiceManager; print('✓ Voice manager OK')"

# Thumbnails
python -c "from thumbnail_generator import ThumbnailGenerator; print('✓ Thumbnails OK')"

# Subtitles
python -c "from subtitle_generator import SubtitleGenerator; print('✓ Subtitles OK')"
```

---

## 📁 **Estrutura de Arquivos Criados**

Após a primeira execução, estes arquivos/pastas serão criados:

```
medium/
├── reporter.db              # SQLite database
├── thumbnails/              # Thumbnails geradas
├── subtitles/               # Arquivos .srt e .vtt
├── schedule.json            # Agendamento
├── youtube_scripts/         # Scripts salvos
├── generated_videos/        # Vídeos gerados
└── .env                     # Suas configurações
```

---

## 🔍 **Troubleshooting**

### Erro: "Module not found"

```bash
pip install -r requirements.txt
```

### Erro: "FFmpeg not found"

```bash
# Mac
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg
```

### Erro: "Database is locked"

```bash
# Feche outras instâncias do programa
pkill -f "python main.py"
```

### NewsAPI não retornando resultados

- Verifique se a API key está correta
- Limite gratuito: 100 requests/dia
- Verifique em: https://newsapi.org/account

### Whisper muito lento

- Use modelo menor: `tiny` ou `base`
- Edite `subtitle_generator.py`: `model = whisper.load_model("base")`

### Thumbnails com fonte padrão (feia)

- Normal! Fontes do sistema variam
- Template mode usa fontes disponíveis
- Para melhor qualidade, use `THUMBNAIL_MODE=ai`

---

## ✅ **Configuração Recomendada para Começar**

```bash
# Mínimo funcional (GRÁTIS)
TARGET_LANGUAGE=pt
VIDEO_MODE=script_only
THUMBNAIL_MODE=template
SUBTITLE_METHOD=script
USE_RSS_FEEDS=true
AUTO_SELECT_VOICE=true

# Adicione apenas o essencial:
OPENAI_API_KEY=sua-key
```

**Custo:** $0.03 por vídeo

---

## 🚀 **Configuração Recomendada para Produção**

```bash
# Automação completa
TARGET_LANGUAGE=pt
VIDEO_MODE=ai_voice
THUMBNAIL_MODE=template  # ou ai se quiser gastar mais
SUBTITLE_METHOD=script
SUBTITLE_LANGUAGES=pt,en

# APIs recomendadas:
OPENAI_API_KEY=sua-key
ELEVENLABS_API_KEY=sua-key
NEWSAPI_KEY=sua-key  # Muito recomendado

# Features
USE_NEWSAPI=true
USE_RSS_FEEDS=true
USE_INTELLIGENT_SCHEDULING=true
AUTO_SELECT_VOICE=true
AUTO_GENERATE_THUMBNAILS=true
AUTO_GENERATE_SUBTITLES=true
```

**Custo:** $0.13-0.33 por vídeo

---

## 📞 **Suporte**

- Documentação completa: `NEW_FEATURES.md`
- Exemplos de código: `example_usage.py`
- Guia rápido: `QUICK_START.md`

---

**Pronto! Você está preparado para criar conteúdo automatizado em escala! 🎉**

