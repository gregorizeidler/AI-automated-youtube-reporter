"""Option 1: AI Voice + Images video generator using ElevenLabs."""

import os
import requests
from typing import Dict, Optional, List
from .base_generator import BaseVideoGenerator
from config import Config
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import (
    ImageClip, AudioFileClip, concatenate_videoclips,
    CompositeVideoClip, TextClip
)


class AIVoiceGenerator(BaseVideoGenerator):
    """Generate videos with AI voice narration and stock images."""
    
    def __init__(self):
        """Initialize AI voice generator."""
        super().__init__()
        self.api_key = Config.ELEVENLABS_API_KEY
        self.voice_id = Config.ELEVENLABS_VOICE_ID
        
    def generate_video(self, script_data: Dict) -> Optional[str]:
        """
        Generate video with AI voice and images.
        
        Steps:
        1. Convert script to audio using ElevenLabs
        2. Download relevant stock images
        3. Create video with images + audio + subtitles
        4. Export final video
        """
        try:
            print(f"\n🎬 Generating video with AI Voice...")
            print(f"   Title: {script_data['title']}")
            
            # Step 1: Generate audio
            print("   📢 Generating AI voice...")
            audio_path = self._generate_audio(script_data['script'])
            if not audio_path:
                return None
            
            # Step 2: Get images
            print("   🖼️  Fetching stock images...")
            images = self._get_stock_images(script_data)
            
            # Step 3: Create video
            print("   🎥 Creating video...")
            video_path = self._create_video(
                audio_path=audio_path,
                images=images,
                title=script_data['title'],
                script=script_data['script']
            )
            
            # Cleanup temp files
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            print(f"   ✅ Video generated: {video_path}")
            return video_path
            
        except Exception as e:
            print(f"   ❌ Error generating video: {str(e)}")
            return None
    
    def _generate_audio(self, text: str) -> Optional[str]:
        """Generate audio using ElevenLabs API."""
        if not self.api_key:
            print("   ⚠️  ElevenLabs API key not configured")
            return None
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                audio_path = os.path.join(self.output_dir, "temp_audio.mp3")
                with open(audio_path, 'wb') as f:
                    f.write(response.content)
                return audio_path
            else:
                print(f"   ❌ ElevenLabs API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Audio generation error: {str(e)}")
            return None
    
    def _get_stock_images(self, script_data: Dict) -> List[str]:
        """Download relevant stock images from Pexels."""
        images = []
        category = script_data.get('category', 'news')
        
        # Search terms based on category
        search_terms = {
            'sports': ['sports', 'athlete', 'game', 'competition', 'stadium'],
            'politics': ['government', 'politics', 'capitol', 'meeting', 'news'],
            'finance': ['business', 'finance', 'stock market', 'money', 'economy']
        }
        
        terms = search_terms.get(category, ['news', 'breaking news'])
        
        # Try to download images (simplified - you'd use Pexels API)
        # For now, create placeholder images
        for i, term in enumerate(terms[:5]):
            image_path = self._create_placeholder_image(term, i)
            if image_path:
                images.append(image_path)
        
        return images
    
    def _create_placeholder_image(self, text: str, index: int) -> str:
        """Create a simple placeholder image with text."""
        # Create 1920x1080 image
        img = Image.new('RGB', (1920, 1080), color=(30, 30, 40))
        draw = ImageDraw.Draw(img)
        
        # Add text
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
        except:
            font = ImageFont.load_default()
        
        # Center text
        text_upper = text.upper()
        bbox = draw.textbbox((0, 0), text_upper, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (1920 - text_width) // 2
        y = (1080 - text_height) // 2
        
        draw.text((x, y), text_upper, fill=(255, 255, 255), font=font)
        
        # Save
        image_path = os.path.join(self.output_dir, f"temp_img_{index}.png")
        img.save(image_path)
        
        return image_path
    
    def _create_video(
        self,
        audio_path: str,
        images: List[str],
        title: str,
        script: str
    ) -> str:
        """Create final video with images, audio, and text overlay."""
        
        # Load audio to get duration
        audio_clip = AudioFileClip(audio_path)
        total_duration = audio_clip.duration
        
        # Calculate duration per image
        image_duration = total_duration / len(images) if images else total_duration
        
        # Create image clips
        clips = []
        for img_path in images:
            clip = (ImageClip(img_path)
                   .set_duration(image_duration)
                   .resize(height=1080))
            clips.append(clip)
        
        # Concatenate images
        video = concatenate_videoclips(clips, method="compose")
        
        # Add audio
        video = video.set_audio(audio_clip)
        
        # Add title overlay at start
        title_clip = (TextClip(title, fontsize=70, color='white', 
                              bg_color='black', size=(1800, None))
                     .set_position('center')
                     .set_duration(3)
                     .fadeout(0.5))
        
        video = CompositeVideoClip([video, title_clip.set_start(0)])
        
        # Export video
        output_filename = self._sanitize_filename(title)
        output_path = os.path.join(self.output_dir, output_filename)
        
        video.write_videofile(
            output_path,
            fps=Config.VIDEO_FPS,
            codec='libx264',
            audio_codec='aac',
            threads=4,
            preset='medium'
        )
        
        # Cleanup temp images
        for img_path in images:
            if os.path.exists(img_path):
                os.remove(img_path)
        
        return output_path

