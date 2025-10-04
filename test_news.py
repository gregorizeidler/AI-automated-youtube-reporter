"""Test script to verify news collection works."""

from news_collector import NewsCollector


def test_news_collection():
    """Test news collection for one category."""
    print("\n" + "="*70)
    print("🧪 TESTING NEWS COLLECTION")
    print("="*70 + "\n")
    
    # Initialize collector
    collector = NewsCollector()
    
    # Test with sports (usually has good results)
    category = "sports"
    print(f"📰 Testing category: {category}")
    print(f"⏳ Searching Google and extracting content...")
    print(f"⚠️  This may take 1-2 minutes, please wait...\n")
    
    # Collect articles
    articles = collector.collect_category_news(category, articles_per_query=2)
    
    # Display results
    print("\n" + "="*70)
    print("📊 RESULTS")
    print("="*70 + "\n")
    
    if articles:
        print(f"✅ Successfully collected {len(articles)} article(s)\n")
        
        for i, article in enumerate(articles, 1):
            print(f"{'─'*70}")
            print(f"📄 Article {i}:")
            print(f"{'─'*70}")
            print(f"📌 Title: {article['title']}")
            print(f"🔗 URL: {article['url']}")
            print(f"📏 Content length: {len(article['content'])} characters")
            print(f"📝 Preview:\n   {article['content'][:250]}...\n")
    else:
        print("❌ No articles collected")
        print("\n⚠️  Possible reasons:")
        print("  • Network connection issues")
        print("  • Google rate limiting")
        print("  • No recent news found")
        print("\n💡 Try:")
        print("  • Running again in a few minutes")
        print("  • Checking your internet connection")
        print("  • Using a different category")
    
    print("="*70)
    print("✅ Test complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_news_collection()

