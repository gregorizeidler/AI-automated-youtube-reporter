"""Main orchestration script for automated YouTube content creation."""

import time
import schedule
from datetime import datetime
from config import Config
from news_collector import NewsCollector
from script_generator import ScriptGenerator
from youtube_uploader import YouTubeUploader, print_script_preview
from video_generator_manager import VideoGeneratorManager


class AutomatedYouTubeReporter:
    """Main class orchestrating the automated YouTube content creation system."""
    
    def __init__(self):
        """Initialize the automated reporter."""
        self.collector = NewsCollector()
        self.generator = ScriptGenerator()
        self.video_manager = VideoGeneratorManager()
        self.uploader = YouTubeUploader() if Config.AUTO_UPLOAD else None
    
    def run_single_cycle(self, save_only: bool = True):
        """
        Execute a single content generation cycle.
        
        Args:
            save_only: If True, only saves scripts. If False, uploads videos (requires video files)
        """
        print("\n" + "="*70)
        print(f"AUTOMATED YOUTUBE REPORTER - Starting Cycle")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70 + "\n")
        
        # Step 1: Collect news from all categories
        print("STEP 1: Collecting news...")
        all_news = self.collector.collect_all_categories()
        
        total_articles = sum(len(articles) for articles in all_news.values())
        print(f"\n✓ Collection complete: {total_articles} articles collected")
        
        if total_articles == 0:
            print("✗ No articles collected. Ending cycle.")
            return
        
        # Step 2: Generate video scripts from collected news
        print("\n" + "-"*70)
        print("STEP 2: Generating video scripts...")
        print("-"*70 + "\n")
        
        generated_scripts = []
        scripts_to_generate = min(Config.MAX_ARTICLES_PER_RUN, len(Config.CATEGORIES))
        
        for category, news_items in all_news.items():
            if len(generated_scripts) >= scripts_to_generate:
                break
            
            if not news_items:
                print(f"Skipping {category} - no news items")
                continue
            
            print(f"\nGenerating script for: {category.upper()}")
            print(f"Using {len(news_items)} news sources...")
            
            script = self.generator.generate_video_script(news_items, category)
            
            if script:
                generated_scripts.append(script)
                print_script_preview(script)
            else:
                print(f"✗ Failed to generate script for {category}")
            
            # Small delay between generations
            time.sleep(2)
        
        print(f"\n✓ Generation complete: {len(generated_scripts)} scripts generated")
        
        if not generated_scripts:
            print("✗ No scripts generated. Ending cycle.")
            return
        
        # Step 3: Generate videos or save scripts
        print("\n" + "-"*70)
        if Config.VIDEO_MODE == "script_only":
            print("STEP 3: Saving scripts...")
        else:
            print("STEP 3: Generating videos...")
        print("-"*70 + "\n")
        
        # Show mode info
        self.video_manager.print_mode_info()
        
        saved_count = 0
        generated_videos = []
        
        for script in generated_scripts:
            print(f"\nProcessing: '{script['title']}'...")
            
            # Save script first (always)
            from youtube_uploader import YouTubeUploader
            temp_uploader = YouTubeUploader()
            script_path = temp_uploader.save_script_metadata(script)
            if script_path:
                saved_count += 1
                print(f"✓ Script saved: {script_path}")
            
            # Generate video if enabled
            if Config.VIDEO_MODE != "script_only":
                video_path = self.video_manager.generate_video(script)
                
                if video_path:
                    generated_videos.append({
                        'path': video_path,
                        'script': script
                    })
                    print(f"✓ Video ready: {video_path}")
                else:
                    print(f"⚠️  Video generation failed, script still available")
            
            time.sleep(1)
        
        # Step 4: Upload to YouTube (if enabled)
        uploaded_count = 0
        if Config.AUTO_UPLOAD and generated_videos and self.uploader:
            print("\n" + "-"*70)
            print("STEP 4: Uploading to YouTube...")
            print("-"*70 + "\n")
            
            for video_data in generated_videos:
                video_path = video_data['path']
                script = video_data['script']
                
                print(f"\nUploading: {script['title']}...")
                
                # Get category ID
                category_id = self.uploader.get_upload_category(script.get('category', 'news'))
                
                result = self.uploader.upload_video(
                    video_file=video_path,
                    title=script['title'],
                    description=script['description'],
                    tags=script.get('tags', []),
                    category_id=category_id,
                    privacy_status="private"  # Upload as private for review
                )
                
                if result:
                    uploaded_count += 1
                    print(f"✓ Uploaded: {result['url']}")
                
                time.sleep(5)  # Delay between uploads
        
        # Summary
        print("\n" + "="*70)
        print("CYCLE COMPLETE - SUMMARY")
        print("="*70)
        print(f"✓ Articles collected: {total_articles}")
        print(f"✓ Scripts generated: {len(generated_scripts)}")
        print(f"✓ Scripts saved: {saved_count}")
        
        if Config.VIDEO_MODE != "script_only":
            print(f"✓ Videos generated: {len(generated_videos)}")
            print(f"📁 Videos saved in: generated_videos/")
        
        if Config.AUTO_UPLOAD and uploaded_count > 0:
            print(f"✓ Videos uploaded to YouTube: {uploaded_count}")
            print(f"⚠️  Videos uploaded as PRIVATE - review before publishing")
        
        print(f"✓ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\n📁 Scripts saved in: youtube_scripts/")
        
        if Config.VIDEO_MODE == "script_only":
            print(f"📝 Ready for video production!")
        elif not Config.AUTO_UPLOAD:
            print(f"📝 Videos ready for manual YouTube upload!")
        
        print("="*70 + "\n")
    
    def run_scheduled(self):
        """Run the reporter on a schedule."""
        print("\n" + "="*70)
        print("AUTOMATED YOUTUBE REPORTER - SCHEDULED MODE")
        print("="*70)
        print(f"Categories: {', '.join(Config.CATEGORIES)}")
        print(f"Interval: Every {Config.PUBLISH_INTERVAL_HOURS} hours")
        print(f"Max scripts per run: {Config.MAX_ARTICLES_PER_RUN}")
        print(f"LLM Provider: {Config.LLM_PROVIDER} ({Config.MODEL_NAME})")
        print(f"Video Style: {Config.VIDEO_STYLE}")
        print("="*70 + "\n")
        
        # Schedule the job
        schedule.every(Config.PUBLISH_INTERVAL_HOURS).hours.do(self.run_single_cycle)
        
        # Run immediately on start
        print("Running initial cycle...")
        self.run_single_cycle()
        
        # Keep running scheduled jobs
        print(f"\nScheduler active. Next run in {Config.PUBLISH_INTERVAL_HOURS} hours.")
        print("Press Ctrl+C to stop.\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n\nScheduler stopped by user.")


def main():
    """Main entry point."""
    # Validate configuration
    if not Config.validate():
        print("\n✗ Configuration validation failed!")
        print("Please check your .env file and ensure all required variables are set.")
        return
    
    print("\n✓ Configuration validated successfully!")
    print(f"\n🎥 YOUTUBE AUTOMATED REPORTER")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"This system will:")
    print(f"  1. Collect real-time news from Google")
    print(f"  2. Generate professional YouTube video scripts")
    print(f"  3. Create optimized titles, descriptions, and tags")
    print(f"  4. Save everything ready for video production")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    # Create reporter instance
    reporter = AutomatedYouTubeReporter()
    
    # Check if running in scheduled mode or single run
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        print("\nRunning in SINGLE-RUN mode...")
        reporter.run_single_cycle()
    else:
        print("\nRunning in SCHEDULED mode...")
        reporter.run_scheduled()


if __name__ == "__main__":
    main()
