"""Unified video generator manager - chooses and manages video generation."""

from typing import Dict, Optional
from config import Config
from video_generators import AIVoiceGenerator, AvatarGenerator, SlideshowGenerator


class VideoGeneratorManager:
    """Manages video generation based on configured mode."""
    
    def __init__(self):
        """Initialize video generator based on config."""
        self.mode = Config.VIDEO_MODE
        self.generator = None
        
        if self.mode == "ai_voice":
            self.generator = AIVoiceGenerator()
            self.mode_name = "AI Voice + Images (ElevenLabs)"
        elif self.mode == "avatar":
            self.generator = AvatarGenerator()
            self.mode_name = "Virtual Avatar (D-ID)"
        elif self.mode == "slideshow":
            self.generator = SlideshowGenerator()
            self.mode_name = "Slideshow + Free TTS"
        elif self.mode == "script_only":
            self.generator = None
            self.mode_name = "Script Only (No Video)"
        else:
            print(f"⚠️  Unknown VIDEO_MODE: {self.mode}")
            print(f"   Using 'script_only' mode")
            self.mode = "script_only"
            self.generator = None
            self.mode_name = "Script Only (No Video)"
    
    def generate_video(self, script_data: Dict) -> Optional[str]:
        """
        Generate video based on configured mode.
        
        Args:
            script_data: Dictionary with script, title, description, etc.
            
        Returns:
            Path to generated video file or None if script_only mode or failed
        """
        if self.mode == "script_only":
            print("\n📝 Script-only mode - no video generation")
            return None
        
        if not self.generator:
            print("\n❌ No video generator available")
            return None
        
        print(f"\n🎬 Using mode: {self.mode_name}")
        
        try:
            video_path = self.generator.generate_video(script_data)
            return video_path
        except Exception as e:
            print(f"\n❌ Video generation failed: {str(e)}")
            return None
    
    def get_mode_info(self) -> Dict:
        """Get information about current mode."""
        mode_info = {
            "script_only": {
                "name": "Script Only",
                "description": "Generates scripts without creating videos",
                "cost": "$0.03/script",
                "speed": "Fast (~1-2 min)",
                "requires": ["OpenAI/Anthropic API key"]
            },
            "ai_voice": {
                "name": "AI Voice + Images",
                "description": "Professional voice narration with stock images",
                "cost": "$0.10-0.30/video",
                "speed": "Medium (~5-10 min)",
                "requires": ["ElevenLabs API key", "FFmpeg installed"]
            },
            "avatar": {
                "name": "Virtual Avatar",
                "description": "Virtual presenter speaking your script",
                "cost": "$0.20-0.50/video",
                "speed": "Slow (~3-8 min)",
                "requires": ["D-ID API key"]
            },
            "slideshow": {
                "name": "Slideshow + Free TTS",
                "description": "Simple slides with free text-to-speech",
                "cost": "$0.03/video (almost free!)",
                "speed": "Fast (~3-5 min)",
                "requires": ["FFmpeg installed", "gTTS or edge-tts"]
            }
        }
        
        return mode_info.get(self.mode, {})
    
    def print_mode_info(self):
        """Print information about current mode."""
        info = self.get_mode_info()
        
        print("\n" + "="*70)
        print(f"VIDEO GENERATION MODE: {self.mode_name.upper()}")
        print("="*70)
        
        if info:
            print(f"📝 Description: {info['description']}")
            print(f"💰 Cost: {info['cost']}")
            print(f"⏱️  Speed: {info['speed']}")
            print(f"📋 Requires: {', '.join(info['requires'])}")
        
        print("="*70 + "\n")

