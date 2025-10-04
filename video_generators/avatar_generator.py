"""Option 2: Virtual Avatar video generator using D-ID."""

import os
import time
import requests
from typing import Dict, Optional
from .base_generator import BaseVideoGenerator
from config import Config


class AvatarGenerator(BaseVideoGenerator):
    """Generate videos with virtual avatar presenter using D-ID API."""
    
    def __init__(self):
        """Initialize avatar generator."""
        super().__init__()
        self.api_key = Config.DID_API_KEY
        self.presenter_id = Config.DID_PRESENTER_ID
        self.base_url = "https://api.d-id.com"
    
    def generate_video(self, script_data: Dict) -> Optional[str]:
        """
        Generate video with virtual avatar presenter.
        
        Steps:
        1. Send script to D-ID API
        2. Wait for video generation
        3. Download completed video
        """
        try:
            print(f"\n🎬 Generating video with Virtual Avatar...")
            print(f"   Title: {script_data['title']}")
            
            if not self.api_key:
                print("   ⚠️  D-ID API key not configured")
                print("   💡 Get your key at: https://www.d-id.com/")
                return None
            
            # Step 1: Create talk
            print("   🎭 Creating avatar presentation...")
            talk_id = self._create_talk(script_data['script'])
            
            if not talk_id:
                return None
            
            # Step 2: Wait for completion
            print("   ⏳ Waiting for video generation (this may take 2-5 minutes)...")
            video_url = self._wait_for_completion(talk_id)
            
            if not video_url:
                return None
            
            # Step 3: Download video
            print("   📥 Downloading video...")
            output_path = self._download_video(video_url, script_data['title'])
            
            if output_path:
                print(f"   ✅ Video generated: {output_path}")
            
            return output_path
            
        except Exception as e:
            print(f"   ❌ Error generating video: {str(e)}")
            return None
    
    def _create_talk(self, script: str) -> Optional[str]:
        """Create a talk (video generation request) via D-ID API."""
        url = f"{self.base_url}/talks"
        
        headers = {
            "Authorization": f"Basic {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Limit script length (D-ID has limits)
        max_chars = 2000
        if len(script) > max_chars:
            script = script[:max_chars] + "..."
        
        payload = {
            "source_url": f"https://d-id-public-bucket.s3.amazonaws.com/alice.jpg",
            "script": {
                "type": "text",
                "input": script,
                "provider": {
                    "type": "microsoft",
                    "voice_id": "en-US-JennyNeural"
                }
            },
            "config": {
                "fluent": True,
                "pad_audio": 0
            }
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code in [200, 201]:
                data = response.json()
                return data.get('id')
            else:
                print(f"   ❌ D-ID API error: {response.status_code}")
                print(f"   Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error creating talk: {str(e)}")
            return None
    
    def _wait_for_completion(self, talk_id: str, timeout: int = 300) -> Optional[str]:
        """Poll D-ID API until video is ready."""
        url = f"{self.base_url}/talks/{talk_id}"
        
        headers = {
            "Authorization": f"Basic {self.api_key}"
        }
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    status = data.get('status')
                    
                    if status == 'done':
                        return data.get('result_url')
                    elif status == 'error':
                        print(f"   ❌ Video generation failed: {data.get('error')}")
                        return None
                    elif status in ['created', 'started']:
                        print(f"   ⏳ Status: {status}...")
                        time.sleep(10)  # Wait 10 seconds before next poll
                    else:
                        print(f"   ⚠️  Unknown status: {status}")
                        time.sleep(10)
                else:
                    print(f"   ❌ Error checking status: {response.status_code}")
                    return None
                    
            except Exception as e:
                print(f"   ❌ Error polling status: {str(e)}")
                return None
        
        print("   ⏱️  Timeout waiting for video generation")
        return None
    
    def _download_video(self, video_url: str, title: str) -> Optional[str]:
        """Download the generated video."""
        try:
            response = requests.get(video_url, stream=True)
            
            if response.status_code == 200:
                output_filename = self._sanitize_filename(title)
                output_path = os.path.join(self.output_dir, output_filename)
                
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                return output_path
            else:
                print(f"   ❌ Download failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error downloading video: {str(e)}")
            return None

