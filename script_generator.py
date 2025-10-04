"""YouTube video script generation module using LLMs."""

from typing import List, Dict, Optional
from datetime import datetime
from config import Config


class ScriptGenerator:
    """Generates professional YouTube video scripts using LLMs."""
    
    def __init__(self):
        """Initialize the script generator."""
        self.provider = Config.LLM_PROVIDER
        self.model = Config.MODEL_NAME
        
        if self.provider == "openai":
            from openai import OpenAI
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        elif self.provider == "anthropic":
            from anthropic import Anthropic
            self.client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def generate_video_script(self, news_items: List[Dict], category: str) -> Optional[Dict]:
        """
        Generate a comprehensive video script from multiple news sources.
        
        Args:
            news_items: List of news articles to synthesize
            category: Category of the video (sports, politics, finance)
            
        Returns:
            Dictionary with 'title', 'script', 'description', 'tags', 'category', 'hook', 'timestamps'
        """
        if not news_items:
            print(f"No news items provided for {category}")
            return None
        
        # Create context from news items
        context = self._create_context(news_items)
        
        # Generate the script
        prompt = self._create_prompt(context, category)
        
        try:
            if self.provider == "openai":
                script_data = self._generate_with_openai(prompt)
            else:
                script_data = self._generate_with_anthropic(prompt)
            
            if script_data:
                script_data['category'] = category
                script_data['sources'] = [item['url'] for item in news_items[:5]]
                script_data['generated_at'] = datetime.now().isoformat()
            
            return script_data
            
        except Exception as e:
            print(f"Error generating script for {category}: {str(e)}")
            return None
    
    def _create_context(self, news_items: List[Dict]) -> str:
        """Create context string from news items."""
        context_parts = []
        
        for i, item in enumerate(news_items[:5], 1):
            context_parts.append(f"""
Article {i}:
Title: {item.get('title', 'N/A')}
Source: {item.get('source', 'N/A')}
Published: {item.get('published_at', 'N/A')}
Description: {item.get('description', 'N/A')}
Content: {item.get('content', 'N/A')[:500]}...
URL: {item.get('url', 'N/A')}
""")
        
        return "\n".join(context_parts)
    
    def _create_prompt(self, context: str, category: str) -> str:
        """Create the prompt for script generation."""
        style_guide = {
            "professional_news": "professional news anchor style, authoritative and informative",
            "casual": "conversational and engaging, like talking to a friend",
            "educational": "clear and educational, explaining complex topics simply"
        }
        
        style = style_guide.get(Config.VIDEO_STYLE, style_guide["professional_news"])
        
        return f"""You are a professional YouTube content creator specializing in news videos. Create a complete video script in English.

Category: {category.upper()}

Source Articles:
{context}

Instructions:
1. Create a COMPLETE video script (500-1200 words for 3-8 minute video)
2. Write in {style}
3. Structure:
   - HOOK: Compelling opening (first 10 seconds to grab attention)
   - INTRO: Brief introduction of the topic
   - MAIN CONTENT: 3-5 key points with details
   - CALL TO ACTION: Ask for likes, comments, subscribe
   - OUTRO: Summary and sign-off

4. YouTube Optimization:
   - Create a clickable title (under 60 characters, with keywords)
   - Write a detailed description (200-300 words)
   - Suggest 8-12 relevant tags
   - Include timestamps for each section

5. Style Guidelines:
   - Use natural, spoken language
   - Include transitions between sections
   - Add [PAUSE] markers where appropriate
   - Use [B-ROLL: description] for visual suggestions
   - Maintain engaging pace

Format your response EXACTLY as:
TITLE: [Your YouTube-optimized title]

HOOK: [First 10 seconds - the attention grabber]

SCRIPT:
[Full video script with sections clearly marked]

[Include timestamps like 0:00, 0:45, 2:15, etc.]

DESCRIPTION:
[Complete YouTube description with summary, links, timestamps, and hashtags]

TAGS: [tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8]

THUMBNAIL_TEXT: [Short punchy text for thumbnail - max 5 words]"""
    
    def _generate_with_openai(self, prompt: str) -> Optional[Dict]:
        """Generate script using OpenAI."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a professional YouTube content creator and scriptwriter."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=3000
        )
        
        content = response.choices[0].message.content
        return self._parse_script_response(content)
    
    def _generate_with_anthropic(self, prompt: str) -> Optional[Dict]:
        """Generate script using Anthropic."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        content = response.content[0].text
        return self._parse_script_response(content)
    
    def _parse_script_response(self, content: str) -> Optional[Dict]:
        """Parse the LLM response into structured script data."""
        try:
            lines = content.strip().split('\n')
            
            title = ""
            hook = ""
            script = []
            description = []
            tags = []
            thumbnail_text = ""
            timestamps = []
            
            current_section = None
            
            for line in lines:
                line_stripped = line.strip()
                
                if line_stripped.startswith('TITLE:'):
                    title = line_stripped.replace('TITLE:', '').strip()
                elif line_stripped.startswith('HOOK:'):
                    hook = line_stripped.replace('HOOK:', '').strip()
                    current_section = 'hook'
                elif line_stripped.startswith('SCRIPT:'):
                    current_section = 'script'
                elif line_stripped.startswith('DESCRIPTION:'):
                    current_section = 'description'
                elif line_stripped.startswith('TAGS:'):
                    tags_str = line_stripped.replace('TAGS:', '').strip()
                    tags = [tag.strip() for tag in tags_str.replace('[', '').replace(']', '').split(',')]
                    current_section = None
                elif line_stripped.startswith('THUMBNAIL_TEXT:'):
                    thumbnail_text = line_stripped.replace('THUMBNAIL_TEXT:', '').strip()
                    current_section = None
                elif current_section == 'hook' and line_stripped:
                    hook += " " + line_stripped
                elif current_section == 'script' and line_stripped:
                    script.append(line_stripped)
                    # Extract timestamps
                    if any(char.isdigit() and ':' in line_stripped[:10] for char in line_stripped[:10]):
                        timestamps.append(line_stripped)
                elif current_section == 'description' and line_stripped:
                    description.append(line_stripped)
            
            script_text = '\n\n'.join(script)
            description_text = '\n'.join(description)
            
            # Validation
            if not title or not script_text or len(script_text.split()) < Config.MIN_SCRIPT_LENGTH:
                print("Generated script does not meet minimum requirements")
                return None
            
            return {
                'title': title[:100],  # YouTube limit
                'hook': hook,
                'script': script_text,
                'description': description_text[:5000],  # YouTube limit
                'tags': tags[:12],  # Reasonable limit
                'thumbnail_text': thumbnail_text,
                'timestamps': timestamps,
                'word_count': len(script_text.split()),
                'estimated_duration': len(script_text.split()) // 150  # ~150 words per minute
            }
            
        except Exception as e:
            print(f"Error parsing script response: {str(e)}")
            return None
