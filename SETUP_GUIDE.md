# 🚀 Setup Guide - Choose Your Video Generation Mode

This guide helps you set up the system based on which video generation option you want to use.

---

## 📋 **Quick Start (Script Only)**

The simplest way to start - generate scripts without video creation:

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure
```bash
cp env.example .env
```

Edit `.env`:
```bash
OPENAI_API_KEY=sk-...  # Get from https://platform.openai.com/
VIDEO_MODE=script_only
```

### 3. Run
```bash
python main.py --once
```

**Result:** Scripts saved in `youtube_scripts/` folder ready for you to record!

---

## 🎙️ **Option 1: AI Voice + Images (ElevenLabs)**

Professional AI voice narration with stock images.

### Cost
- **~$0.10-0.30 per video**
- ElevenLabs: $5-22/month
- OpenAI: ~$0.03/script

### Setup

#### 1. Get ElevenLabs API Key
1. Go to [ElevenLabs.io](https://elevenlabs.io/)
2. Sign up and subscribe to a plan
3. Go to Profile → API Keys
4. Copy your API key

#### 2. Install FFmpeg
**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html)

#### 3. Configure
Edit `.env`:
```bash
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=your_elevenlabs_key
VIDEO_MODE=ai_voice
```

Optional - choose voice:
```bash
# Popular voices:
# 21m00Tcm4TlvDq8ikWAM - Rachel (female, calm)
# ErXwobaYiN019PkySvjV - Antoni (male, friendly)
# MF3mGyEYCl7XYWbV9V6O - Elli (female, energetic)
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
```

#### 4. Run
```bash
python main.py --once
```

**Result:** Full videos with AI voice in `generated_videos/`!

---

## 👤 **Option 2: Virtual Avatar (D-ID)**

Virtual presenter speaking your script like a news anchor.

### Cost
- **~$0.20-0.50 per video**
- D-ID: $5-50/month
- OpenAI: ~$0.03/script

### Setup

#### 1. Get D-ID API Key
1. Go to [D-ID.com](https://www.d-id.com/)
2. Sign up for an account
3. Go to API Access
4. Copy your API key

#### 2. Configure
Edit `.env`:
```bash
OPENAI_API_KEY=sk-...
DID_API_KEY=your_did_api_key
VIDEO_MODE=avatar
```

Optional - choose avatar:
```bash
# Popular presenters:
# amy-jcwCkr1grs - Amy (female, professional)
# josh-jcwCkr1grs - Josh (male, news anchor)
DID_PRESENTER_ID=amy-jcwCkr1grs
```

#### 3. Run
```bash
python main.py --once
```

**Result:** Professional-looking presenter videos in `generated_videos/`!

**Note:** Video generation takes 3-8 minutes per video (D-ID processes on their servers).

---

## 📊 **Option 3: Slideshow + Free TTS (Almost Free!)**

Simple slideshow videos with free text-to-speech.

### Cost
- **~$0.03 per video** (just OpenAI for scripts!)
- Everything else is FREE!

### Setup

#### 1. Install FFmpeg
(Same as Option 1 - see above)

#### 2. Configure
Edit `.env`:
```bash
OPENAI_API_KEY=sk-...
VIDEO_MODE=slideshow
FREE_TTS_SERVICE=gtts  # or edge-tts
```

#### 3. Run
```bash
python main.py --once
```

**Result:** Slideshow videos with voice in `generated_videos/`!

**Best for:** Starting out, low budget, testing the system.

---

## 📤 **Enable Auto-Upload to YouTube (Optional)**

Upload videos automatically to YouTube.

### Setup

#### 1. Get YouTube API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **YouTube Data API v3**
4. Create **OAuth 2.0 Client ID** credentials
5. Download JSON as `client_secrets.json`
6. Put file in project root directory

#### 2. Configure
Edit `.env`:
```bash
AUTO_UPLOAD=true
YOUTUBE_CLIENT_SECRETS_FILE=client_secrets.json
```

#### 3. First Run Authorization
```bash
python main.py --once
```

- Browser will open
- Log in to your YouTube account
- Authorize the app
- Token saved for future runs

**Result:** Videos auto-uploaded to YouTube as PRIVATE (you review before publishing)!

---

## 🎯 **Comparison Table**

| Feature | Script Only | AI Voice | Avatar | Slideshow |
|---------|-------------|----------|--------|-----------|
| **Cost/video** | $0.03 | $0.13-0.33 | $0.23-0.53 | $0.03 |
| **Speed** | 1-2 min | 5-10 min | 3-8 min | 3-5 min |
| **Quality** | N/A | Professional | Very Professional | Basic |
| **Your Work** | Record video | None! | None! | None! |
| **Setup** | Easy | Medium | Easy | Easy |
| **Best For** | DIY creators | Automation | Premium look | Budget/Testing |

---

## 📝 **Complete Configuration Examples**

### Example 1: Maximum Automation
```bash
# .env
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=...
VIDEO_MODE=ai_voice
AUTO_UPLOAD=true
CATEGORIES=sports,finance
MAX_ARTICLES_PER_RUN=5
```

**Run:** `python main.py`  
**Result:** Generates 5 videos every 6 hours and uploads to YouTube automatically!

### Example 2: Budget-Friendly
```bash
# .env
OPENAI_API_KEY=sk-...
VIDEO_MODE=slideshow
AUTO_UPLOAD=false
MAX_ARTICLES_PER_RUN=3
```

**Run:** `python main.py --once`  
**Result:** 3 slideshow videos, costs $0.09 total, manual upload.

### Example 3: Script Only (Manual Production)
```bash
# .env
OPENAI_API_KEY=sk-...
VIDEO_MODE=script_only
```

**Run:** `python main.py --once`  
**Result:** Just scripts, you record videos yourself with full control.

---

## 🔧 **Troubleshooting**

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "FFmpeg not found"
- Install FFmpeg (see Option 1 setup)
- Restart terminal after install

### "ElevenLabs API error: 401"
- Check API key in `.env`
- Verify you have credits on ElevenLabs account

### "D-ID API error: 403"
- Check API key
- Verify D-ID account is active

### Videos not uploading
- Check `client_secrets.json` exists
- Delete `token.pickle` and re-authorize
- Verify YouTube API is enabled in Google Cloud

---

## 💡 **Tips**

### Start Small
1. Begin with `VIDEO_MODE=script_only`
2. Test with `--once` flag
3. Try `slideshow` mode (cheapest)
4. Upgrade to `ai_voice` or `avatar` when ready

### Save Money
- Use `slideshow` mode = almost free!
- Set `MAX_ARTICLES_PER_RUN=1` for testing
- Use `AUTO_UPLOAD=false` to review before uploading

### Best Quality
- Use `avatar` mode for professional look
- Set `VIDEO_RESOLUTION=1920x1080`
- Choose appropriate `VIDEO_STYLE` for your niche

---

## 🚀 **Next Steps**

Once set up:

1. **Test:** `python main.py --once`
2. **Review:** Check `youtube_scripts/` and `generated_videos/`
3. **Adjust:** Modify `.env` settings as needed
4. **Automate:** Remove `--once` to run continuously
5. **Scale:** Increase `MAX_ARTICLES_PER_RUN`

---

**Need help?** Check the README.md for more details!

