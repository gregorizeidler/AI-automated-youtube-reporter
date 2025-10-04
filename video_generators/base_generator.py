"""Base class for video generators."""

from abc import ABC, abstractmethod
from typing import Dict, Optional
import os


class BaseVideoGenerator(ABC):
    """Base class for all video generator implementations."""
    
    def __init__(self):
        """Initialize base video generator."""
        self.output_dir = "generated_videos"
        os.makedirs(self.output_dir, exist_ok=True)
    
    @abstractmethod
    def generate_video(self, script_data: Dict) -> Optional[str]:
        """
        Generate video from script data.
        
        Args:
            script_data: Dictionary containing script, title, etc.
            
        Returns:
            Path to generated video file or None if failed
        """
        pass
    
    def _sanitize_filename(self, title: str) -> str:
        """Create safe filename from title."""
        import re
        from datetime import datetime
        
        # Remove special characters
        safe_title = re.sub(r'[^\w\s-]', '', title)
        safe_title = re.sub(r'[-\s]+', '_', safe_title)
        safe_title = safe_title[:50]  # Limit length
        
        # Add timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        return f"{timestamp}_{safe_title}.mp4"
    
    def _estimate_duration(self, text: str, words_per_minute: int = 150) -> float:
        """Estimate audio duration from text."""
        word_count = len(text.split())
        return (word_count / words_per_minute) * 60  # Convert to seconds

