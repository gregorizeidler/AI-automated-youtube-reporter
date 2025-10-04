# ⚡ Quick Start - 3 Modos de Operação

## 🎯 **Escolha Seu Modo:**

### **Modo 1: Apenas Roteiros** (Mais Simples)
```bash
# .env
VIDEO_MODE=script_only
```
→ **Gera apenas roteiros, você grava os vídeos**

### **Modo 2: Vídeo com Voz IA** (Melhor Qualidade)
```bash
# .env  
VIDEO_MODE=ai_voice
ELEVENLABS_API_KEY=sua_chave
```
→ **Cria vídeo completo com voz profissional**

### **Modo 3: Avatar Virtual** (Mais Profissional)
```bash
# .env
VIDEO_MODE=avatar
DID_API_KEY=sua_chave
```
→ **Apresentador virtual narrando as notícias**

### **Modo 4: Slideshow Grátis** (Mais Barato)
```bash
# .env
VIDEO_MODE=slideshow
```
→ **Slides + voz gratuita (quase de graça!)**

---

## 🚀 **Como Usar:**

### 1. Configure
```bash
cp env.example .env
# Edite .env com suas chaves de API
```

### 2. Instale
```bash
pip install -r requirements.txt
```

### 3. Execute
```bash
# Uma vez
python main.py --once

# Contínuo (a cada X horas)
python main.py
```

---

## 💰 **Custos:**

| Modo | Custo/Vídeo | Tempo | Qualidade |
|------|-------------|-------|-----------|
| Script Only | $0.03 | 2 min | - |
| AI Voice | $0.13-0.33 | 8 min | ⭐⭐⭐⭐ |
| Avatar | $0.23-0.53 | 5 min | ⭐⭐⭐⭐⭐ |
| Slideshow | $0.03 | 4 min | ⭐⭐ |

---

## 🎬 **O Que Acontece:**

```
1. Sistema busca notícias no Google
2. IA escreve roteiro profissional  
3. [Opcional] Gera vídeo automaticamente
4. [Opcional] Faz upload pro YouTube
5. Pronto! 🎉
```

---

**Veja SETUP_GUIDE.md para instruções detalhadas de cada modo!**

