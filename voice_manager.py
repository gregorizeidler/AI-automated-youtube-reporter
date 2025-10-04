"""Voice personalization system for different categories and languages."""

from typing import Dict, Optional
from config import Config
from multilang import LanguageManager


class VoiceProfile:
    """Voice profile configuration."""
    
    def __init__(
        self,
        voice_id: str,
        name: str,
        gender: str,
        accent: str,
        style: str,
        language: str = 'en'
    ):
        """Initialize voice profile."""
        self.voice_id = voice_id
        self.name = name
        self.gender = gender
        self.accent = accent
        self.style = style
        self.language = language


class VoiceManager:
    """Manages voice selection based on category and language."""
    
    # ElevenLabs voice profiles
    ELEVENLABS_VOICES = {
        'en': {
            'sports': VoiceProfile(
                voice_id='pNInz6obpgDQGcFmaJgB',  # Adam - energetic male
                name='Adam',
                gender='male',
                accent='american',
                style='energetic',
                language='en'
            ),
            'politics': VoiceProfile(
                voice_id='21m00Tcm4TlvDq8ikWAM',  # Rachel - professional female
                name='Rachel',
                gender='female',
                accent='american',
                style='authoritative',
                language='en'
            ),
            'finance': VoiceProfile(
                voice_id='VR6AewLTigWG4xSOukaG',  # Arnold - serious male
                name='Arnold',
                gender='male',
                accent='american',
                style='professional',
                language='en'
            ),
            'technology': VoiceProfile(
                voice_id='ErXwobaYiN019PkySvjV',  # Antoni - casual male
                name='Antoni',
                gender='male',
                accent='american',
                style='casual',
                language='en'
            ),
            'entertainment': VoiceProfile(
                voice_id='MF3mGyEYCl7XYWbV9V6O',  # Elli - friendly female
                name='Elli',
                gender='female',
                accent='american',
                style='friendly',
                language='en'
            ),
            'default': VoiceProfile(
                voice_id='21m00Tcm4TlvDq8ikWAM',  # Rachel
                name='Rachel',
                gender='female',
                accent='american',
                style='professional',
                language='en'
            ),
        },
        'pt': {
            'sports': VoiceProfile(
                voice_id='pt-BR-AntonioNeural',
                name='Antonio',
                gender='male',
                accent='brazilian',
                style='energetic',
                language='pt'
            ),
            'politics': VoiceProfile(
                voice_id='pt-BR-FranciscaNeural',
                name='Francisca',
                gender='female',
                accent='brazilian',
                style='authoritative',
                language='pt'
            ),
            'finance': VoiceProfile(
                voice_id='pt-BR-FabioNeural',
                name='Fabio',
                gender='male',
                accent='brazilian',
                style='professional',
                language='pt'
            ),
            'default': VoiceProfile(
                voice_id='pt-BR-FranciscaNeural',
                name='Francisca',
                gender='female',
                accent='brazilian',
                style='professional',
                language='pt'
            ),
        },
        'es': {
            'sports': VoiceProfile(
                voice_id='es-ES-AlvaroNeural',
                name='Alvaro',
                gender='male',
                accent='spanish',
                style='energetic',
                language='es'
            ),
            'politics': VoiceProfile(
                voice_id='es-ES-ElviraNeural',
                name='Elvira',
                gender='female',
                accent='spanish',
                style='authoritative',
                language='es'
            ),
            'default': VoiceProfile(
                voice_id='es-ES-ElviraNeural',
                name='Elvira',
                gender='female',
                accent='spanish',
                style='professional',
                language='es'
            ),
        }
    }
    
    @classmethod
    def get_voice_for_category(
        cls, 
        category: str, 
        language: str = 'en',
        service: str = 'elevenlabs'
    ) -> VoiceProfile:
        """
        Get optimal voice for category and language.
        
        Args:
            category: Content category
            language: Language code
            service: TTS service (elevenlabs, gtts, edge-tts)
        """
        if service == 'elevenlabs':
            voices = cls.ELEVENLABS_VOICES.get(language, cls.ELEVENLABS_VOICES['en'])
            return voices.get(category, voices['default'])
        
        # For free TTS services, return basic config
        return VoiceProfile(
            voice_id=LanguageManager.get_voice_code(language),
            name='Default',
            gender='neutral',
            accent='standard',
            style='neutral',
            language=language
        )
    
    @classmethod
    def get_voice_settings(
        cls,
        category: str,
        language: str = 'en'
    ) -> Dict:
        """
        Get voice settings including stability, similarity, etc.
        
        These settings work with ElevenLabs API.
        """
        settings_by_category = {
            'sports': {
                'stability': 0.5,  # More dynamic
                'similarity_boost': 0.7,
                'style': 0.7,  # More expressive
            },
            'politics': {
                'stability': 0.75,  # More stable/serious
                'similarity_boost': 0.8,
                'style': 0.3,  # More neutral
            },
            'finance': {
                'stability': 0.8,  # Very stable
                'similarity_boost': 0.75,
                'style': 0.2,  # Neutral
            },
            'technology': {
                'stability': 0.6,
                'similarity_boost': 0.75,
                'style': 0.5,
            },
            'entertainment': {
                'stability': 0.5,
                'similarity_boost': 0.7,
                'style': 0.8,  # Very expressive
            },
            'default': {
                'stability': 0.65,
                'similarity_boost': 0.75,
                'style': 0.5,
            }
        }
        
        return settings_by_category.get(category, settings_by_category['default'])
    
    @classmethod
    def list_available_voices(cls, language: str = 'en') -> Dict[str, VoiceProfile]:
        """List all available voices for a language."""
        return cls.ELEVENLABS_VOICES.get(language, cls.ELEVENLABS_VOICES['en'])
    
    @classmethod
    def print_voice_info(cls, category: str, language: str = 'en'):
        """Print voice information for category."""
        voice = cls.get_voice_for_category(category, language)
        settings = cls.get_voice_settings(category, language)
        
        print(f"\n🎙️  Voice Profile for {category.upper()} ({language.upper()})")
        print("=" * 60)
        print(f"Voice: {voice.name}")
        print(f"Gender: {voice.gender}")
        print(f"Accent: {voice.accent}")
        print(f"Style: {voice.style}")
        print(f"Voice ID: {voice.voice_id}")
        print(f"\nSettings:")
        print(f"  Stability: {settings['stability']}")
        print(f"  Similarity: {settings['similarity_boost']}")
        print(f"  Expressiveness: {settings['style']}")
        print("=" * 60)

