"""Test script to verify AI script generation works."""

import os
from config import Config
from script_generator import ScriptGenerator
from youtube_uploader import print_script_preview


def test_script_generation():
    """Test script generation with sample news."""
    print("\n" + "="*70)
    print("🧪 TESTING AI SCRIPT GENERATION")
    print("="*70 + "\n")
    
    # Check API key
    if not Config.OPENAI_API_KEY and not Config.ANTHROPIC_API_KEY:
        print("❌ No API key found!")
        print("\n📝 Please set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env")
        print("\n💡 Get your key from:")
        print("  • OpenAI: https://platform.openai.com/")
        print("  • Anthropic: https://console.anthropic.com/")
        return
    
    print(f"🤖 Using: {Config.LLM_PROVIDER.upper()} ({Config.MODEL_NAME})")
    print(f"🎬 Video Style: {Config.VIDEO_STYLE}")
    print()
    
    # Sample news items (realistic sports news)
    sample_news = [
        {
            'title': 'Championship Game Ends in Dramatic Fashion',
            'description': 'Local team wins in overtime after incredible comeback',
            'content': '''In an extraordinary display of athleticism and determination, 
the home team staged a remarkable comeback to win the championship in overtime. 
The victory marks their first championship in over a decade and cements this season 
as one of the most memorable in franchise history.

Down by 15 points with just 8 minutes remaining, the team refused to give up. 
The MVP of the game led the charge with 35 points, including the game-winning shot 
in the final seconds of overtime. The arena erupted as thousands of fans celebrated 
the historic moment.

"This is what we've been working towards all season," said the team captain in a 
post-game interview. "Every practice, every game, it all led to this moment. I couldn't 
be prouder of this team."

The championship parade is scheduled for this weekend, with the city expecting 
massive crowds to celebrate the victory. This marks a new era for the franchise 
and gives hope to fans for sustained success in coming seasons.''',
            'url': 'https://example.com/sports/championship-win',
            'source': 'Sports News Network',
            'published_at': '2025-10-03'
        },
        {
            'title': 'Star Player Breaks All-Time Scoring Record',
            'description': 'Veteran athlete sets new milestone in historic performance',
            'content': '''A legendary player etched their name permanently in the record 
books last night, breaking the all-time career scoring record in front of a sold-out 
crowd. The achievement came midway through the third quarter, drawing a five-minute 
standing ovation from fans, players, and coaches alike.

The record-breaking moment was pure poetry in motion - a signature move that has 
defined this player's incredible 15-year career. As the basket was confirmed, the 
game was paused for a ceremony honoring this historic achievement.

"To all the young athletes watching, this is proof that hard work and dedication 
pay off," the player said during the on-court ceremony. "I've been blessed to play 
this game for so long, and breaking this record is surreal."

League officials and fellow players took to social media to congratulate the new 
record holder. Many consider this one of the greatest individual achievements in 
sports history. The player shows no signs of slowing down and could extend the 
record significantly before retirement.''',
            'url': 'https://example.com/sports/scoring-record',
            'source': 'Athletic Times',
            'published_at': '2025-10-03'
        },
        {
            'title': 'Unexpected Team Emerges as Season Favorites',
            'description': 'Underdog squad defying all expectations with winning streak',
            'content': '''What started as a season with modest expectations has turned 
into one of the most surprising success stories in recent memory. The team, picked 
by many analysts to finish near the bottom of their division, currently sits at the 
top of the standings with an impressive 12-game winning streak.

The turnaround can be attributed to several factors: excellent team chemistry, 
strategic coaching adjustments, and breakout performances from young players. 
The roster, assembled with careful planning and smart trades, is proving that 
teamwork and system play can overcome individual superstar power.

"Nobody believed in us except the people in this locker room," said the head coach. 
"We've built something special here, and we're not done yet. This is just the beginning."

Fans are rallying behind the team's underdog story, with attendance at home games 
increasing dramatically. Merchandise sales have tripled, and the city is embracing 
their unexpected contenders. Sports analysts are now reconsidering their preseason 
predictions and giving this team serious championship consideration.''',
            'url': 'https://example.com/sports/underdog-story',
            'source': 'Sports Illustrated',
            'published_at': '2025-10-02'
        }
    ]
    
    # Initialize generator
    generator = ScriptGenerator()
    
    print("⏳ Generating YouTube script from sample news...")
    print("⚠️  This may take 30-60 seconds, please wait...\n")
    
    # Generate script
    script = generator.generate_video_script(sample_news, "sports")
    
    # Display results
    print("\n" + "="*70)
    print("📊 RESULTS")
    print("="*70 + "\n")
    
    if script:
        print("✅ Script generated successfully!\n")
        
        # Show detailed preview
        print_script_preview(script)
        
        # Show detailed breakdown
        print("📋 DETAILED BREAKDOWN:")
        print(f"{'─'*70}")
        print(f"📺 Title: {script['title']}")
        print(f"   Length: {len(script['title'])} chars (YouTube limit: 100)")
        print(f"\n⏱️  Estimated Duration: {script['estimated_duration']} minutes")
        print(f"📝 Word Count: {script['word_count']} words")
        print(f"\n🎯 Hook (First 10 seconds):")
        print(f"   {script['hook'][:150]}...")
        print(f"\n🏷️  Tags ({len(script['tags'])}):")
        print(f"   {', '.join(script['tags'])}")
        print(f"\n🖼️  Thumbnail Text:")
        print(f"   \"{script['thumbnail_text']}\"")
        print(f"\n📄 Full Script Preview:")
        print(f"{'─'*70}")
        print(script['script'][:600] + "...\n")
        print(f"{'─'*70}")
        print(f"\n📝 Description Preview:")
        print(f"{'─'*70}")
        print(script['description'][:400] + "...\n")
        
        # Save option
        print("\n💾 SAVE SCRIPT?")
        print(f"{'─'*70}")
        save = input("Save this script to file? (y/n): ").lower().strip()
        
        if save == 'y':
            from youtube_uploader import YouTubeUploader
            uploader = YouTubeUploader()
            filepath = uploader.save_script_metadata(script)
            print(f"\n✅ Script saved to: {filepath}")
            print(f"📁 You can now use this script to create your video!")
        
    else:
        print("❌ Failed to generate script")
        print("\n⚠️  Possible issues:")
        print("  • API key invalid or expired")
        print("  • Insufficient API credits")
        print("  • Model name incorrect")
        print("  • Network connection issues")
        print("\n💡 Try:")
        print("  • Checking your API key in .env")
        print("  • Verifying your account has credits")
        print("  • Testing your internet connection")
    
    print("\n" + "="*70)
    print("✅ Test complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_script_generation()

