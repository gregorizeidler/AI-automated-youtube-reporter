"""YouTube API integration for uploading videos and managing content."""

import os
import pickle
from typing import Dict, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from config import Config


# YouTube API scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
          'https://www.googleapis.com/auth/youtube']


class YouTubeUploader:
    """Uploads videos and metadata to YouTube."""
    
    def __init__(self):
        """Initialize the YouTube uploader."""
        self.credentials = None
        self.youtube = None
        self.authenticate()
    
    def authenticate(self) -> bool:
        """
        Authenticate with YouTube API.
        
        Returns:
            True if successful, False otherwise
        """
        creds = None
        
        # Token file stores the user's access and refresh tokens
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Token refresh failed: {e}")
                    creds = None
            
            if not creds:
                if not os.path.exists(Config.YOUTUBE_CLIENT_SECRETS_FILE):
                    print(f"\n✗ YouTube credentials file not found: {Config.YOUTUBE_CLIENT_SECRETS_FILE}")
                    print("\nTo get YouTube API credentials:")
                    print("1. Go to: https://console.cloud.google.com/")
                    print("2. Create a project")
                    print("3. Enable YouTube Data API v3")
                    print("4. Create OAuth 2.0 credentials")
                    print("5. Download as 'client_secrets.json'")
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    Config.YOUTUBE_CLIENT_SECRETS_FILE, SCOPES)
                creds = flow.run_local_server(port=8080)
            
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        self.credentials = creds
        self.youtube = build('youtube', 'v3', credentials=creds)
        print("✓ Authenticated with YouTube API")
        return True
    
    def upload_video(
        self,
        video_file: str,
        title: str,
        description: str,
        tags: list = None,
        category_id: str = "25",  # 25 = News & Politics, 17 = Sports
        privacy_status: str = "private"  # private, unlisted, public
    ) -> Optional[Dict]:
        """
        Upload a video to YouTube.
        
        Args:
            video_file: Path to video file
            title: Video title (max 100 chars)
            description: Video description (max 5000 chars)
            tags: List of tags (max 500 chars total)
            category_id: YouTube category ID
            privacy_status: "private", "unlisted", or "public"
            
        Returns:
            Dictionary with upload details or None if failed
        """
        if not self.youtube:
            print("✗ Not authenticated with YouTube")
            return None
        
        if not os.path.exists(video_file):
            print(f"✗ Video file not found: {video_file}")
            return None
        
        # Prepare request body
        body = {
            'snippet': {
                'title': title[:100],
                'description': description[:5000],
                'tags': tags[:15] if tags else [],
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Create media upload
        media = MediaFileUpload(
            video_file,
            chunksize=-1,
            resumable=True,
            mimetype='video/*'
        )
        
        try:
            print(f"\n📤 Uploading video: {title}")
            print(f"   File: {video_file}")
            print(f"   Size: {os.path.getsize(video_file) / (1024*1024):.2f} MB")
            
            # Execute upload
            request = self.youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    print(f"   Progress: {progress}%")
            
            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            print(f"\n✓ Video uploaded successfully!")
            print(f"  Video ID: {video_id}")
            print(f"  URL: {video_url}")
            print(f"  Status: {privacy_status}")
            
            return {
                'id': video_id,
                'url': video_url,
                'title': title,
                'status': privacy_status
            }
            
        except Exception as e:
            print(f"✗ Upload failed: {str(e)}")
            return None
    
    def save_script_metadata(self, script_data: Dict, output_dir: str = "youtube_scripts") -> str:
        """
        Save script and metadata to file for manual video creation.
        
        Args:
            script_data: Script dictionary from ScriptGenerator
            output_dir: Directory to save files
            
        Returns:
            Path to saved file
        """
        os.makedirs(output_dir, exist_ok=True)
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create filename from title
        safe_title = "".join(c for c in script_data['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_title = safe_title.replace(' ', '_')[:50]
        
        filename = f"{timestamp}_{safe_title}.txt"
        filepath = os.path.join(output_dir, filename)
        
        # Format content
        content = f"""========================================
YOUTUBE VIDEO SCRIPT
========================================

TITLE: {script_data['title']}

ESTIMATED DURATION: {script_data.get('estimated_duration', 'N/A')} minutes
WORD COUNT: {script_data.get('word_count', 'N/A')}
CATEGORY: {script_data.get('category', 'N/A')}
GENERATED: {script_data.get('generated_at', 'N/A')}

========================================
THUMBNAIL TEXT
========================================
{script_data.get('thumbnail_text', 'N/A')}

========================================
HOOK (First 10 seconds)
========================================
{script_data.get('hook', 'N/A')}

========================================
FULL SCRIPT
========================================
{script_data['script']}

========================================
YOUTUBE DESCRIPTION
========================================
{script_data['description']}

========================================
TAGS
========================================
{', '.join(script_data.get('tags', []))}

========================================
SOURCES
========================================
"""
        
        for i, source in enumerate(script_data.get('sources', []), 1):
            content += f"{i}. {source}\n"
        
        content += "\n========================================\n"
        content += "INSTRUCTIONS FOR RECORDING:\n"
        content += "========================================\n"
        content += "1. Read the script naturally - don't rush\n"
        content += "2. Record in a quiet environment\n"
        content += "3. Use good lighting and clean audio\n"
        content += "4. Add B-roll footage where marked\n"
        content += "5. Create thumbnail with suggested text\n"
        content += "6. Use the description and tags when uploading\n"
        
        # Save file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Script saved: {filepath}")
        return filepath
    
    def get_upload_category(self, category: str) -> str:
        """Get YouTube category ID from content category."""
        category_map = {
            'sports': '17',  # Sports
            'politics': '25',  # News & Politics
            'finance': '25',  # News & Politics
            'news': '25'
        }
        return category_map.get(category.lower(), '25')


# Helper function for manual script review
def print_script_preview(script_data: Dict):
    """Print a preview of the generated script."""
    print("\n" + "="*70)
    print("SCRIPT PREVIEW")
    print("="*70)
    print(f"\n📹 TITLE: {script_data['title']}")
    print(f"⏱️  DURATION: ~{script_data.get('estimated_duration', 'N/A')} minutes")
    print(f"📝 WORDS: {script_data.get('word_count', 'N/A')}")
    print(f"🏷️  TAGS: {', '.join(script_data.get('tags', [])[:5])}...")
    print(f"\n🎬 HOOK:")
    print(f"   {script_data.get('hook', 'N/A')[:200]}...")
    print(f"\n📄 SCRIPT PREVIEW:")
    print(f"   {script_data['script'][:300]}...")
    print("\n" + "="*70 + "\n")

