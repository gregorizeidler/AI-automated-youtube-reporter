"""Automatic thumbnail generation with AI or templates."""

import os
import requests
from typing import Optional, Dict
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from config import Config


class ThumbnailGenerator:
    """Generate YouTube thumbnails automatically."""
    
    def __init__(self, output_dir: str = "thumbnails"):
        """Initialize thumbnail generator."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Default thumbnail size for YouTube
        self.width = 1280
        self.height = 720
    
    def generate_template_thumbnail(
        self,
        title: str,
        category: str,
        thumbnail_text: Optional[str] = None
    ) -> Optional[str]:
        """
        Generate thumbnail from template with text overlay.
        
        Args:
            title: Video title
            category: Category for styling
            thumbnail_text: Short text for thumbnail (5 words max)
        """
        try:
            # Create image
            img = Image.new('RGB', (self.width, self.height), color=self._get_category_color(category))
            draw = ImageDraw.Draw(img)
            
            # Try to load a nice font, fallback to default
            try:
                font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
                font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
            except:
                try:
                    font_large = ImageFont.truetype("arial.ttf", 80)
                    font_small = ImageFont.truetype("arial.ttf", 40)
                except:
                    font_large = ImageFont.load_default()
                    font_small = ImageFont.load_default()
            
            # Draw gradient background effect
            for i in range(self.height):
                alpha = i / self.height
                color = self._blend_colors(
                    self._get_category_color(category),
                    self._darken_color(self._get_category_color(category)),
                    alpha
                )
                draw.rectangle([(0, i), (self.width, i + 1)], fill=color)
            
            # Main text
            text = thumbnail_text or title[:50]
            text = text.upper()
            
            # Add text shadow for readability
            shadow_offset = 4
            self._draw_text_centered(
                draw, text, font_large,
                (self.width // 2 + shadow_offset, self.height // 2 + shadow_offset),
                (0, 0, 0, 180)  # Black shadow
            )
            
            # Main text
            self._draw_text_centered(
                draw, text, font_large,
                (self.width // 2, self.height // 2),
                (255, 255, 255)  # White text
            )
            
            # Category badge
            badge_text = category.upper()
            badge_width = 200
            badge_height = 50
            badge_x = 30
            badge_y = 30
            
            # Badge background
            draw.rectangle(
                [(badge_x, badge_y), (badge_x + badge_width, badge_y + badge_height)],
                fill=(255, 0, 0),  # Red like YouTube
                outline=(255, 255, 255),
                width=3
            )
            
            # Badge text
            self._draw_text_centered(
                draw, badge_text, font_small,
                (badge_x + badge_width // 2, badge_y + badge_height // 2),
                (255, 255, 255)
            )
            
            # Save thumbnail
            filename = self._sanitize_filename(title) + '.png'
            filepath = self.output_dir / filename
            img.save(filepath, 'PNG', quality=95)
            
            print(f"✓ Thumbnail generated: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error generating thumbnail: {str(e)}")
            return None
    
    def generate_ai_thumbnail(
        self,
        prompt: str,
        title: str
    ) -> Optional[str]:
        """
        Generate thumbnail using DALL-E or similar AI.
        
        Args:
            prompt: Image generation prompt
            title: Video title for filename
        """
        if not hasattr(Config, 'OPENAI_API_KEY') or not Config.OPENAI_API_KEY:
            print("⚠️  OpenAI API key not configured for AI thumbnails")
            return None
        
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=Config.OPENAI_API_KEY)
            
            print(f"🎨 Generating AI thumbnail with DALL-E...")
            
            # Generate image with DALL-E
            response = client.images.generate(
                model="dall-e-3",
                prompt=f"YouTube thumbnail for: {prompt}. Professional, eye-catching, 16:9 aspect ratio, bold text, high contrast",
                size="1792x1024",  # Closest to 16:9
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            
            # Download image
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()
            
            # Save image
            filename = self._sanitize_filename(title) + '_ai.png'
            filepath = self.output_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(img_response.content)
            
            # Resize to YouTube dimensions
            img = Image.open(filepath)
            img = img.resize((self.width, self.height), Image.Resampling.LANCZOS)
            img.save(filepath, 'PNG', quality=95)
            
            print(f"✓ AI thumbnail generated: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error generating AI thumbnail: {str(e)}")
            # Fallback to template
            return self.generate_template_thumbnail(title, 'default')
    
    def download_stock_image(
        self,
        query: str,
        title: str
    ) -> Optional[str]:
        """
        Download stock image from Pexels or Unsplash.
        
        Args:
            query: Search query
            title: Video title for filename
        """
        # Try Pexels first
        if hasattr(Config, 'PEXELS_API_KEY') and Config.PEXELS_API_KEY:
            return self._download_from_pexels(query, title)
        
        # Try Unsplash
        if hasattr(Config, 'UNSPLASH_ACCESS_KEY') and Config.UNSPLASH_ACCESS_KEY:
            return self._download_from_unsplash(query, title)
        
        print("⚠️  No stock image API keys configured")
        return None
    
    def _download_from_pexels(self, query: str, title: str) -> Optional[str]:
        """Download from Pexels."""
        try:
            headers = {'Authorization': Config.PEXELS_API_KEY}
            response = requests.get(
                'https://api.pexels.com/v1/search',
                headers=headers,
                params={'query': query, 'per_page': 1, 'orientation': 'landscape'},
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            if data['photos']:
                image_url = data['photos'][0]['src']['large2x']
                return self._download_and_save_image(image_url, title, 'pexels')
            
        except Exception as e:
            print(f"❌ Pexels error: {str(e)}")
        
        return None
    
    def _download_from_unsplash(self, query: str, title: str) -> Optional[str]:
        """Download from Unsplash."""
        try:
            headers = {'Authorization': f'Client-ID {Config.UNSPLASH_ACCESS_KEY}'}
            response = requests.get(
                'https://api.unsplash.com/search/photos',
                headers=headers,
                params={'query': query, 'per_page': 1, 'orientation': 'landscape'},
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            if data['results']:
                image_url = data['results'][0]['urls']['regular']
                return self._download_and_save_image(image_url, title, 'unsplash')
            
        except Exception as e:
            print(f"❌ Unsplash error: {str(e)}")
        
        return None
    
    def _download_and_save_image(self, url: str, title: str, source: str) -> Optional[str]:
        """Download and save image."""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            filename = self._sanitize_filename(title) + f'_{source}.jpg'
            filepath = self.output_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            # Resize to thumbnail dimensions
            img = Image.open(filepath)
            img = img.resize((self.width, self.height), Image.Resampling.LANCZOS)
            img.save(filepath, 'JPEG', quality=95)
            
            print(f"✓ Stock image downloaded: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error downloading image: {str(e)}")
            return None
    
    def _get_category_color(self, category: str) -> tuple:
        """Get color scheme for category."""
        colors = {
            'sports': (0, 100, 200),  # Blue
            'politics': (150, 0, 0),  # Dark red
            'finance': (0, 120, 0),  # Green
            'technology': (100, 0, 150),  # Purple
            'entertainment': (200, 50, 0),  # Orange
            'default': (50, 50, 50)  # Gray
        }
        return colors.get(category, colors['default'])
    
    def _darken_color(self, color: tuple, factor: float = 0.5) -> tuple:
        """Darken a color."""
        return tuple(int(c * factor) for c in color)
    
    def _blend_colors(self, color1: tuple, color2: tuple, alpha: float) -> tuple:
        """Blend two colors."""
        return tuple(int(c1 * (1 - alpha) + c2 * alpha) for c1, c2 in zip(color1, color2))
    
    def _draw_text_centered(self, draw, text: str, font, position: tuple, color: tuple):
        """Draw centered text."""
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = position[0] - text_width // 2
        y = position[1] - text_height // 2
        draw.text((x, y), text, font=font, fill=color)
    
    def _sanitize_filename(self, title: str) -> str:
        """Sanitize title for filename."""
        # Remove invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            title = title.replace(char, '')
        
        # Limit length
        return title[:100].strip()

