"""Multi-language support module."""

from typing import Dict, Optional
from config import Config


class LanguageManager:
    """Manages multi-language content generation."""
    
    # Supported languages with their codes and names
    LANGUAGES = {
        'en': {'name': 'English', 'voice_codes': ['en-US', 'en-GB', 'en-AU']},
        'pt': {'name': 'Português', 'voice_codes': ['pt-BR', 'pt-PT']},
        'es': {'name': 'Español', 'voice_codes': ['es-ES', 'es-MX', 'es-AR']},
        'fr': {'name': 'Français', 'voice_codes': ['fr-FR', 'fr-CA']},
        'de': {'name': 'Deutsch', 'voice_codes': ['de-DE']},
        'it': {'name': 'Italiano', 'voice_codes': ['it-IT']},
        'ja': {'name': '日本語', 'voice_codes': ['ja-JP']},
        'ko': {'name': '한국어', 'voice_codes': ['ko-KR']},
        'zh': {'name': '中文', 'voice_codes': ['zh-CN', 'zh-TW']},
    }
    
    # Language-specific prompts
    PROMPT_TEMPLATES = {
        'en': {
            'instruction': 'Create a complete video script in English.',
            'style': 'professional news anchor style',
        },
        'pt': {
            'instruction': 'Crie um roteiro completo de vídeo em Português.',
            'style': 'estilo profissional de âncora de notícias',
        },
        'es': {
            'instruction': 'Crea un guión completo de video en Español.',
            'style': 'estilo profesional de presentador de noticias',
        },
        'fr': {
            'instruction': 'Créez un script vidéo complet en Français.',
            'style': 'style professionnel de présentateur de nouvelles',
        },
        'de': {
            'instruction': 'Erstellen Sie ein vollständiges Videoskript auf Deutsch.',
            'style': 'professioneller Nachrichtensprecher-Stil',
        },
        'it': {
            'instruction': 'Crea uno script video completo in Italiano.',
            'style': 'stile professionale di conduttore di notizie',
        },
        'ja': {
            'instruction': '日本語で完全なビデオスクリプトを作成してください。',
            'style': 'プロのニュースキャスタースタイル',
        },
        'ko': {
            'instruction': '한국어로 완전한 비디오 스크립트를 작성하세요.',
            'style': '전문 뉴스 앵커 스타일',
        },
        'zh': {
            'instruction': '用中文创建完整的视频脚本。',
            'style': '专业新闻主播风格',
        },
    }
    
    @classmethod
    def get_prompt_instruction(cls, language: str) -> str:
        """Get language-specific prompt instruction."""
        return cls.PROMPT_TEMPLATES.get(language, cls.PROMPT_TEMPLATES['en'])['instruction']
    
    @classmethod
    def get_style_description(cls, language: str) -> str:
        """Get language-specific style description."""
        return cls.PROMPT_TEMPLATES.get(language, cls.PROMPT_TEMPLATES['en'])['style']
    
    @classmethod
    def get_voice_code(cls, language: str, variant: int = 0) -> str:
        """
        Get voice code for TTS services.
        
        Args:
            language: Language code (e.g., 'pt', 'en')
            variant: Variant index (e.g., 0 for pt-BR, 1 for pt-PT)
        """
        lang_data = cls.LANGUAGES.get(language, cls.LANGUAGES['en'])
        voice_codes = lang_data['voice_codes']
        
        if variant < len(voice_codes):
            return voice_codes[variant]
        return voice_codes[0]
    
    @classmethod
    def is_supported(cls, language: str) -> bool:
        """Check if language is supported."""
        return language in cls.LANGUAGES
    
    @classmethod
    def get_language_name(cls, language: str) -> str:
        """Get full language name."""
        return cls.LANGUAGES.get(language, cls.LANGUAGES['en'])['name']
    
    @classmethod
    def translate_metadata(cls, language: str) -> Dict[str, str]:
        """Get translated metadata labels."""
        translations = {
            'en': {
                'title': 'Title',
                'description': 'Description',
                'tags': 'Tags',
                'subscribe_cta': 'Don\'t forget to like and subscribe!',
                'sources': 'Sources',
                'thumbnail_text': 'BREAKING NEWS',
            },
            'pt': {
                'title': 'Título',
                'description': 'Descrição',
                'tags': 'Tags',
                'subscribe_cta': 'Não esqueça de curtir e se inscrever!',
                'sources': 'Fontes',
                'thumbnail_text': 'ÚLTIMA HORA',
            },
            'es': {
                'title': 'Título',
                'description': 'Descripción',
                'tags': 'Etiquetas',
                'subscribe_cta': '¡No olvides dar like y suscribirte!',
                'sources': 'Fuentes',
                'thumbnail_text': 'ÚLTIMA HORA',
            },
            'fr': {
                'title': 'Titre',
                'description': 'Description',
                'tags': 'Tags',
                'subscribe_cta': 'N\'oubliez pas d\'aimer et de vous abonner!',
                'sources': 'Sources',
                'thumbnail_text': 'DERNIÈRE MINUTE',
            },
        }
        
        return translations.get(language, translations['en'])


def get_target_language() -> str:
    """Get configured target language."""
    return Config.TARGET_LANGUAGE if hasattr(Config, 'TARGET_LANGUAGE') else 'en'

