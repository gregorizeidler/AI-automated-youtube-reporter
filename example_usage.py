"""
Example usage of new features.

This script demonstrates how to use all the new features together.
"""

from database import get_database
from multilang import LanguageManager
from news_sources import EnhancedNewsCollector
from scheduler import IntelligentScheduler
from voice_manager import VoiceManager
from thumbnail_generator import ThumbnailGenerator
from subtitle_generator import SubtitleGenerator
from config import Config


def example_1_database_tracking():
    """Example 1: Using database to track content."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Database Tracking")
    print("="*70)
    
    db = get_database()
    
    # Get statistics
    stats = db.get_statistics(days=30)
    print(f"\n📊 Last 30 days statistics:")
    print(f"  Total scripts: {stats['total_scripts']}")
    print(f"  Videos generated: {stats['videos_generated']}")
    print(f"  Videos uploaded: {stats['videos_uploaded']}")
    print(f"  By category: {stats['by_category']}")
    
    # Check recent topics to avoid duplicates
    recent_topics = db.get_recent_topics('sports', days=7)
    print(f"\n📝 Recent sports topics (last 7 days):")
    for topic in recent_topics[:5]:
        print(f"  - {topic}")


def example_2_multilanguage():
    """Example 2: Multi-language support."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Multi-language Support")
    print("="*70)
    
    languages = ['en', 'pt', 'es', 'fr']
    
    for lang in languages:
        lang_name = LanguageManager.get_language_name(lang)
        instruction = LanguageManager.get_prompt_instruction(lang)
        voice_code = LanguageManager.get_voice_code(lang)
        
        print(f"\n🌍 {lang_name} ({lang}):")
        print(f"  Voice code: {voice_code}")
        print(f"  Instruction: {instruction[:50]}...")


def example_3_multiple_news_sources():
    """Example 3: Collecting from multiple sources."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Multiple News Sources")
    print("="*70)
    
    collector = EnhancedNewsCollector()
    
    # Collect from all sources
    articles = collector.collect_from_all_sources(
        category='sports',
        language='en',
        use_newsapi=Config.USE_NEWSAPI,
        use_rss=Config.USE_RSS_FEEDS,
        use_reddit=Config.USE_REDDIT
    )
    
    print(f"\n📰 Collected {len(articles)} articles")
    
    # Show sources breakdown
    sources = {}
    for article in articles:
        source = article.get('source', 'Unknown')
        sources[source] = sources.get(source, 0) + 1
    
    print("\n📊 Sources breakdown:")
    for source, count in sources.items():
        print(f"  {source}: {count} articles")


def example_4_intelligent_scheduling():
    """Example 4: Intelligent scheduling."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Intelligent Scheduling")
    print("="*70)
    
    scheduler = IntelligentScheduler()
    
    # Get next optimal time for different categories
    categories = ['sports', 'politics', 'finance']
    
    print("\n📅 Next optimal posting times:")
    for category in categories:
        next_time = scheduler.get_next_optimal_time(
            category=category,
            min_hours_gap=4,
            timezone_offset=Config.TIMEZONE_OFFSET
        )
        print(f"  {category.capitalize()}: {next_time.strftime('%Y-%m-%d %H:%M')}")
    
    # Show upcoming schedule
    scheduler.print_schedule(days=7)


def example_5_voice_personalization():
    """Example 5: Voice personalization by category."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Voice Personalization")
    print("="*70)
    
    categories = ['sports', 'politics', 'finance', 'technology']
    language = Config.TARGET_LANGUAGE
    
    print(f"\n🎙️  Voice profiles for {language.upper()}:")
    
    for category in categories:
        voice = VoiceManager.get_voice_for_category(category, language)
        settings = VoiceManager.get_voice_settings(category)
        
        print(f"\n  {category.upper()}:")
        print(f"    Voice: {voice.name} ({voice.gender})")
        print(f"    Style: {voice.style}")
        print(f"    Stability: {settings['stability']}")
        print(f"    Expressiveness: {settings['style']}")


def example_6_thumbnail_generation():
    """Example 6: Automatic thumbnail generation."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Thumbnail Generation")
    print("="*70)
    
    generator = ThumbnailGenerator()
    
    print(f"\n🎨 Thumbnail mode: {Config.THUMBNAIL_MODE}")
    
    # Example: Generate template thumbnail
    if Config.THUMBNAIL_MODE == 'template' or not Config.AUTO_GENERATE_THUMBNAILS:
        print("\n📝 Generating template thumbnail...")
        thumbnail_path = generator.generate_template_thumbnail(
            title='Breaking Sports News: Championship Finals',
            category='sports',
            thumbnail_text='BIG GAME'
        )
        
        if thumbnail_path:
            print(f"✓ Thumbnail created: {thumbnail_path}")
    
    # Show what would happen with other modes
    print("\n💡 Other available modes:")
    print("  - template: Fast, free, customizable")
    print("  - ai: DALL-E 3, premium quality (~$0.04)")
    print("  - stock: Pexels/Unsplash, professional photos")


