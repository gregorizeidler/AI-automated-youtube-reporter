# 🎉 New Features Guide

Este guia explica as novas funcionalidades adicionadas ao Automated YouTube Reporter.

---

## 📊 **1. Sistema de Database SQLite**

### O que faz?
- Armazena histórico de artigos coletados
- Rastreia scripts gerados e vídeos publicados
- Evita duplicação de conteúdo
- Permite análise de performance

### Como usar:

```python
from database import get_database

# Obter estatísticas
db = get_database()
stats = db.get_statistics(days=30)
print(f"Scripts gerados: {stats['total_scripts']}")
print(f"Vídeos publicados: {stats['videos_uploaded']}")

# Ver tópicos recentes (evitar duplicatas)
recent_topics = db.get_recent_topics('sports', days=7)
```

### Arquivos:
- `reporter.db` - Database SQLite criado automaticamente
- Queries são registradas automaticamente durante a execução

---

## 🌍 **2. Suporte Multi-idiomas**

### Idiomas Suportados:
- 🇺🇸 English (en)
- 🇧🇷 Português (pt)
- 🇪🇸 Español (es)
- 🇫🇷 Français (fr)
- 🇩🇪 Deutsch (de)
- 🇮🇹 Italiano (it)
- 🇯🇵 日本語 (ja)
- 🇰🇷 한국어 (ko)
- 🇨🇳 中文 (zh)

### Configuração no .env:

```bash
# Para português brasileiro
TARGET_LANGUAGE=pt
LANGUAGE_VARIANT=0  # 0=pt-BR, 1=pt-PT

# Para espanhol da Espanha
TARGET_LANGUAGE=es
LANGUAGE_VARIANT=0  # 0=es-ES, 1=es-MX, 2=es-AR
```

### Recursos:
- Scripts gerados no idioma escolhido
- Vozes TTS automaticamente selecionadas
- Metadados traduzidos (título, descrição)
- Estilos de narração adaptados por idioma

---

## 📰 **3. Múltiplas Fontes de Notícias**

### Fontes Disponíveis:

#### **NewsAPI** (Recomendado)
- API profissional de notícias
- 100 requisições/dia grátis
- Cadastre-se em: https://newsapi.org

```bash
NEWSAPI_KEY=your-key-here
USE_NEWSAPI=true
```

#### **RSS Feeds**
- Feeds de CNN, BBC, ESPN, etc.
- Grátis, sem necessidade de API key
- Configurado automaticamente

```bash
USE_RSS_FEEDS=true
```

#### **Reddit**
- Posts trending de subreddits relevantes
- Ótimo para tópicos virais
- Sem necessidade de API key

```bash
USE_REDDIT=true
```

#### **Google Search** (Padrão)
- Busca tradicional do Google
- Gratuito

```bash
USE_GOOGLE_SEARCH=true
```

### Como funciona:
```python
from news_sources import EnhancedNewsCollector

collector = EnhancedNewsCollector()
articles = collector.collect_from_all_sources(
    category='sports',
    language='pt',
    use_newsapi=True,
    use_rss=True,
    use_reddit=False
)
```

---

## 📅 **4. Agendamento Inteligente**

### O que faz?
- Agenda publicações nos horários de pico
- Respeita intervalo mínimo entre posts
- Adapta por categoria (esportes à noite, finanças pela manhã)
- Considera dias da semana ideais

### Horários Otimizados por Categoria:

| Categoria | Melhores Horários | Melhores Dias |
|-----------|-------------------|---------------|
| **Sports** | 18:00, 20:00, 12:00 | Fim de semana |
| **Politics** | 07:00, 12:00, 18:00 | Dias úteis |
| **Finance** | 08:00, 12:00, 16:00 | Dias úteis |
| **Technology** | 10:00, 14:00, 21:00 | Dias úteis |

### Configuração:

```bash
USE_INTELLIGENT_SCHEDULING=true
TIMEZONE_OFFSET=-3  # Brasil (UTC-3)
MIN_HOURS_BETWEEN_POSTS=4
```

### Uso:

```python
from scheduler import IntelligentScheduler

scheduler = IntelligentScheduler()

# Agendar vídeo
scheduled_time = scheduler.schedule_video(
    video_id=123,
    category='sports',
    title='Breaking Sports News'
)

# Ver agenda dos próximos 7 dias
scheduler.print_schedule(days=7)

# Publicar vídeos na hora certa
due_videos = scheduler.get_due_videos()
```

