"""Automatic subtitle/caption generation for videos."""

import os
import json
from typing import List, Dict, Optional
from pathlib import Path
from datetime import timedelta


class SubtitleGenerator:
    """Generate SRT subtitle files from script and timing."""
    
    def __init__(self, output_dir: str = "subtitles"):
        """Initialize subtitle generator."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_srt_from_script(
        self,
        script_text: str,
        title: str,
        words_per_minute: int = 150,
        chars_per_subtitle: int = 80
    ) -> Optional[str]:
        """
        Generate SRT file from script with estimated timing.
        
        Args:
            script_text: Full video script
            title: Video title (for filename)
            words_per_minute: Speaking speed
            chars_per_subtitle: Characters per subtitle line
        """
        try:
            # Clean script (remove markers)
            clean_text = self._clean_script(script_text)
            
            # Split into subtitle chunks
            subtitle_chunks = self._split_into_chunks(clean_text, chars_per_subtitle)
            
            # Generate timing for each chunk
            subtitles = self._generate_timing(subtitle_chunks, words_per_minute)
            
            # Create SRT content
            srt_content = self._create_srt(subtitles)
            
            # Save to file
            filename = self._sanitize_filename(title) + '.srt'
            filepath = self.output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            
            print(f"✓ Subtitles generated: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error generating subtitles: {str(e)}")
            return None
    
    def generate_srt_from_audio(
        self,
        audio_file: str,
        title: str,
        language: str = 'en'
    ) -> Optional[str]:
        """
        Generate SRT from audio using speech recognition (Whisper).
        
        Args:
            audio_file: Path to audio file
            title: Video title
            language: Language code
        """
        try:
            # Check if Whisper is available
            try:
                import whisper
            except ImportError:
                print("⚠️  Whisper not installed. Install with: pip install openai-whisper")
                return self._fallback_to_script_timing(title)
            
            print(f"🎙️  Transcribing audio with Whisper...")
            
            # Load model (base is a good balance of speed/accuracy)
            model = whisper.load_model("base")
            
            # Transcribe with word-level timestamps
            result = model.transcribe(
                audio_file,
                language=language,
                word_timestamps=True,
                verbose=False
            )
            
            # Generate subtitles from segments
            subtitles = []
            for segment in result['segments']:
                subtitles.append({
                    'start': segment['start'],
                    'end': segment['end'],
                    'text': segment['text'].strip()
                })
            
            # Create SRT content
            srt_content = self._create_srt(subtitles)
            
            # Save to file
            filename = self._sanitize_filename(title) + '.srt'
            filepath = self.output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            
            print(f"✓ Subtitles generated from audio: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error transcribing audio: {str(e)}")
            return None
    
    def generate_vtt_from_srt(self, srt_file: str) -> Optional[str]:
        """
        Convert SRT to WebVTT format (for web players).
        
        Args:
            srt_file: Path to SRT file
        """
        try:
            with open(srt_file, 'r', encoding='utf-8') as f:
                srt_content = f.read()
            
            # VTT header
            vtt_content = "WEBVTT\n\n"
            
            # Convert SRT format to VTT (comma to dot in timestamps)
            vtt_content += srt_content.replace(',', '.')
            
            # Save VTT file
            vtt_file = srt_file.replace('.srt', '.vtt')
            with open(vtt_file, 'w', encoding='utf-8') as f:
                f.write(vtt_content)
            
            print(f"✓ WebVTT generated: {vtt_file}")
            return vtt_file
            
        except Exception as e:
            print(f"❌ Error converting to VTT: {str(e)}")
            return None
    
    def translate_subtitles(
        self,
        srt_file: str,
        target_language: str
    ) -> Optional[str]:
        """
        Translate subtitles to another language using OpenAI.
        
        Args:
            srt_file: Path to original SRT file
            target_language: Target language code
        """
        try:
            from openai import OpenAI
            from config import Config
            
            if not Config.OPENAI_API_KEY:
                print("⚠️  OpenAI API key required for translation")
                return None
            
            client = OpenAI(api_key=Config.OPENAI_API_KEY)
            
            # Read original subtitles
            with open(srt_file, 'r', encoding='utf-8') as f:
                srt_content = f.read()
            
            # Extract text only
            subtitles = self._parse_srt(srt_content)
            texts = [sub['text'] for sub in subtitles]
            
            print(f"🌐 Translating subtitles to {target_language}...")
            
            # Translate in batches
            translated_texts = []
            batch_size = 20
            
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                batch_text = "\n".join(batch)
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"Translate the following subtitles to {target_language}. Maintain the same number of lines and similar length."},
                        {"role": "user", "content": batch_text}
                    ],
                    temperature=0.3
                )
                
                translated_batch = response.choices[0].message.content.strip().split('\n')
                translated_texts.extend(translated_batch)
            
            # Create new subtitles with translated text
            for i, subtitle in enumerate(subtitles):
                if i < len(translated_texts):
                    subtitle['text'] = translated_texts[i]
            
            # Generate new SRT
            srt_content = self._create_srt(subtitles)
            
            # Save translated file
            translated_file = srt_file.replace('.srt', f'_{target_language}.srt')
            with open(translated_file, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            
            print(f"✓ Translated subtitles: {translated_file}")
            return translated_file
            
        except Exception as e:
            print(f"❌ Error translating subtitles: {str(e)}")
            return None
    
    def _clean_script(self, script: str) -> str:
        """Remove markers and clean script."""
        import re
        
        # Remove stage directions
        script = re.sub(r'\[.*?\]', '', script)
        
        # Remove timestamps
        script = re.sub(r'\d+:\d+', '', script)
        
        # Clean whitespace
        script = ' '.join(script.split())
        
        return script
    
    def _split_into_chunks(self, text: str, max_chars: int) -> List[str]:
        """Split text into subtitle-sized chunks."""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1  # +1 for space
            
            if current_length + word_length > max_chars and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = word_length
            else:
                current_chunk.append(word)
                current_length += word_length
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def _generate_timing(self, chunks: List[str], wpm: int) -> List[Dict]:
        """Generate timing for subtitle chunks."""
        subtitles = []
        current_time = 0.0
        
        for chunk in chunks:
            word_count = len(chunk.split())
            duration = (word_count / wpm) * 60  # Convert to seconds
            
            # Minimum 1 second, maximum 7 seconds per subtitle
            duration = max(1.0, min(7.0, duration))
            
            subtitles.append({
                'start': current_time,
                'end': current_time + duration,
                'text': chunk
            })
            
            current_time += duration
        
        return subtitles
    
    def _create_srt(self, subtitles: List[Dict]) -> str:
        """Create SRT formatted content."""
        srt_content = []
        
        for i, subtitle in enumerate(subtitles, 1):
            start_time = self._format_srt_time(subtitle['start'])
            end_time = self._format_srt_time(subtitle['end'])
            
            srt_content.append(f"{i}")
            srt_content.append(f"{start_time} --> {end_time}")
            srt_content.append(subtitle['text'])
            srt_content.append("")  # Empty line between subtitles
        
        return '\n'.join(srt_content)
    
    def _format_srt_time(self, seconds: float) -> str:
        """Format time for SRT (HH:MM:SS,mmm)."""
        td = timedelta(seconds=seconds)
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        secs = int(td.total_seconds() % 60)
        millis = int((td.total_seconds() % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def _parse_srt(self, srt_content: str) -> List[Dict]:
        """Parse SRT content into subtitle list."""
        subtitles = []
        blocks = srt_content.strip().split('\n\n')
        
        for block in blocks:
            lines = block.split('\n')
            if len(lines) >= 3:
                # Parse timing
                timing_line = lines[1]
                times = timing_line.split(' --> ')
                
                if len(times) == 2:
                    start = self._parse_srt_time(times[0])
                    end = self._parse_srt_time(times[1])
                    text = '\n'.join(lines[2:])
                    
                    subtitles.append({
                        'start': start,
                        'end': end,
                        'text': text
                    })
        
        return subtitles
    
    def _parse_srt_time(self, time_str: str) -> float:
        """Parse SRT time to seconds."""
        time_str = time_str.strip().replace(',', '.')
        parts = time_str.split(':')
        
        hours = float(parts[0])
        minutes = float(parts[1])
        seconds = float(parts[2])
        
        return hours * 3600 + minutes * 60 + seconds
    
    def _sanitize_filename(self, title: str) -> str:
        """Sanitize title for filename."""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            title = title.replace(char, '')
        return title[:100].strip()
    
    def _fallback_to_script_timing(self, title: str) -> Optional[str]:
        """Fallback method if Whisper not available."""
        print("⚠️  Using fallback script-based timing")
        return None

