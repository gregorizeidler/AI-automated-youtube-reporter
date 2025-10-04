"""Option 3: Slideshow + Free TTS video generator."""

import os
from typing import Dict, Optional, List
from .base_generator import BaseVideoGenerator
from config import Config
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import (
    ImageClip, AudioFileClip, concatenate_videoclips,
    CompositeVideoClip, TextClip
)


class SlideshowGenerator(BaseVideoGenerator):
    """Generate simple slideshow videos with free text-to-speech."""
    
    def __init__(self):
        """Initialize slideshow generator."""
        super().__init__()
        self.tts_service = Config.FREE_TTS_SERVICE
    
    def generate_video(self, script_data: Dict) -> Optional[str]:
        """
        Generate slideshow video with free TTS.
        
        Steps:
        1. Convert script to audio using free TTS (gTTS or edge-tts)
        2. Split script into key points
        3. Create slides for each point
        4. Combine slides + audio into video
        """
        try:
            print(f"\n🎬 Generating slideshow video with Free TTS...")
            print(f"   Title: {script_data['title']}")
            
            # Step 1: Generate audio
            print(f"   📢 Generating speech ({self.tts_service})...")
            audio_path = self._generate_audio(script_data['script'])
            
            if not audio_path:
                return None
            
            # Step 2: Create slides
            print("   📊 Creating slides...")
            slides = self._create_slides(script_data)
            
            # Step 3: Create video
            print("   🎥 Assembling video...")
            video_path = self._create_video(
                audio_path=audio_path,
                slides=slides,
                title=script_data['title']
            )
            
            # Cleanup
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            for slide in slides:
                if os.path.exists(slide):
                    os.remove(slide)
            
            if video_path:
                print(f"   ✅ Video generated: {video_path}")
            
            return video_path
            
        except Exception as e:
            print(f"   ❌ Error generating video: {str(e)}")
            return None
    
    def _generate_audio(self, text: str) -> Optional[str]:
        """Generate audio using free TTS service."""
        audio_path = os.path.join(self.output_dir, "temp_audio.mp3")
        
        try:
            if self.tts_service == "gtts":
                from gtts import gTTS
                
                tts = gTTS(text=text, lang='en', slow=False)
                tts.save(audio_path)
                return audio_path
                
            elif self.tts_service == "edge-tts":
                import edge_tts
                import asyncio
                
                async def generate():
                    communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
                    await communicate.save(audio_path)
                
                asyncio.run(generate())
                return audio_path
            
            else:
                print(f"   ⚠️  Unknown TTS service: {self.tts_service}")
                return None
                
        except Exception as e:
            print(f"   ❌ TTS error: {str(e)}")
            return None
    
    def _create_slides(self, script_data: Dict) -> List[str]:
        """Create slide images from script content."""
        slides = []
        
        # Title slide
        title_slide = self._create_slide(
            text=script_data['title'],
            subtitle="",
            is_title=True,
            index=0
        )
        slides.append(title_slide)
        
        # Split script into segments (by paragraphs or sentences)
        script = script_data['script']
        segments = script.split('\n\n')[:10]  # Max 10 slides
        
        for i, segment in enumerate(segments, 1):
            if segment.strip():
                # Take first 200 chars for slide
                text = segment.strip()[:200]
                if len(segment) > 200:
                    text += "..."
                
                slide = self._create_slide(
                    text=text,
                    subtitle=f"Slide {i}",
                    is_title=False,
                    index=i
                )
                slides.append(slide)
        
        # End slide
        end_slide = self._create_slide(
            text="Thanks for watching!",
            subtitle="Like, Subscribe & Comment",
            is_title=True,
            index=len(slides)
        )
        slides.append(end_slide)
        
        return slides
    
    def _create_slide(
        self,
        text: str,
        subtitle: str,
        is_title: bool,
        index: int
    ) -> str:
        """Create a single slide image."""
        # Create 1920x1080 image
        img = Image.new('RGB', (1920, 1080), color=(20, 30, 50))
        draw = ImageDraw.Draw(img)
        
        try:
            # Try to load system fonts
            if is_title:
                font_size = 90
                sub_font_size = 50
            else:
                font_size = 60
                sub_font_size = 40
            
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
                sub_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", sub_font_size)
            except:
                font = ImageFont.load_default()
                sub_font = ImageFont.load_default()
            
            # Wrap text
            wrapped_text = self._wrap_text(text, font, 1800)
            
            # Calculate total height
            line_height = font_size + 20
            total_height = len(wrapped_text) * line_height
            
            # Start position (centered vertically)
            y = (1080 - total_height) // 2
            
            # Draw each line
            for line in wrapped_text:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x = (1920 - text_width) // 2
                
                draw.text((x, y), line, fill=(255, 255, 255), font=font)
                y += line_height
            
            # Add subtitle at bottom
            if subtitle:
                bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
                text_width = bbox[2] - bbox[0]
                x = (1920 - text_width) // 2
                draw.text((x, 980), subtitle, fill=(200, 200, 200), font=sub_font)
            
        except Exception as e:
            print(f"   ⚠️  Font rendering error: {e}")
            # Fallback to simple text
            draw.text((100, 500), text[:100], fill=(255, 255, 255))
        
        # Save slide
        slide_path = os.path.join(self.output_dir, f"temp_slide_{index}.png")
        img.save(slide_path)
        
        return slide_path
    
    def _wrap_text(self, text: str, font, max_width: int) -> List[str]:
        """Wrap text to fit within max_width."""
        words = text.split()
        lines = []
        current_line = []
        
        draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines[:6]  # Max 6 lines per slide
    
    def _create_video(self, audio_path: str, slides: List[str], title: str) -> str:
        """Create final video from slides and audio."""
        # Load audio
        audio_clip = AudioFileClip(audio_path)
        total_duration = audio_clip.duration
        
        # Calculate duration per slide
        slide_duration = total_duration / len(slides)
        
        # Create video clips
        clips = []
        for slide_path in slides:
            clip = (ImageClip(slide_path)
                   .set_duration(slide_duration)
                   .resize(height=1080))
            clips.append(clip)
        
        # Concatenate
        video = concatenate_videoclips(clips, method="compose")
        video = video.set_audio(audio_clip)
        
        # Export
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
        
        return output_path