def example_7_subtitle_generation():
    """Example 7: Automatic subtitle generation."""
    print("\n" + "="*70)
    print("EXAMPLE 7: Subtitle Generation")
    print("="*70)
    
    generator = SubtitleGenerator()
    
    print(f"\n📝 Subtitle method: {Config.SUBTITLE_METHOD}")
    print(f"📝 Languages: {', '.join(Config.SUBTITLE_LANGUAGES)}")
    
    # Example script
    sample_script = """
    Welcome to today's news update. In breaking sports news, 
    the championship finals are set for this weekend. 
    Both teams have been preparing intensively for this crucial match.
    Analysts predict this could be one of the most exciting games of the season.
    """
    
    print("\n📄 Generating subtitles from script...")
    srt_path = generator.generate_srt_from_script(
        script_text=sample_script,
        title='Sample News Video',
        words_per_minute=150
    )
    
    if srt_path:
        print(f"✓ Subtitles created: {srt_path}")
        
        # Convert to WebVTT
        vtt_path = generator.generate_vtt_from_srt(srt_path)
        if vtt_path:
            print(f"✓ WebVTT created: {vtt_path}")
    
    print("\n💡 Available methods:")
    print("  - script: Fast, estimated timing, free")
    print("  - whisper: Accurate, transcribes audio, slower")


def example_8_complete_workflow():
    """Example 8: Complete workflow with all features."""
    print("\n" + "="*70)
    print("EXAMPLE 8: Complete Workflow")
    print("="*70)
    
    print("\n🎬 Simulating complete video creation workflow:\n")
    
    steps = [
        "1. ✓ Collect news from multiple sources (NewsAPI + RSS + Google)",
        "2. ✓ Check database for duplicate articles",
        "3. ✓ Generate script in target language (pt, es, en, etc.)",
        "4. ✓ Select optimal voice for category",
        "5. ✓ Generate video with AI voice/avatar",
        "6. ✓ Create thumbnail automatically",
        "7. ✓ Generate subtitles in multiple languages",
        "8. ✓ Schedule for optimal posting time",
        "9. ✓ Save everything to database",
        "10. ✓ Upload to YouTube (if enabled)"
    ]
    
    for step in steps:
        print(f"  {step}")
    
    print("\n💡 Configuration summary:")
    print(f"  Language: {Config.TARGET_LANGUAGE}")
    print(f"  Video mode: {Config.VIDEO_MODE}")
    print(f"  Thumbnail mode: {Config.THUMBNAIL_MODE}")
    print(f"  Subtitle method: {Config.SUBTITLE_METHOD}")
    print(f"  Auto voice selection: {Config.AUTO_SELECT_VOICE}")
    print(f"  Intelligent scheduling: {Config.USE_INTELLIGENT_SCHEDULING}")


def main():
    """Run all examples."""
    print("\n" + "="*70)
    print("🎉 NEW FEATURES EXAMPLES")
    print("="*70)
    print("\nThis script demonstrates all new features added to the system.")
    print("Check NEW_FEATURES.md for detailed documentation.\n")
    
    try:
        # Run examples
        example_1_database_tracking()
        example_2_multilanguage()
        example_3_multiple_news_sources()
        example_4_intelligent_scheduling()
        example_5_voice_personalization()
        example_6_thumbnail_generation()
        example_7_subtitle_generation()
        example_8_complete_workflow()
        
        print("\n" + "="*70)
        print("✅ All examples completed successfully!")
        print("="*70)
        print("\nNext steps:")
        print("1. Update your .env file with new configurations")
        print("2. Install new dependencies: pip install -r requirements.txt")
        print("3. Run: python main.py --once")
        print("\nRead NEW_FEATURES.md for detailed usage guide.")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}")
        print("Make sure all dependencies are installed and configured.")


if __name__ == "__main__":
    main()

