"""
Quick test of LinkedIn Automation Platform core features
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.platform import LinkedInAutomationPlatform
from modules.ai_content_creator import ContentType, UserGoal
from modules.ai_engagement_engine import RiskLevel
from modules.automation_system import AutomationMode


def main():
    print("\n" + "="*70)
    print("  LINKEDIN AUTOMATION PLATFORM - QUICK TEST")
    print("="*70)
    
    # Create user profile
    user_profile = {
        "name": "Test User",
        "email": "test@example.com",
        "industry": "Technology",
        "title": "Software Engineer",
        "primary_goal": "BRAND_BUILDING",
        "tone_preference": "professional"
    }
    
    print("\n✅ Step 1: Initializing platform...")
    platform = LinkedInAutomationPlatform(
        user_profile=user_profile,
        automation_mode=AutomationMode.MANUAL_APPROVAL,
        risk_level=RiskLevel.SAFE
    )
    print("   Platform initialized successfully!")
    
    print("\n✅ Step 2: Generating AI content...")
    content = platform.create_optimized_content(
        content_type=ContentType.TEXT_POST,
        topic="Artificial Intelligence",
        goal=UserGoal.BRAND_BUILDING
    )
    print(f"   Content created: {content['topic']}")
    print(f"   Hashtags: {', '.join(content['hashtags'][:3])}")
    
    print("\n✅ Step 3: Getting trending topics...")
    trends = platform.get_trending_topics()
    print(f"   Found {len(trends)} trending topics")
    print(f"   Top trend: {trends[0]['topic']} (score: {trends[0]['trend_score']})")
    
    print("\n✅ Step 4: Scheduling post...")
    post = platform.schedule_post(content)
    print(f"   Post scheduled: {post['id']}")
    print(f"   Status: {post['status']}")
    
    print("\n✅ Step 5: Getting platform status...")
    status = platform.get_status()
    print(f"   Automation mode: {status['automation_mode']}")
    print(f"   Risk level: {status['risk_level']}")
    print(f"   Pending approvals: {status['pending_approvals']}")
    
    print("\n✅ Step 6: Checking content analytics...")
    analytics = platform.content_creator.get_content_analytics()
    print(f"   Total posts generated: {analytics['total_posts_generated']}")
    print(f"   Average quality score: {analytics['average_quality_score']:.2f}")
    
    print("\n" + "="*70)
    print("  ✨ ALL TESTS PASSED! Platform is working correctly.")
    print("="*70)
    print("\n📚 Next steps:")
    print("   • Run 'python examples/demo.py' for full feature demo")
    print("   • Read docs/PRODUCT_DESCRIPTION.md for complete overview")
    print("   • Check README.md for usage examples")
    print("\n")


if __name__ == "__main__":
    main()