---

## 🎙️ **5. Personalização de Voz por Categoria**

### O que faz?
- Seleciona automaticamente a voz ideal para cada categoria
- Ajusta tom, energia e estilo
- Suporta múltiplos idiomas

### Vozes por Categoria (Inglês):

| Categoria | Voz | Estilo |
|-----------|-----|--------|
| **Sports** | Adam (M) | Energético |
| **Politics** | Rachel (F) | Autoritativo |
| **Finance** | Arnold (M) | Profissional |
| **Technology** | Antoni (M) | Casual |
| **Entertainment** | Elli (F) | Amigável |

### Configuração:

```bash
# Auto-seleção (recomendado)
AUTO_SELECT_VOICE=true

# Ou fixar uma voz para tudo
AUTO_SELECT_VOICE=false
VOICE_OVERRIDE=21m00Tcm4TlvDq8ikWAM
```

### Uso Programático:

```python
from voice_manager import VoiceManager

# Obter voz para categoria
voice = VoiceManager.get_voice_for_category('sports', language='pt')
print(f"Voz: {voice.name}, Estilo: {voice.style}")

# Configurações de qualidade
settings = VoiceManager.get_voice_settings('sports')
print(f"Estabilidade: {settings['stability']}")
```

---

## 🎨 **6. Geração Automática de Thumbnails**

### Modos Disponíveis:

#### **1. Template** (Padrão - Grátis)
```bash
THUMBNAIL_MODE=template
```
- Gera thumbnail com texto e cores por categoria
- Totalmente grátis
- Rápido

#### **2. AI (DALL-E 3)**
```bash
THUMBNAIL_MODE=ai
```
- Usa DALL-E 3 para gerar imagens únicas
- Custo: ~$0.04 por thumbnail
- Qualidade profissional
- Requer OpenAI API

#### **3. Stock Images**
```bash
THUMBNAIL_MODE=stock
PEXELS_API_KEY=your-key
# ou
UNSPLASH_ACCESS_KEY=your-key
```
- Busca imagens relevantes em bancos de imagens
- Grátis com Pexels/Unsplash API
- Boa qualidade

### Configuração:

```bash
AUTO_GENERATE_THUMBNAILS=true
THUMBNAIL_MODE=template
```

### Uso:

```python
from thumbnail_generator import ThumbnailGenerator

generator = ThumbnailGenerator()

# Template
thumbnail_path = generator.generate_template_thumbnail(
    title='Breaking Sports News',
    category='sports',
    thumbnail_text='ÚLTIMA HORA'
)

# AI (DALL-E)
thumbnail_path = generator.generate_ai_thumbnail(
    prompt='exciting sports championship',
    title='Championship Finals'
)

# Stock image
thumbnail_path = generator.download_stock_image(
    query='football stadium',
    title='Big Game Tonight'
)
```

---

## 📝 **8. Legendas Automáticas (SRT)**

### Modos de Geração:

#### **1. Script-based** (Padrão - Grátis)
```bash
SUBTITLE_METHOD=script
```
- Gera legendas baseadas no script
- Timing estimado (150 palavras/min)
- Instantâneo e grátis

#### **2. Whisper** (Mais Preciso)
```bash
SUBTITLE_METHOD=whisper
```
- Transcreve o áudio real
- Timing perfeito
- Requer instalação do Whisper

### Múltiplos Idiomas:

```bash
SUBTITLE_LANGUAGES=en,pt,es
```
- Gera legendas em múltiplos idiomas
- Tradução automática via GPT
- Um arquivo .srt por idioma

### Configuração:

```bash
AUTO_GENERATE_SUBTITLES=true
SUBTITLE_METHOD=script
SUBTITLE_LANGUAGES=en
```

### Instalação do Whisper (Opcional):

```bash
pip install openai-whisper
# Whisper requer FFmpeg instalado
```

### Uso:

```python
from subtitle_generator import SubtitleGenerator

generator = SubtitleGenerator()

# Gerar do script
srt_path = generator.generate_srt_from_script(
    script_text='Full video script here...',
    title='My Video',
    words_per_minute=150
)

# Gerar do áudio (Whisper)
srt_path = generator.generate_srt_from_audio(
    audio_file='video_audio.mp3',
    title='My Video',
    language='pt'
)

# Traduzir legendas
pt_srt = generator.translate_subtitles(
    srt_file='video.srt',
    target_language='pt'
)

# Converter para WebVTT
vtt_path = generator.generate_vtt_from_srt('video.srt')
```

