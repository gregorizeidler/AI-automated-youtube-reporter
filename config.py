"""Configuration management for the automated reporter."""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    
    # News Sources API Keys
    NEWSAPI_KEY: str = os.getenv("NEWSAPI_KEY", "")
    PEXELS_API_KEY: str = os.getenv("PEXELS_API_KEY", "")
    UNSPLASH_ACCESS_KEY: str = os.getenv("UNSPLASH_ACCESS_KEY", "")
    
    # YouTube Configuration
    YOUTUBE_CLIENT_SECRETS_FILE: str = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE", "client_secrets.json")
    YOUTUBE_CHANNEL_NAME: str = os.getenv("YOUTUBE_CHANNEL_NAME", "Automated News Reporter")
    
    # Video Generation Configuration
    VIDEO_MODE: str = os.getenv("VIDEO_MODE", "script_only")
    # Options: 
    #   - "script_only" = Only generate scripts (no video)
    #   - "ai_voice" = Option 1: AI voice + images (ElevenLabs)
    #   - "avatar" = Option 2: Virtual avatar presenter (D-ID)
    #   - "slideshow" = Option 3: Slideshow + free TTS
    
    # Option 1: AI Voice Settings (ElevenLabs)
    ELEVENLABS_VOICE_ID: str = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # Default: Rachel
    
    # Option 2: Avatar Settings (D-ID)
    DID_API_KEY: str = os.getenv("DID_API_KEY", "")
    DID_PRESENTER_ID: str = os.getenv("DID_PRESENTER_ID", "amy-jcwCkr1grs")
    
    # Option 3: Free TTS Settings
    FREE_TTS_SERVICE: str = os.getenv("FREE_TTS_SERVICE", "gtts")  # gtts or edge-tts
    
    # Video Settings (All options)
    VIDEO_RESOLUTION: str = os.getenv("VIDEO_RESOLUTION", "1920x1080")  # 1920x1080 or 1280x720
    VIDEO_FPS: int = int(os.getenv("VIDEO_FPS", "30"))
    AUTO_UPLOAD: bool = os.getenv("AUTO_UPLOAD", "false").lower() == "true"
    
    # LLM Configuration
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")
    
    # Content Configuration
    CATEGORIES: List[str] = os.getenv("CATEGORIES", "sports,politics,finance").split(",")
    PUBLISH_INTERVAL_HOURS: int = int(os.getenv("PUBLISH_INTERVAL_HOURS", "6"))
    MAX_ARTICLES_PER_RUN: int = int(os.getenv("MAX_ARTICLES_PER_RUN", "3"))
    
    # Multi-language Support
    TARGET_LANGUAGE: str = os.getenv("TARGET_LANGUAGE", "en")  # en, pt, es, fr, de, it, ja, ko, zh
    LANGUAGE_VARIANT: int = int(os.getenv("LANGUAGE_VARIANT", "0"))  # 0 for default variant
    
    # News Collection Options
    USE_NEWSAPI: bool = os.getenv("USE_NEWSAPI", "true").lower() == "true"
    USE_RSS_FEEDS: bool = os.getenv("USE_RSS_FEEDS", "true").lower() == "true"
    USE_REDDIT: bool = os.getenv("USE_REDDIT", "false").lower() == "true"
    USE_GOOGLE_SEARCH: bool = os.getenv("USE_GOOGLE_SEARCH", "true").lower() == "true"
    
    # Voice Personalization
    AUTO_SELECT_VOICE: bool = os.getenv("AUTO_SELECT_VOICE", "true").lower() == "true"
    VOICE_OVERRIDE: str = os.getenv("VOICE_OVERRIDE", "")  # Override auto-selection
    
    # Thumbnail Generation
    THUMBNAIL_MODE: str = os.getenv("THUMBNAIL_MODE", "template")  # template, ai, stock
    AUTO_GENERATE_THUMBNAILS: bool = os.getenv("AUTO_GENERATE_THUMBNAILS", "true").lower() == "true"
    
    # Subtitle Generation
    AUTO_GENERATE_SUBTITLES: bool = os.getenv("AUTO_GENERATE_SUBTITLES", "true").lower() == "true"
    SUBTITLE_METHOD: str = os.getenv("SUBTITLE_METHOD", "script")  # script, whisper
    SUBTITLE_LANGUAGES: List[str] = os.getenv("SUBTITLE_LANGUAGES", "en").split(",")
    
    # Intelligent Scheduling
    USE_INTELLIGENT_SCHEDULING: bool = os.getenv("USE_INTELLIGENT_SCHEDULING", "false").lower() == "true"
    TIMEZONE_OFFSET: int = int(os.getenv("TIMEZONE_OFFSET", "0"))  # Hours from UTC
    MIN_HOURS_BETWEEN_POSTS: int = int(os.getenv("MIN_HOURS_BETWEEN_POSTS", "4"))
    
    # Video Script Configuration
    MIN_SCRIPT_LENGTH: int = 500  # words for ~3-5 min video
    MAX_SCRIPT_LENGTH: int = 1500  # words for ~10-12 min video
    VIDEO_STYLE: str = os.getenv("VIDEO_STYLE", "professional_news")  # professional_news, casual, educational
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration."""
        required = []
        
        if cls.LLM_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            required.append("OPENAI_API_KEY")
        elif cls.LLM_PROVIDER == "anthropic" and not cls.ANTHROPIC_API_KEY:
            required.append("ANTHROPIC_API_KEY")
        
        if required:
            print(f"Missing required configuration: {', '.join(required)}")
            print(f"Note: YouTube credentials will be requested during first upload")
            return False
        
        return True