---

## 🚀 **Workflow Completo com Novas Features**

### Exemplo: Canal de Notícias em Português

```bash
# .env configuration
TARGET_LANGUAGE=pt
LANGUAGE_VARIANT=0

# Múltiplas fontes
USE_NEWSAPI=true
USE_RSS_FEEDS=true
USE_REDDIT=false

# Voice personalizada
AUTO_SELECT_VOICE=true

# Thumbnails automáticas
AUTO_GENERATE_THUMBNAILS=true
THUMBNAIL_MODE=template

# Legendas em PT e EN
AUTO_GENERATE_SUBTITLES=true
SUBTITLE_METHOD=script
SUBTITLE_LANGUAGES=pt,en

# Agendamento inteligente
USE_INTELLIGENT_SCHEDULING=true
TIMEZONE_OFFSET=-3
MIN_HOURS_BETWEEN_POSTS=4

# Modo de vídeo
VIDEO_MODE=ai_voice
ELEVENLABS_API_KEY=your-key
```

### Executar:

```bash
python main.py --once
```

### O que acontece:

1. ✅ Coleta notícias de NewsAPI + RSS + Google
2. ✅ Verifica no database se não é duplicado
3. ✅ Gera script em português
4. ✅ Seleciona voz ideal para categoria
5. ✅ Gera vídeo com AI voice
6. ✅ Cria thumbnail automaticamente
7. ✅ Gera legendas .srt em PT e EN
8. ✅ Agenda publicação no horário ideal
9. ✅ Salva tudo no database
10. ✅ Upload agendado para YouTube

---

## 📊 **Comandos Úteis**

### Ver estatísticas:

```python
from database import get_database

db = get_database()
stats = db.get_statistics(days=30)
print(stats)
```

### Ver agenda:

```python
from scheduler import IntelligentScheduler

scheduler = IntelligentScheduler()
scheduler.print_schedule(days=7)
```

### Listar vozes disponíveis:

```python
from voice_manager import VoiceManager

voices = VoiceManager.list_available_voices('pt')
for category, voice in voices.items():
    print(f"{category}: {voice.name} ({voice.style})")
```

---

## 💰 **Custos Estimados**

### Modo Econômico (Script + Template):
- **$0.03** por vídeo
- Scripts: $0.03
- Thumbnails: Grátis
- Legendas: Grátis

### Modo Intermediário (AI Voice + Template):
- **$0.13-0.33** por vídeo
- Scripts: $0.03
- Voice: $0.10-0.30
- Thumbnails: Grátis
- Legendas: Grátis

### Modo Premium (AI Voice + AI Thumbnail):
- **$0.17-0.37** por vídeo
- Scripts: $0.03
- Voice: $0.10-0.30
- Thumbnails: $0.04
- Legendas: Grátis

### Modo Ultra (Avatar + AI Thumbnail + Multi-lang Subs):
- **$0.27-0.57** por vídeo
- Scripts: $0.03
- Avatar: $0.20-0.50
- Thumbnails: $0.04
- Legendas múltiplas: $0.00-0.05

---

## 🔧 **Troubleshooting**

### Database está crescendo muito:
```python
# Limpar artigos antigos não usados
from database import get_database
db = get_database()
# Implementar sua própria lógica de limpeza
```

### Whisper muito lento:
```bash
# Use modelo menor
# No código: model = whisper.load_model("tiny")  # ou "base"
```

### Thumbnails não ficando boas:
```bash
# Tente AI mode
THUMBNAIL_MODE=ai
```

### Agendamento não funcionando:
```bash
# Verifique timezone
TIMEZONE_OFFSET=-3  # Ajuste para seu fuso
```

---

## 📚 **Próximos Passos**

1. Configure seu `.env` com as novas opções
2. Instale dependências: `pip install -r requirements.txt`
3. Execute teste: `python main.py --once`
4. Verifique pasta `reporter.db`, `thumbnails/`, `subtitles/`
5. Ajuste configurações conforme necessário

---

## 💡 **Dicas Pro**

1. **Use NewsAPI** para notícias de qualidade
2. **Template thumbnails** são suficientes para começar
3. **Script-based subtitles** funcionam muito bem
4. **Database tracking** evita conteúdo duplicado
5. **Agendamento inteligente** maximiza views
6. **Multi-idiomas** abre novos mercados

---

**Divirta-se criando conteúdo automatizado em escala! 🚀**

